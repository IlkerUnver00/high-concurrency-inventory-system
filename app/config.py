from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/inventory"

    model_config = SettingsConfigDict(
        env_file=".env",
    )


settings = Settings()