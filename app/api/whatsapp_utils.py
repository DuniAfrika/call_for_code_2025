import os
import requests
import httpx  # Add this import
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


async def send_whatsapp_message(payload: dict):
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json',
    }

    # Use dictionary keys instead of attributes
    payload = {
        "messaging_product": "whatsapp",
        "to": payload["to"],  # Access the "to" key
        "text": {"body": payload["text"]["body"]}  # Access the "text" -> "body" key
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(URL, json=payload, headers=headers)

    if response.status_code == 200:
        return {"status": "success", "message": "Message sent"}
    else:
        raise HTTPException(status_code=response.status_code, detail=response.json())

   

async def receive_whatsapp_message(request: Request):
    try:
        body = await request.json()
        # Process the incoming message
        entry = body.get("entry", [])
        if entry:
            for item in entry:
                changes = item.get("changes", [])
                for change in changes:
                    messages = change.get("value", {}).get("messages", [])
                    for message in messages:
                        sender = message.get("from")
                        text = message.get("text", {}).get("body")
                        # Log or process the sender and message text
                        print(f"Message from {sender}: {text}")
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

