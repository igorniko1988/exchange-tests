from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_PATH = Path(__file__).parents[2] / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="EXCHANGE_TESTS_", env_file=ENV_PATH)
    BASE_URL: str = "http://localhost:8080"
    REQUEST_TIMEOUT: float = 10.00
    ADMIN_EMAIL: str = "admin@mini-exchange.io"
    ADMIN_PASSWORD: SecretStr = "admin-password"
