from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class ADKModel(BaseModel):
    genai_use_vertexai: str
    api_key: SecretStr


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_nested_delimiter="__"
    )

    google: ADKModel


settings = Settings()
