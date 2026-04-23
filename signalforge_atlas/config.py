from functools import lru_cache
from typing import Literal

from pydantic import Field, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    environment: Literal["development", "staging", "production"] = "development"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"

    openrouter_api_key: str = Field(default="")
    openrouter_base_url: HttpUrl = Field(default="https://openrouter.ai/api/v1")
    openrouter_model: str = Field(default="meta-llama/llama-3.2-3b-instruct:free")

    enable_apify: bool = False
    apify_api_token: str = ""


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
