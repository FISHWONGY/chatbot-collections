from webex_bot.webex_bot import WebexBot

from commands import *
from settings import app_config
from os import getenv
import logging
import google.cloud.logging

if (env := getenv("ENV")) and env == "prod":
    client = google.cloud.logging.Client()
    client.setup_logging()

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] {%(filename)s:%(lineno)d} %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)

bot = WebexBot(app_config.WEBEX_TOKEN, approved_users=["user@email.com"])

bot.add_command(Ping())


if __name__ == "__main__":
    bot.run()
