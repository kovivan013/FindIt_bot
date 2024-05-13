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

    async def get_data(
            self,
            path: str
    ) -> dict:
        keys = self.__collect_path(path)
        result: dict = {}

        async with self.state.proxy() as session:
            for i in keys:
                result = session.setdefault(
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
    ) -> Union[BaseModel]:
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

            session.update(
                update_path
            )

        return kwargs

    async def clear_partial_data(
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



