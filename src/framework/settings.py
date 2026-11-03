from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV = Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV, env_prefix="EXCHANGE_TESTS_")
    BASE_URL: str = "http://localhost:8080"
    REQUEST_TIMEOUT: float = 10
    ADMIN_EMAIL: str = "admin@mini-exchange.io"
    ADMIN_PASSWORD: SecretStr = "admin-password"
