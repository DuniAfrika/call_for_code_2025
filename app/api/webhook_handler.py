"""
    Webhook handler
"""

from fastapi import APIRouter, Request
from api.whatsapp_utils import send_whatsapp_message


router = APIRouter()


@router.post("/send_whatsapp_message")
def webhook_handler(request:Request):
    response = send_whatsapp_message()
    return response

