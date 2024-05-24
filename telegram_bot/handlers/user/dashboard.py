# Потерявшие вещь выставляют для детективов

from aiogram import Dispatcher
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardRemove,
    InputMedia,
    InputFile,
    ContentTypes,
    ForceReply
)
from . import signup

from config import dp, bot
from common import dtos
from common.interfaces import DataStructure
from common.classes import ServicePhotos, Symbols, FSMActions
from classes.utils_classes import (
    FSMStorageProxy,
    MessageProxy
)
from network.s3 import blob
from classes.api_requests import UserAPI, AnnouncementsAPI
from utils import utils
from keyboards.keyboards import (
    MainMenu,
    DashboardMenu,
    YesOrNo,
    Controls
)
from states.states import (
    MainMenuStates,
    DashboardStates,
    GetAnnouncementStates
)
from common.schemas import BaseUser
from decorators.decorators import (
    check_registered,
    private_message
)


@check_registered()
async def dashboard(
        event: CallbackQuery,
        state: FSMContext
) -> None:
    await DashboardStates.input_query.set()
    await MessageProxy(state).clear_deletion_list()
    await event.message.edit_media(
        media=InputMedia(
            media=utils.get_photo(
                ServicePhotos.ANNOUNCEMENTS_DASHBOARD
            ),
            caption="🔍 *Що шукаємо сьогодні?* Просто уведіть пошуковий запит.",
            parse_mode="Markdown"
        ),
        reply_markup=YesOrNo.cancel_inline_keyboard()
    )

async def select_mode(
        event: Message,
        state: FSMContext
) -> None:
    await event.delete()
    await FSMStorageProxy(state).update_data(
        FSMActions.GET_ANNOUNCEMENTS,
        query=event.text
    )
    await MessageProxy(state).edit_caption(
        caption=f"Які речі Ви шукаєте за запитом *{event.text}*?",
        parse_mode="Markdown",
        reply_markup=DashboardMenu.options_keyboard()
    )

async def collect_result(
        event: CallbackQuery,
        state: FSMContext
) -> None:
    await DashboardStates.query_result.set()
    storage = FSMStorageProxy(state)
    await storage.update_data(
        FSMActions.GET_ANNOUNCEMENTS,
        mode=DashboardMenu.modes[
            event.data
        ],
        page=0,
        limit=2
    )

    response = await AnnouncementsAPI.get_announcements(
        state.user,
        **(
            await storage.get_data(
                FSMActions.GET_ANNOUNCEMENTS
            )
        )
    )

    await storage.update_data(
        FSMActions.COLLECTED_ANNOUNCEMENTS,
        p0=response.data.announcements.model_dump()
    )
    await storage.set_data(
        FSMActions.DOCUMENT,
        data=response.data.document.as_dict()
    )

    if response._success:

        await event.message.edit_caption(
            caption=f"За Вашим запитом було знайдено *{response.data.document.pages * 2}+* оголошень.",
            parse_mode="Markdown",
            reply_markup=DashboardMenu.keyboard(
                page=response.data.document.page + 1,
                pages=response.data.document.pages
            )
        )

        for i, announcement in response.data.announcements.as_dict().items():

            await MessageProxy(state).update_deletion_list(
                await event.message.answer_photo(
                    photo=blob.get_preview(
                        announcement.announcement_id
                    ),
                    caption=utils.announcement_caption(
                        announcement
                    ),
                    reply_markup=DashboardMenu.announcement_keyboard(
                        announcement.announcement_id
                    ),
                    parse_mode="Markdown",
                    disable_notification=True
                )
            )


async def update_page(
        event: CallbackQuery,
        state: FSMContext
) -> None:
    await DashboardStates.query_result.set()
    storage = FSMStorageProxy(state)
    pages = (
        await storage.data_model(
            FSMActions.DOCUMENT
        )
    ).pages

    next_page: dict = {
        Controls.previous_page_callback: lambda page = (
            await storage.data_model(
                FSMActions.GET_ANNOUNCEMENTS
            )
        ).page: page - 1 if page > 0 else 0,
        Controls.next_page_callback: lambda page = (
            await storage.data_model(
                FSMActions.GET_ANNOUNCEMENTS
            )
        ).page: page + 1 if page < pages else pages,
        Controls.backward_callback: lambda page = (
            await storage.data_model(
                FSMActions.GET_ANNOUNCEMENTS
            )
        ).page: page
    }

    page = next_page[
        event.data
    ]()

    await storage.update_data(
        FSMActions.GET_ANNOUNCEMENTS,
        page=page
    )

    collected_announcements = await storage.data_model(
        FSMActions.COLLECTED_ANNOUNCEMENTS
    )

    if (page_key := f"p{page}") in collected_announcements.as_dict():
        announcements = collected_announcements.as_dict()[page_key]
    else:
        response = await AnnouncementsAPI.get_announcements(
            state.user,
            **(
                await storage.get_data(
                    FSMActions.GET_ANNOUNCEMENTS
                )
            )
        )
        await storage.update_data(
            FSMActions.COLLECTED_ANNOUNCEMENTS,
            **{
                page_key: response.data.announcements.model_dump()
            }
        )
        announcements = response.data.announcements

        await storage.set_data(
            FSMActions.DOCUMENT,
            data=response.data.document.as_dict()
        )

    await MessageProxy(state).clear_deletion_list()
    await event.message.edit_reply_markup(
        reply_markup=DashboardMenu.keyboard(
            page=page + 1,
            pages=pages
        )
    )

    for i, announcement in announcements.as_dict().items():

        await MessageProxy(state).update_deletion_list(
            await event.message.answer_photo(
                photo=blob.get_preview(
                    announcement.announcement_id
                ),
                caption=utils.announcement_caption(
                    announcement
                ),
                reply_markup=DashboardMenu.announcement_keyboard(
                    announcement.announcement_id
                ),
                parse_mode="Markdown",
                disable_notification=True
            )
        )

async def filters_menu(
        event: CallbackQuery,
        state: FSMContext
) -> None:
    pass

async def get_announcement(
        event: CallbackQuery,
        state: FSMContext
) -> None:
    announcement_id = event.data.split("_")[0]
    response = await AnnouncementsAPI.get_announcement(
        state.user,
        announcement_id=announcement_id
    )

    if response._success:

        await GetAnnouncementStates.preview.set()
        await MessageProxy(state).clear_deletion_list()
        return await MessageProxy(state).edit_media(
            media=InputMedia(
                media=blob.get_preview(
                    announcement_id
                ),
                caption=utils.announcement_details(
                    response.data
                ),
                parse_mode="Markdown"
            ),
            reply_markup=DashboardMenu.preview_keyboard(
                response.data.mode
            )
        )

    await event.answer(
        text=f"❌ {response.message}",
        show_alert=True
    )

def register(
        dp: Dispatcher
) -> None:
    dp.register_message_handler(
        select_mode,
        state=DashboardStates.input_query
    )
    dp.register_callback_query_handler(
        collect_result,
        Text(
            equals=[
                DashboardMenu.lost_things_callback,
                DashboardMenu.found_things_callback
            ]
        ),
        state=DashboardStates.input_query
    )
    dp.register_callback_query_handler(
        update_page,
        Text(
            equals=[
                DashboardMenu.previous_page_callback,
                DashboardMenu.next_page_callback
            ]
        ),
        state=DashboardStates.query_result
    )
    dp.register_callback_query_handler(
        update_page,
        Text(
            equals=DashboardMenu.backward_callback
        ),
        state=GetAnnouncementStates.preview
    )
    dp.register_callback_query_handler(
        signup.back_to_start_menu,
        Text(
            equals=YesOrNo.cancel_callback
        ),
        state=DashboardStates.input_query
    )
    dp.register_callback_query_handler(
        dashboard,
        Text(
            equals=DashboardMenu.another_query_callback
        ),
        state=DashboardStates.query_result
    )
    dp.register_callback_query_handler(
        get_announcement,
        Text(
            endswith=DashboardMenu.detail_callback
        ),
        state=DashboardStates.query_result
    )
