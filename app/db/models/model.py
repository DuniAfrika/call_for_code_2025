from pydantic import BaseModel


class WhatsAppWebhook(BaseModel):
    to: str
    message: str
