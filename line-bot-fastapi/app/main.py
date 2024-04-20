from fastapi import FastAPI, HTTPException, Request

from linebot.v3.webhook import WebhookParser
from linebot.v3.messaging import (
    AsyncApiClient,
    AsyncMessagingApi,
    Configuration,
    ReplyMessageRequest,
    TextMessage,
)
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
)

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

channel_secret = app_config.LINE_CHANNEL_SECRET
channel_access_token = app_config.LINE_TOKEN

configuration = Configuration(access_token=channel_access_token)

async_api_client = AsyncApiClient(configuration)
line_bot_api = AsyncMessagingApi(async_api_client)
parser = WebhookParser(channel_secret)


@app.get("/health")
async def health():
    return "ok"


@app.post("/line/events")
async def handle_callback(request: Request):
    signature = request.headers["X-Line-Signature"]

    body = await request.body()
    body = body.decode()

    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    for event in events:
        logging.info(event)
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessageContent):
            continue

        if event.message.text == "!ping":
            await line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="pong!")],
                )
            )
        else:
            await line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=event.message.text)],
                )
            )

    return "OK"
