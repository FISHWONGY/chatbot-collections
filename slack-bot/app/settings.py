from pydantic import BaseSettings
from gcp_secrets import GCPSecrets

secrets = GCPSecrets()


class AppConfig(BaseSettings):
    SLACK_BOT_TOKEN: str = secrets.get_secret("slack-bot-token")
    SLACK_SIGNING_SECRET: str = secrets.get_secret("slack-signing-secret")


def get_config() -> AppConfig:
    return AppConfig()


app_config = get_config()
