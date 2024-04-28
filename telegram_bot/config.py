from pydantic_settings import BaseSettings, SettingsConfigDict
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Dispatcher, Bot


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

    BOT_TOKEN: str
    BASE_API_URL: str = "http://bot_api:8000"
    HELPERS_CHAT: int = -4186817944

settings = Settings()
storage = MemoryStorage()

bot = Bot(
    token=settings.BOT_TOKEN
)
dp = Dispatcher(
    bot=bot,
    storage=storage
)
