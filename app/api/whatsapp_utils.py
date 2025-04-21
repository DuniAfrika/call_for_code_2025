import os
import requests
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import PlainTextResponse 
from pydantic import BaseModel
from dotenv import load_dotenv
from app.db.models import WhatsAppWebhook

# VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
VERIFY_TOKEN = "secret_token"

async def verify_webhook(request: Request):
    params = request.query_params
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return PlainTextResponse(content=challenge, status_code=200)
    else:
        return PlainTextResponse(content="Verification failed", status_code=403)


"""
    - Send message
    - Recive message
    - Process message
    - verification
"""

load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
URL = os.getenv("URL")


async def send_whatsapp_message(payload: WhatsAppWebhook):

    headers ={
        'Authorization':f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json',
        }

    payload = {
            "messaging_product": "whatsapp",
            "to": payload.to,
            "text":{"body": payload.message}
            }

    response = requests.post(URL, json=payload, headers=headers)

    if response.status_code == 200:
        return {"status":"success", "message":"Message sent"}
    else:
        raise HTTPException(status_code = response.status_code, detail=response.json())

