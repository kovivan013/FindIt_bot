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
from classes.api_requests import OpenStreetMapAPI,  UserAPI
from utils import utils
from keyboards.keyboards import (
    AddAnnouncementMenu
)
from states.states import (
    AddAnnouncementStates
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
    await AddAnnouncementStates.select_mode.set()
    await MessageProxy(state).clear_deletion_list()
    await MessageProxy(state).edit_media(
        media=InputMedia(
            media=utils.get_photo(
                ServicePhotos.LOGO
            ),
            caption="*Для чого Ви розміщуєте оголошення?*",
            parse_mode="Markdown"
        ),
        reply_markup=AddAnnouncementMenu.keyboard()
    )


async def input_title(
        event: CallbackQuery,
        state: FSMContext
) -> None:
    await AddAnnouncementStates.input_title.set()
    return await MessageProxy(state).edit_media(
        media=InputMedia(
            media=utils.get_photo(
                ServicePhotos.NAME
            ),
            caption="*Уведіть назву оголошення*, це може бути назва самої речі, або її найкоротший опис.",
            parse_mode="Markdown"
        ),
        reply_markup=AddAnnouncementMenu.cancel_inline_keyboard()
    )

async def check_title(
        event: Message,
        state: FSMContext
) -> None:
    await event.delete()
    storage = FSMStorageProxy(state)
    title = utils.TextFilter(event.text)

    if title._max_lenght(50):
        if title._not_in(Symbols.MAIN_SYMBOLS):
            return await MessageProxy(state).edit_caption(
                caption="В назві можна використовувати лише літери українського та англійського алфавітів."
            )
        else:
            await storage.update_data(
                FSMActions.ADD_ANNOUNCEMENT,
                title=event.text
            )
            return await input_description(
                event, state=state
            )

    return await MessageProxy(state).edit_caption(
        caption="Довжина назви не повинна перевищувати 50 символів."
    )

async def input_description(
        event: Message,
        state: FSMContext
) -> None:
    await AddAnnouncementStates.input_description.set()
    return await MessageProxy(state).edit_media(
        media=InputMedia(
            media=utils.get_photo(
                ServicePhotos.DESCRIPTION
            ),
            caption="*Уведіть опис оголошення*, аби користувачі детальніше дізналися про цю річ.",
            parse_mode="Markdown"
        ),
        reply_markup=AddAnnouncementMenu.cancel_inline_keyboard()
    )

async def check_description(
        event: Message,
        state: FSMContext
) -> None:
    await event.delete()
    storage = FSMStorageProxy(state)
    title = utils.TextFilter(event.text)

    if title._max_lenght(512):
        if title._not_in(Symbols.MAIN_SYMBOLS):
            return await MessageProxy(state).edit_caption(
                caption="В описі можна використовувати лише літери українського та англійського алфавітів."
            )
        else:
            await storage.update_data(
                FSMActions.ADD_ANNOUNCEMENT,
                description=event.text
            )
            return await input_photo(
                event, state=state
            )

    return await MessageProxy(state).edit_caption(
        caption="Довжина опису не повинна перевищувати 512 символів."
    )

async def input_photo(
        event: Message,
        state: FSMContext
) -> None:
    await AddAnnouncementStates.input_photo.set()
    return await MessageProxy(state).edit_media(
        media=InputMedia(
            media=utils.get_photo(
                ServicePhotos.PHOTO
            ),
            caption="*Відправте фото речі* для кращого розпізнання.",
            parse_mode="Markdown"
        ),
        reply_markup=AddAnnouncementMenu.cancel_inline_keyboard()
    )

async def check_photo(
        event: Message,
        state: FSMContext
) -> None:
    await event.delete()
    storage = FSMStorageProxy(state)
    await storage.update_data(
        FSMActions.ADD_ANNOUNCEMENT,
        photo_id=event.photo[-1].file_id
    )
    await input_location(
        event, state=state
    )

async def input_location(
        event: Message,
        state: FSMContext
) -> None:
    await AddAnnouncementStates.input_location.set()
    return await MessageProxy(state).edit_media(
        media=InputMedia(
            media=utils.get_photo(
                ServicePhotos.LOCATION
            ),
            caption="*Відправте локацію*, де була знайдена / загублена (обновить) річ.",
            parse_mode="Markdown"
        ),
        reply_markup=AddAnnouncementMenu.cancel_inline_keyboard()
    )

async def check_location(
        event: Message,
        state: FSMContext
) -> None:
    storage = FSMStorageProxy(state)
    response = await OpenStreetMapAPI.get_address(
        latitude=event.location.latitude,
        longitude=event.location.longitude
    )

    await storage.update_data(
        FSMActions.ADD_ANNOUNCEMENT,
        address=response
    )
    await storage.update_data(
        FSMActions.ADD_ANNOUNCEMENT + "/location",
        latitude=event.location.latitude,
        longitude=event.location.longitude,
        **utils.collect_place(
            response
        )
    )

    await input_date(
        event, state=state
    )

async def input_date(
        event: Message,
        state: FSMContext
) -> None:
    await AddAnnouncementStates.input_date.set()
    return await MessageProxy(state).edit_media(
        media=InputMedia(
            media=utils.get_photo(
                ServicePhotos.DATE
            ),
            caption="*Оберіть дату*, коли знайдена / загублена (обновить) річ.",
            parse_mode="Markdown"
        ),
        reply_markup=AddAnnouncementMenu.cancel_inline_keyboard()
    )

async def check_date(
        event: CallbackQuery,
        state: FSMContext
) -> None:
    storage = FSMStorageProxy(state)

async def input_tags(
        event: CallbackQuery,
        state: FSMContext
) -> None:
    await AddAnnouncementStates.input_tags.set()
    return await MessageProxy(state).edit_media(
        media=InputMedia(
            media=utils.get_photo(
                ServicePhotos.DATE
            ),
            caption="*Уведіть теги оголошення* для більш релевантного пошуку.",
            parse_mode="Markdown"
        ),
        reply_markup=AddAnnouncementMenu.cancel_inline_keyboard()
    )

async def add_tag(
        event: Message,
        state: FSMContext
) -> None:
    storage = FSMStorageProxy(state)

async def remove_tag(
        event: CallbackQuery,
        state: FSMContext
) -> None:
    storage = FSMStorageProxy(state)

async def check_tags(
        event: CallbackQuery,
        state: FSMContext
) -> None:
    storage = FSMStorageProxy(state)

async def secret_question(
        event: CallbackQuery,
        state: FSMContext
) -> None:
    await AddAnnouncementStates.secret_question.set()
    return await MessageProxy(state).edit_media(
        media=InputMedia(
            media=utils.get_photo(
                ServicePhotos.DATE
            ),
            caption="*Уведіть секретне запитання* для захисту від шахраїв.",
            parse_mode="Markdown"
        ),
        reply_markup=AddAnnouncementMenu.cancel_inline_keyboard()
    )

async def check_question(
        event: Message,
        state: FSMContext
) -> None:
    storage = FSMStorageProxy(state)

async def encrypted_answer(
        event: Message,
        state: FSMContext
) -> None:
    await AddAnnouncementStates.encrypted_answer.set()
    return await MessageProxy(state).edit_media(
        media=InputMedia(
            media=utils.get_photo(
                ServicePhotos.DATE
            ),
            caption="*Уведіть відповідь* на секретне запитання.",
            parse_mode="Markdown"
        ),
        reply_markup=AddAnnouncementMenu.cancel_inline_keyboard()
    )

async def check_answer(
        event: Message,
        state: FSMContext
) -> None:
    # не шифровать ответ до проверки пользователем.
    storage = FSMStorageProxy(state)

async def check_payload(
        event: Message,
        state: FSMContext
) -> None:
    pass

async def create_request(
        event: CallbackQuery,
        state: FSMContext
) -> None:
    # TODO: зашифровать данные
    pass


def register(
        dp: Dispatcher
) -> None:
    dp.register_callback_query_handler(
        input_title,
        Text(
            equals=[
                AddAnnouncementMenu.lost_callback,
                AddAnnouncementMenu.found_callback
            ]
        ),
        state=AddAnnouncementStates.select_mode
    )
    dp.register_message_handler(
        check_title,
        state=AddAnnouncementStates.input_title
    )
    dp.register_message_handler(
        check_description,
        state=AddAnnouncementStates.input_description
    )
    dp.register_message_handler(
        check_photo,
        content_types=ContentTypes.PHOTO,
        state=AddAnnouncementStates.input_photo
    )
    dp.register_message_handler(
        check_location,
        content_types=ContentTypes.LOCATION,
        state=AddAnnouncementStates.input_location
    )
