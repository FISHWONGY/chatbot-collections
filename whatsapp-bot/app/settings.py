from pydantic import BaseSettings
from gcp_secrets import GCPSecrets

secrets = GCPSecrets()


class AppConfig(BaseSettings):
    VERIFICATION_TOKEN: str = secrets.get_secret("whatsapp-token")
    ACCESS_TOKEN: str = secrets.get_secret("whatsapp-access-token")
    APP_ID: str = secrets.get_secret("whatsapp-app-id")
    APP_SECRET: str = secrets.get_secret("whatsapp-app-secret")
    RECIPIENT_WAID: str = secrets.get_secret("whatsapp-phone-number")
    PHONE_NUMBER_ID: str = secrets.get_secret("whatsapp-phone-id")

    WHATSAPP_API_VERSION = "v19.0"
    WHATSAPP_API_URL = "https://graph.facebook.com/v18.0/me/messages"


def get_config() -> AppConfig:
    return AppConfig()


app_config = get_config()
