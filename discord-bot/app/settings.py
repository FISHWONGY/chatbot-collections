from pydantic import BaseSettings
from gcp_secrets import GCPSecrets

secrets = GCPSecrets()


class AppConfig(BaseSettings):
    DISCORD_TOKEN: str = secrets.get_secret("discord-token")
    DC_SER_ID: str = secrets.get_secret("discord-server-id")


def get_config() -> AppConfig:
    return AppConfig()


app_config = get_config()
