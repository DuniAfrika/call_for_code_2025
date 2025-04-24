"""Webhook handler file for WhatsApp utility."""
from fastapi import APIRouter, Request
# from app.api import send_whatsapp_message, verify_webhook, process_whatsapp_message
import app.api as WhatsAppUtil
from app.db.models import WhatsAppWebhook
import json


router = APIRouter()


@router.get("/webhook")
async def verify_webhook_handler(request: Request):
    """Handle WhatsApp webhook verification.

    Args:
        request: (Request) - Incoming HTTP Request Object.

    Return:
        response: (dict) - JSON response from the whatsApp utility service.
    """
    response = await WhatsAppUtil.verify_webhook(request)
    return response


@router.post("/webhook")
async def receive_message(request: Request):
    """Receives a message from WhatsApp and responds accordingly.

    Args:
        request (Request): Incoming HTTP request object from WhatsApp.

    Returns:
        dict: A status message indicating receipt.
    """
    reply_payload = await WhatsAppUtil.process_whatsapp_message(request)

    if reply_payload:
        response = await WhatsAppUtil.send_whatsapp_message(reply_payload)
        print("✅ Response sent:", response)

    return {"status": "received"}


@router.post("/webhook/send")
async def send_whatsapp_message_handler(payload: dict):
    """Handle Send WhatsApp messages.

    Args:
        payload: (dict) - JSON Payload with WhatsApp information.

    Return:
        response: (dict) - JSON response from the whatsApp utility service.
    """
    response = await WhatsAppUtil.send_whatsapp_message(payload)
    return response
