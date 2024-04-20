import logging
import requests
import json
from settings import app_config


logger = logging.getLogger(__name__)


class Whatsapp:
    def __init__(self) -> None:
        self.ACCESS_TOKEN = app_config.ACCESS_TOKEN
        self.VERSION = app_config.WHATSAPP_API_VERSION
        self.PHONE_NUMBER_ID = app_config.PHONE_NUMBER_ID

    @staticmethod
    def log_http_response(response):
        logger.info(f"Status: {response.status_code}")
        logger.info(f"Content-type: {response.headers.get('content-type')}")
        logger.info(f"Body: {response.text}")

    def send_message(self, data):
        headers = {
            "Content-type": "application/json",
            "Authorization": f"Bearer {self.ACCESS_TOKEN}",
        }

        url = (
            f"https://graph.facebook.com/{self.VERSION}/{self.PHONE_NUMBER_ID}/messages"
        )

        response = requests.post(url, data=data, headers=headers)
        self.log_http_response(response)

    @staticmethod
    def get_text_message_input(recipient, text):
        return json.dumps(
            {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": recipient,
                "type": "text",
                "text": {"preview_url": False, "body": text},
            }
        )

    @staticmethod
    def is_valid_whatsapp_message(body):
        return body.get("object") == "whatsapp_business_account" and any(
            "messages" in change.get("value", {})
            for entry in body.get("entry", [])
            for change in entry.get("changes", [])
        )

    def process_whatsapp_message(self, body):
        wa_id = body["entry"][0]["changes"][0]["value"]["contacts"][0]["wa_id"]
        message = body["entry"][0]["changes"][0]["value"]["messages"][0]
        message_body = message["text"]["body"]

        logger.info(
            f"Logs from process_whatsapp_message:"
            f"\nBody:{body}\nWA ID:{wa_id}\nMessage:{message}\nMessage:{message_body}"
        )

        if message_body.strip() == "!ping":
            response = "pong!"
        else:
            response = message_body.strip()

        data = self.get_text_message_input(wa_id, response)
        self.send_message(data)
