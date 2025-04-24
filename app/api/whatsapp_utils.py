"""WhatsApp utility file:
verify_webhook,
send_whatsapp_message,
process_whatsapp_message."""
import os
import requests
import httpx
from fastapi import (
        FastAPI,
        HTTPException,
        Request,
        )
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from app.db.models import WhatsAppWebhook
import json


load_dotenv()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
URL = os.getenv("URL")


async def verify_webhook(request: Request):
    """Handle webhook_verification by Meta Cloud API.

    Args:
        request: (Request) -HTTP Request.

    Return:
        PlainTextResponse:  (file)
        File Response from Meta Cloud API.
    """
    params = request.query_params
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return PlainTextResponse(
                content=challenge,
                status_code=200
                )
    else:
        return PlainTextResponse(
                content="Verification failed",
                status_code=403
                )


async def send_whatsapp_message(payload: dict):
    """Handle send WhatsApp message.

    Args:
        payload: (dict) -JSON input.

    Return:
        response:  (dict)
        JSON Response from Meta Cloud API.
    """
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json',
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": payload["to"],
        "text": {"body": payload["text"]["body"]}
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
                URL,
                json=payload,
                headers=headers
                )

    if response.status_code == 200:
        return {
                "status": "success",
                "message": "Message sent"
                }
    else:
        raise HTTPException(
                status_code=response.status_code,
                detail=response.json()
                )


async def process_whatsapp_message(request: Request) -> dict | None:
    """Parse an incoming WhatsApp message and generates a reply payload.

    Args:
        request (Request): Incoming HTTP request from WhatsApp.

    Returns:
        dict | None: Reply payload to be sent back via WhatsApp,
                     or None if no message needs to be sent.
    """
    body = await request.body()
    data = json.loads(body)

    try:
        entry = data['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        messages = value.get('messages', [])

        if messages:
            message = messages[0]
            sender = message['from']
            message_type = message['type']

            reply_template_for_text = (
                    "Thank you for your message!"
                    "We will get back to you shortly"
                    )

            reply_template_for_image = ("Thank you for sending the image!"
                                        "We will review it shorlty"
                                        )

            if message_type == "text":
                text = message['text']['body']
                print(f"📨 Text message from {sender}: {text}")
                return {
                    "to": sender,
                    "text": {"body": reply_template_for_text}
                }

            elif message_type == "image":
                caption = message['image'].get('caption', '')
                print(f"🖼️ Image from {sender} with caption: {caption}")
                return {
                    "to": sender,
                    "text": {"body": reply_template_for_image}
                }

            else:
                return {
                    "to": sender,
                    "text": {"body": (
                        "Sorry, we currently support"
                        "only text and image messages."
                        )}
                }

    except Exception as e:
        print("❌ Error processing message:", str(e))

    return None
