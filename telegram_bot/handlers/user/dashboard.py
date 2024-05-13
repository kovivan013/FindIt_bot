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
    YesOrNo
)
from states.states import (
    MainMenuStates,
    DashboardStates
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
        reply_markup=DashboardMenu.keyboard()
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

    if response._success:
        for i, announcement in response.data.announcements.as_dict().items():
            caption = f"{announcement.title}\n\n" \
                      f"" \
                      f"📍 *{announcement.location.place_name}*\n" \
                      f"⌚ *{utils.to_date(announcement.timestamp)}*"

            await event.message.answer_photo(
                photo=blob.get_preview(
                    announcement.announcement_id
                ),
                caption=caption,
                parse_mode="Markdown",
                disable_notification=True
            )


async def filters_menu(
        event: CallbackQuery,
        state: FSMContext
) -> None:
    pass

# class Filters:
#
#     async def


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