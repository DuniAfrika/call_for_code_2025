"""
    Webhook handler
"""

from fastapi import APIRouter, Request
from app.api import send_whatsapp_message
from app.db.models import WhatsAppWebhook


router = APIRouter()


@router.post("/send_whatsapp_message")
async def webhook_handler(payload: WhatsAppWebhook):
    response = await send_whatsapp_message(payload)
    return response

