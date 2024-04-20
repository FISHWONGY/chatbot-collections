from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse, PlainTextResponse
import httpx

from settings import app_config

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

app = FastAPI()

SLACK_BOT_TOKEN = app_config.SLACK_BOT_TOKEN


@app.get("/health")
async def health():
    return "ok"


async def send_message_to_slack(channel_id, message):
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-type": "application/json",
    }
    payload = {"channel": channel_id, "text": message}
    async with httpx.AsyncClient() as client:
        await client.post(url, headers=headers, json=payload)


@app.post("/slack/events")
async def handle_events(request: Request):
    body = await request.json()

    if body.get("type") == "url_verification":
        return JSONResponse(
            content={"challenge": body.get("challenge")}, status_code=200
        )

    if body.get("type") == "event_callback":
        event = body.get("event", {})
        logger.info(f"Event: {event}")

        if (
            event.get("type") == "message"
            and "subtype" not in event
            and "bot_id" not in event
        ):
            channel_id = event.get("channel")
            message_text = event.get("text", "")
            user_id = event.get("user")

            logger.info(
                f"Channel ID: {channel_id}\nMessage Text: {message_text}\nUser ID: {user_id}"
            )

            if message_text.strip() == "!ping":
                await send_message_to_slack(channel_id, "pong!")
            else:
                await send_message_to_slack(
                    channel_id, f"{user_id} said: {message_text}"
                )

            return Response(status_code=200)

    return JSONResponse(content={}, status_code=200)
