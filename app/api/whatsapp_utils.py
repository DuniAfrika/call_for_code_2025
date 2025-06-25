import os
import requests
import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from app.db import WhatsAppWebhook
from app.services import process_nlp, process_image
from app.mcp.redis_client import load_context, save_context
import json

load_dotenv()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
URL = os.getenv("URL")


async def verify_webhook(request: Request):
    """Handle webhook_verification by Meta Cloud API."""
    try:
        params = request.query_params
        mode = params.get("hub.mode")
        token = params.get("hub.verify_token")
        challenge = params.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return PlainTextResponse(content=challenge, status_code=200)
        else:
            return PlainTextResponse(content="Verification failed", status_code=403)
    except Exception as e:
        print("Error Verifying Webhook", {e})
        return HTTPException(status_code=500, detail="Internal Server Error")


async def send_whatsapp_message(payload: dict):
    """Handle send WhatsApp message."""
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json',
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": payload["to"],
        "text": {"body": payload["text"]["body"]}
    }
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(URL, json=payload, headers=headers)
        response.raise_for_status()

        return {"status": "success", "message": "Message sent"}

    except httpx.ConnectTimeout:
        print("ERROR: Could not connect to WhatsApp API")
        return {"status": "Connection Timeout. Please Retry"}

    except httpx.HTTPStatusError as e:
        print("HTTP Error:", e.response.status_code, e.response.json())
        return HTTPException(status_code=e.response.status_code, detail=e.response.json())

    except Exception as e:
        print("Unknown Error Occurred", str(e))
        return HTTPException(status_code=500, detail="Internal Server Error")


def download_whatsapp_image(media_id: str, save_path: str) -> str:
    """Download WhatsApp image locally."""
    try:
        # Step 1: Get media URL
        media_info_url = f"https://graph.facebook.com/v19.0/{media_id}"
        headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
        media_info_response = requests.get(media_info_url, headers=headers)
        media_info_response.raise_for_status()
        media_url = media_info_response.json().get('url')

        # Step 2: Download the image
        download_response = requests.get(media_url, headers=headers)
        download_response.raise_for_status()

        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "wb") as f:
            f.write(download_response.content)

        return save_path

    except Exception as e:
        print(f"❌ Failed to download image: {str(e)}")
        raise


async def process_whatsapp_message(request: Request) -> dict | None:
    """Parse an incoming WhatsApp message and generate a reply payload."""
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
            
            # Load existing chat context or initialize
            context = await load_context(sender)

            if message_type == "text":
                text = message['text']['body']
                reply_template_for_text = process_nlp(text)

                print(f"📨 Text message from {sender}: {text}")
                # Add user message to history
                context.add_message("user", text)
                # Generate assistant response using context
                response_text = await process_nlp(context)
                # Add assistant reply to context
                context.add_message("assistant", response_text)
                # Save updated context to Redis
                await save_context(sender, context)
                return {
                    "to": sender,
                    "text": {"body": reply_template_for_text}
                    # If message sending fails in future, consider adding:
# "type": "text" and "messaging_product": "whatsapp"
                }

            elif message_type == "image":
                caption = message['image'].get('caption', '')
                media_id = message['image']['id']

                print(f"🖼️ Image from {sender} with caption: {caption}")

                # Download image to local storage
                save_path = f"data/{media_id}.jpg"
                try:
                    downloaded_image_path = download_whatsapp_image(media_id, save_path)
                    print(f"✅ Image downloaded to {downloaded_image_path}")
                except Exception as e:
                    print("❌ Image download failed:", str(e))

                result = process_image(save_path)
                reply_template_for_image = result["choices"][0]["message"]["content"]

                 # Add user message to history
                context.add_message("user", f"[Image with caption: {caption}]")
                
                 # Add assistant reply to context
                context.add_message("assistant", reply_template_for_image)
                
                 # Save updated context
                await save_context(sender, context)

                return {
                    "to": sender,
                    "text": {"body": reply_template_for_image}
                }

            else:
                return {
                    "to": sender,
                    "text": {"body": (
                        "Sorry, we currently support "
                        "only text and image messages."
                    )}
                }

    except Exception as e:
        print("❌ Error processing message:", str(e))

    return None
