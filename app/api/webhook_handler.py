"""
    Webhook handler
"""

from fastapi import APIRouter, Request
from app.api import send_whatsapp_message, verify_webhook
from app.db.models import WhatsAppWebhook


router = APIRouter()


@router.get("/webhook")
async def verify_webhook_handler(request: Request):
    response = await verify_webhook(request)
    return response

@router.post("/webhook")
async def webhook_handler(payload: WhatsAppWebhook):
    response = await send_whatsapp_message(payload)
    return response

