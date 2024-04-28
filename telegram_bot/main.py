from config import dp
from aiogram import executor


async def on_startup(_) -> None:
    print("Bot started!")

async def on_shutdown(_) -> None:
    print("Bot shutdown!")

def start_bot() -> None:
    executor.start_polling(
        dispatcher=dp,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown
    )

if __name__ == "__main__":
    start_bot()