from pydantic import BaseSettings
from gcp_secrets import GCPSecrets

secrets = GCPSecrets()


class AppConfig(BaseSettings):
    WEBEX_TOKEN: str = secrets.get_secret("webex-token")


def get_config() -> AppConfig:
    return AppConfig()


app_config = get_config()
