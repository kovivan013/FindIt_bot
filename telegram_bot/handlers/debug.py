from aiogram import Dispatcher
from aiogram.types import Message, ContentTypes
from aiogram.dispatcher.storage import FSMContext


async def debug_handler(
        event: Message,
        state: FSMContext
) -> None:
    await event.delete()

def register(
        dp: Dispatcher
) -> None:
    dp.register_message_handler(
        debug_handler,
        content_types=ContentTypes.ANY,
        state=["*"]
    )
