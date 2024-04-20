from settings import app_config
from helpers.whatsappapi import Whatsapp

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

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


whatsappapi = Whatsapp()

VERIFICATION_TOKEN = app_config.VERIFICATION_TOKEN
WHATSAPP_TOKEN = app_config.ACCESS_TOKEN
WHATSAPP_API_URL = app_config.WHATSAPP_API_URL


@app.get("/health")
async def health():
    return "ok"


@app.get("/whatsapp/events")
async def verify(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    logger.info(f"Mode: {mode}\nToken: {token}\nChallenge: {challenge}")

    if mode == "subscribe" and token == VERIFICATION_TOKEN:
        return JSONResponse(content=int(challenge))
    else:
        raise HTTPException(status_code=403, detail="Verification token mismatch")


@app.post("/whatsapp/events")
async def webhook(request: Request):
    body = await request.json()
    logger.info(f"Logs from webhook\nBody received: {body}")
    if whatsappapi.is_valid_whatsapp_message(body):
        whatsappapi.process_whatsapp_message(body)
    return JSONResponse(content={"status": "received"})
