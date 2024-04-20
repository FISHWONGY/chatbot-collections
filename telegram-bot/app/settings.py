from pydantic import BaseSettings
from gcp_secrets import GCPSecrets

secrets = GCPSecrets()


class AppConfig(BaseSettings):
    TELEGRAM_TOKEN: str = secrets.get_secret("telegram-token")


def get_config() -> AppConfig:
    return AppConfig()


app_config = get_config()
