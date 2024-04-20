from settings import app_config

from fastapi import FastAPI, Request
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler

from os import getenv
import google.cloud.logging
import logging


if (env := getenv("ENV")) and env == "prod":
    client = google.cloud.logging.Client()
    client.setup_logging()

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] {%(filename)s:%(lineno)d} %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)


slack_app = App(
    token=app_config.SLACK_BOT_TOKEN,
    signing_secret=app_config.SLACK_SIGNING_SECRET,
)

handler = SlackRequestHandler(slack_app)

app = FastAPI()


@slack_app.event("message")
def handle_message_events(body, say, logger):
    logger.info(body)
    event = body.get("event", {})

    if "bot_id" in event:
        return

    text = event.get("text", "").strip()
    user_id = event.get("user")

    if text == "!ping":
        say("pong!")
    else:
        say(f"<@{user_id}> said: {text}")


@app.post("/slack/events")
async def endpoint(req: Request):
    return await handler.handle(req)


@app.get("/health")
async def health():
    return "ok"
