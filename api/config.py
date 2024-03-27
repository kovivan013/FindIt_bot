from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

    uri: str = "postgresql+asyncpg://{}:{}@{}:{}/{}"
    name: str
    host: str
    port: int
    user: str
    password: str

    SERVER_HOST: str = "127.0.0.1"
    SERVER_PORT: int = 8000

    @property
    def url(self) -> str:
        return self.uri.format(
            self.user,
            self.password,
            self.host,
            self.port,
            self.name
        )

settings = Settings()

