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
    SECRET_KEY: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str

    # BOT_TOKEN: str = "6225987952:AAHVW2HXVngsAmMuQLco0sVanOabpYaRnWU"
    # SECRET_KEY: str = "MIIEpAIBAAKCAQEArzIbpW1Z8otAXNtFAkdWuvGxzOETuz4YXh3m4Q1dwIF5Dms5zWy9b0O3m05wfc6sAxbc/lAT0YrSsqxohyDVPX7GAfua/55fgBMxevPnpoDry2HZtNH5g0Ef7mlP3f0Vijyzz1rxLKHC9k+1iTX7wnEwBf0xDUi4zCM8rBW8XgvUlxt/jBjaCBiGSS91Jb519mTdQUtNYwG5skTqTRQkupCCqsa4Is4DPguMlTI698miDFNoQ3QVyV7Qichq6aBDggQanIQEXuWn09yVWsxHQNU5Krd3udq6lQ3oqxzJJsqBRv+Frr2qAyKjA7bqEby80IgTZVWN7aMnLU6fOMH+mQIDAQABAoIBAQCC/8jETZvwTEd4J0zWg1lKt+bm93W1kJzP4zP8G+56P1WxfmPeQuzzAYOM0X4z1BGyzam5T09CY7dgeqI+SEKqlNyiJuyjLlzie3eIJFCWo9esYCJVnpwflNa3gm+B4ff1QaaB6dJkOSB65OctDfyOS+xIziWbdUEZA1AerLII7zjiW/KVyqJUrT8qxT0nnlU7+AZqyfFpO0r5CMJGAHQEw2wTB3UUPQk+HQvHFb5tb9oP7IsNzrfjYuFBCim1wZ75LLnFe2e3mfDs9qbqBEYdP4og//adl1ogCeFpYQFZXR0Wq+z9KHGYUZZvJbUqtydDvi/NhFGWmK2BePne5UYxAoGBAO1wAwDjkeB+pzotJYoDgl91qeXvsna7+UorgBCYPsmEbAjhTsl79RB5XOhDWHHSHnc66m1suqRfCbLjY0yqISRNkTRnDloSy1AQqe8zQfUPjjiD8uumXwLxB/lEUXPP4Ldp8H2QMkepSGMDXOxM1HcxLJAauOCM/80aWZvkfnZzAoGBALzkaVEIXzq8nqSa5dS/1kGJgAwN1B6/tS8Up+moHT/vfsOZw8j6NmN8tBtYFzvUfuQFzeSn0u13Jfh0f27dv1UPkYnmBt31P9lN2MEGBudiP+FTPAixeDVQYB2mGOgqRBbeCRlVCM9c3amgys768X9tYw8MEaNlDmcfe1vDROfDAoGAA3lzIc0yskVILyq/9OAORVVUch/qzZ/8iuBOFHAV4x8D8bFSVNJyiJYuDNwHbEr11SrQiV9g78zQOITpTBLlP0G/UTP82saRoQ9NXUmzumFK5HrR0C70Dvf19OjSBE7Ta/up4Dx+79uDSqee8XpCVagrjcRGVkrZ52duTkCutQ8CgYEAnNYN9+E6qJtaIZQXRnluHYZcUiXdPRayCoBdFu2mM6LYHvJ6FFJkfGBbbuTKjbvXC98h4DvUL6UhWtTnxhbKOYcusU/T3dE3DWfMlCA79Tyni6A/lXw9Mg8lbxitT39gf5gl9+mZ4graZXCDVC4Z/FLH0AOWVZOfzNHf7AYLHV8CgYAfSxp3XeZXDW5Ad9ieYXOBQKdRMPlbpYttK40mRkb1AHeJ8N+qkN47/qDFneEKeozU0bmZ+w2lQSH5qokB00l1p79+BTl1KAefyvnnRPrZegiACAmPmjnhn1yP63mESW1BvMtDHKjuxTXmnBTyyNXZp67wonpQOmtlzliQBbaPdg=="
    BASE_API_URL: str = "http://127.0.0.1:8000"
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
