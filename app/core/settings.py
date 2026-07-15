from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="IAM_", env_file=".env", env_file_encoding="utf-8"
    )

    DATABASE_URL: str = Field(env="DATABASE_URL")
    JWT_SECRET_KEY: str = Field(env="JWT_SECRET_KEY")
    JWT_ALGORITHM: str = Field(env="JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(env="ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(env="REFRESH_TOKEN_EXPIRE_DAYS")
    ENVIRONMENT: str = Field(env="ENVIRONMENT")


settings = Settings()