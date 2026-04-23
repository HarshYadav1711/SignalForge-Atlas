from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "SignalForge Atlas"
    environment: Literal["development", "staging", "production"] = "development"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    log_file: str = "logs/system.log"
    request_timeout_seconds: int = 12
    request_retry_attempts: int = 3
    binance_kline_limit: int = 500
    openrouter_api_key: str = ""
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_model: str = "meta-llama/llama-3.2-3b-instruct:free"


@lru_cache(maxsize=1)
def get_settings() -> AppSettings:
    return AppSettings()
