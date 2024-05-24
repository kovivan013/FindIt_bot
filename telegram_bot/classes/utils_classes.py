import jwt

from datetime import datetime
from aiogram.types import Message, InlineKeyboardMarkup, InputMedia
from common.classes import FSMActions
from decorators.decorators import handle_error
from typing import Union, Optional
from pydantic import BaseModel
from common.interfaces import OAuthStructure, DataModel
from aiogram.dispatcher.storage import FSMContext
from utils.utils import timestamp
from config import settings


class OAuth2:

    __SECRET_KEY: str = settings.SECRET_KEY

    @classmethod
    async def _prepare_token(
            cls,
            auth: int
    ) -> str:
        request = OAuthStructure(
            id_=auth,
            exp=timestamp() + 60
        )

        return jwt.encode(
            request.model_dump(),
            cls.__SECRET_KEY,
            algorithm="HS256"
        )


class FSMStorageProxy:

    def __init__(
            self,
            state: FSMContext
    ):
        self.state = state

    def __collect_path(
            self,
            path: str
    ) -> list:
        return [i for i in path.split("/") if i]

    def __update(
            self,
            base: dict,
            data: dict
    ):
        for i, v in data.items():
            if all([
                isinstance(
                    v, dict
                ),
                i in base,
                isinstance(
                    base.get(
                        i, None
                    ), dict
                )
            ]):
                self.__update(
                    base.setdefault(
                        i, {}
                    ),
                    v
                )
            else:
                base[i] = v

        return base

    async def get_data(
            self,
            path: str
    ) -> dict:
        keys = self.__collect_path(path)

        async with self.state.proxy() as session:
            result = session
            for i in keys:
                result = result.setdefault(
                    i, {}
                )

        return result

    async def collect_model(
            self,
            path: str,
            model: BaseModel
    ) -> Union[BaseModel]:
        return model().model_validate(
            await self.get_data(path)
        )

    async def data_model(
            self,
            path: str
    ) -> Union[DataModel]:
        return DataModel(
            await self.get_data(path)
        )

    async def update_data(
            self,
            path: str,
            /,
            **kwargs
    ) -> dict:
        keys = self.__collect_path(path)
        update_path: dict = {}

        async with self.state.proxy() as session:
            default = session
            for i in keys:
                default = default.get(
                    i, {}
                )

            default.update(
                kwargs
            )

            update_path.update({
                keys[-1]: default
            })

            for i in reversed(keys[:-1]):
                update_path = {
                    i: update_path
                }

            session = self.__update(
                session,
                update_path
            )

        return kwargs

    async def set_data(
            self,
            path: str,
            /,
            data: dict
    ) -> dict:
        keys = self.__collect_path(path)
        update_path: dict = {}

        async with self.state.proxy() as session:
            update_path.update({
                keys[-1]: data
            })

            for i in reversed(keys[:-1]):
                update_path = {
                    i: update_path
                }

            session.update(
                update_path
            )

        return data

    async def clear_data(
            self,
            path: str
    ) -> None:
        keys = self.__collect_path(path)

        async with self.state.proxy() as session:
            update_path: dict = {}

            for i in keys:
                update_path = {
                    i: update_path
                }

                session.update(
                    update_path
                )


class MessageProxy(FSMStorageProxy):

    @handle_error
    async def edit_text(
            self,
            text: str,
            parse_mode: Optional[str] = None,
            entities: Optional[list] = None,
            disable_web_page_preview: Optional[bool] = None,
            reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> Union[Message]:
        return await (
            await self.data_model(
                FSMActions.APP_CONFIG
            )
        ).message.edit_text(
            text=text,
            parse_mode=parse_mode,
            entities=entities,
            disable_web_page_preview=disable_web_page_preview,
            reply_markup=reply_markup
        )

    @handle_error
    async def edit_caption(
            self,
            caption: str,
            parse_mode: Optional[str] = None,
            caption_entities: Optional[list] = None,
            reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> Union[Message]:
        return await (
            await self.data_model(
                FSMActions.APP_CONFIG
            )
        ).message.edit_caption(
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            reply_markup=reply_markup
        )

    @handle_error
    async def edit_media(
            self,
            media: InputMedia,
            reply_markup: Optional[InlineKeyboardMarkup] = None
    ):
        return await (
            await self.data_model(
                FSMActions.APP_CONFIG
            )
        ).message.edit_media(
            media=media,
            reply_markup=reply_markup
        )

    @handle_error
    async def edit_reply_markup(
            self,
            reply_markup: InlineKeyboardMarkup
    ) -> Union[Message]:
        return await (
            await self.data_model(
                FSMActions.APP_CONFIG
            )
        ).message.edit_reply_markup(
            reply_markup=reply_markup
        )

    @handle_error
    async def delete_message(self) -> bool:
        return await (
            await self.data_model(
                FSMActions.APP_CONFIG
            )
        ).message.delete()

    @handle_error
    async def update_deletion_list(
            self,
            message: Message
    ) -> None:
        deletion_list = (
            await self.data_model(
                FSMActions.APP_CONFIG
            )
        ).deletion_list

        deletion_list.append(
            message
        )

        await self.update_data(
            FSMActions.APP_CONFIG,
            deletion_list=deletion_list
        )

    @handle_error
    async def clear_deletion_list(self) -> None:
        deletion_list = (
            await self.data_model(
                FSMActions.APP_CONFIG
            )
        ).deletion_list

        for message in deletion_list:

            success = False

            try:
                success = await message.delete()
            finally:
                if success:
                    deletion_list = deletion_list[1:]

        await self.update_data(
            FSMActions.APP_CONFIG,
            deletion_list=deletion_list
        )


class Dashboard(FSMStorageProxy):

    pass
    # async def send_announcements(self) -> None:
    #
    #     response = await AnnouncementsAPI.get_announcements(
    #         state.user,
    #         **(
    #             await storage.get_data(
    #                 FSMActions.GET_ANNOUNCEMENTS
    #             )
    #         )
    #     )
    #
    #     if response._success:
    #
    #         await event.message.edit_caption(
    #             caption=f"За Вашим запитом було знайдено *{response.data.document.pages * 2 - 1}+* оголошень.",
    #             parse_mode="Markdown",
    #             reply_markup=DashboardMenu.keyboard(
    #                 page=response.data.document.page + 1,
    #                 pages=response.data.document.pages
    #             )
    #         )
    #
    #         for i, announcement in response.data.announcements.as_dict().items():
    #             caption = f"{announcement.title}\n\n" \
    #                       f"" \
    #                       f"📍 *{announcement.location.place_name}*\n" \
    #                       f"⌚ *{utils.to_date(announcement.timestamp)}*"
    #
    #             await MessageProxy(state).update_deletion_list(
    #                 await event.message.answer_photo(
    #                     photo=blob.get_preview(
    #                         announcement.announcement_id
    #                     ),
    #                     caption=caption,
    #                     parse_mode="Markdown",
    #                     disable_notification=True
    #                 )
    #             )



