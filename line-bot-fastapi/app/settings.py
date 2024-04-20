from pydantic_settings import BaseSettings
from gcp_secrets import GCPSecrets

secrets = GCPSecrets()


class AppConfig(BaseSettings):
    LINE_TOKEN: str = secrets.get_secret("line-token")
    LINE_CHANNEL_SECRET: str = secrets.get_secret("line-channel-secret")


def get_config() -> AppConfig:
    return AppConfig()


app_config = get_config()
