"""
    Webhook handler
"""

from fastapi import APIRouter, Request
from app.api import send_whatsapp_message, verify_webhook, receive_whatsapp_message
from app.db.models import WhatsAppWebhook
import json

router = APIRouter()


@router.get("/webhook")
async def verify_webhook_handler(request: Request):
    """
    Handle WhatsApp webhook verification.
    """
    response = await verify_webhook(request)
    return response

@router.post("/webhook")
async def receive_message(request: Request):
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

            if message_type == "text":
                text = message['text']['body']
                print(f"📨 Text message from {sender}: {text}")

                # Prepare reply for text message
                reply_payload = {
                    "to": sender,
                    "text": {"body": "Thank you for your message! We will get back to you shortly."}
                }

            elif message_type == "image":
                image_id = message['image']['id']
                caption = message['image'].get('caption', '')
                print(f"🖼️ Image received from {sender} with caption: {caption}")

                # Prepare reply for image message
                reply_payload = {
                    "to": sender,
                    "text": {"body": "Thank you for sending the image! We will review it shortly."}
                }

            else:
                print(f"⚠️ Unsupported message type from {sender}: {message_type}")
                reply_payload = {
                    "to": sender,
                    "text": {"body": "Sorry, we currently support only text and image messages."}
                }

            # Send the reply
            response = await send_whatsapp_message(reply_payload)
            print("✅ Response sent:", response)

    except Exception as e:
        print("❌ Error processing message:", str(e))

    return {"status": "received"}



@router.post("/webhook/send")
async def send_whatsapp_message_handler(payload: dict):
    """
    Handle sending WhatsApp messages.
    """
    response = await send_whatsapp_message(payload)
    return response





