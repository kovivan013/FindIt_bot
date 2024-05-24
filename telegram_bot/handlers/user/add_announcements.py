# хендлера для добавления объявления

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


async def announcement_mode(
        event: CallbackQuery,
        state: FSMContext
) -> None:
    pass

async def input_title(
        event: CallbackQuery,
        state: FSMContext
) -> None:
    pass

async def check_title(
        event: Message,
        state: FSMContext
) -> None:
    pass

async def input_description(
        event: Message,
        state: FSMContext
) -> None:
    pass

async def check_description(
        event: Message,
        state: FSMContext
) -> None:
    pass

async def input_photo(
        event: Message,
        state: FSMContext
) -> None:
    pass

async def check_photo(
        event: Message,
        state: FSMContext
) -> None:
    pass

async def input_location(
        event: Message,
        state: FSMContext
) -> None:
    pass

async def check_date(
        event: Message,
        state: FSMContext
) -> None:
    pass

async def input_date(
        event: Message,
        state: FSMContext
) -> None:
    pass

async def check_date(
        event: CallbackQuery,
        state: FSMContext
) -> None:
    pass

async def input_tags(
        event: CallbackQuery,
        state: FSMContext
) -> None:
    pass

# FUNCTIONS

async def check_tags(
        event: CallbackQuery,
        state: FSMContext
) -> None:
    pass

async def secret_question(
        event: CallbackQuery,
        state: FSMContext
) -> None:
    pass

async def check_question(
        event: Message,
        state: FSMContext
) -> None:
    pass

async def encrypted_answer(
        event: Message,
        state: FSMContext
) -> None:
    pass

async def check_answer(
        event: Message,
        state: FSMContext
) -> None:
    pass

async def check_payload(
        event: Message,
        state: FSMContext
) -> None:
    pass

async def create_request(
        event: CallbackQuery,
        state: FSMContext
) -> None:
    pass