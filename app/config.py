from pydantic_settings import BaseSettings,SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    # App
    APP_NAME: str
    APP_VERSION: str
    DEBUG: bool
    SECRET_KEY: str

    # PostgreSQL
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URL: str

    # Redis
    REDIS_URL: str

    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # File Upload
    MAX_FILE_SIZE_MB: int
    UPLOAD_DIR: str

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()