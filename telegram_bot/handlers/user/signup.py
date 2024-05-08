from typing import Union
from aiogram import Dispatcher
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardRemove,
    InputMedia,
    InputFile
)

from config import dp, bot
from common import dtos
from common.interfaces import DataStructure
from common.classes import ServicePhotos, Symbols, FSMActions
from classes.utils_classes import (
    FSMStorageProxy,
    MessageProxy
)
from classes.api_requests import UserAPI
from utils import utils
from keyboards.keyboards import (
    MainMenu
)
from states.states import (
    MainMenuStates
)
from common.schemas import BaseUser
from decorators.decorators import (
    check_registered,
    private_message
)


async def welcome(
        event: Message,
        state: FSMContext
) -> None:
    await MainMenuStates.welcome.set()
    await event.answer_photo(
        photo=utils.get_photo(
            ServicePhotos.LOGO
        ),
        caption="Реєстрація",
        reply_markup=MainMenu.welcome_keyboard()
    )

async def input_username(
        event: CallbackQuery,
        state: FSMContext
) -> None:
    await MainMenuStates.input_username.set()
    await event.message.delete()

    await FSMStorageProxy(state).update_data(
        FSMActions.APP_CONFIG,
        message=await event.message.answer_photo(
            photo=utils.get_photo(
                ServicePhotos.USERNAME
            ),
            caption="Уведіть ваш нікнейм"
        )
    )

async def check_username(
        event: Message,
        state: FSMContext
) -> None:
    storage = FSMStorageProxy(state)

    if len(event.text) <= 50:
        for i in event.text:
            if i not in Symbols.UKRAINIAN_ALPHABET + Symbols.ENGLISH_ALPHABET + " ":
                return await MessageProxy(state).edit_caption(
                    caption="У нікнеймі можна використовувати лише літери українського та англійського алфавітів"
                )
        else:
            return await input_description(
                event, state=state
            )

    return await MessageProxy(state).edit_caption(
        caption="Довжина нікнейму не повинна перевищувати 50 символів"
    )


async def input_description(
        event: Message,
        state: FSMContext
) -> None:
    await MainMenuStates.input_description.set()

    await FSMStorageProxy(state).update_data(
        FSMActions.APP_CONFIG,
        message=await event.message.answer_photo(
            photo=utils.get_photo(
                ServicePhotos.USERNAME
            ),
            caption="Уведіть ваш нікнейм"
        )
    )

async def check_description(
        event: Message,
        state: FSMContext
) -> None:
    pass

async def input_phone_number(
        event: Message,
        state: FSMContext
) -> None:
    pass

async def check_phone_number(
        event: Message,
        state: FSMContext
) -> None:
    pass

async def create_account(
        event: Message,
        state: FSMContext
) -> None:
    pass

async def banned_menu(
        event: Message,
        state: FSMContext
) -> None:
    await event.answer("banned menu")

async def back_to_start_menu(
        event: CallbackQuery,
        state: FSMContext
) -> None:
    await start_menu(
        event.message, state
    )

@check_registered()
@private_message
async def start_menu(
        event: Message,
        state: FSMContext
) -> None:
    await MainMenuStates.start_menu.set()
    user = await UserAPI.get_user(
        event.from_user.id,
        telegram_id=event.from_user.id
    )
    await event.answer_photo(
        photo=utils.get_photo(
            ServicePhotos.LOGO
        ),
        caption=f"👋 Вітаємо, {user.data.username}",
        reply_markup=MainMenu.keyboard()
    )


def register(
        dp: Dispatcher
) -> None:
    dp.register_message_handler(
        start_menu,
        commands=["start"]
    )
    dp.register_callback_query_handler(
        input_username,
        Text(
            equals=MainMenu.continue_work_callback
        ),
        state=MainMenuStates.welcome
    )
    dp.register_message_handler(
        check_username,
        state=MainMenuStates.input_username
    )