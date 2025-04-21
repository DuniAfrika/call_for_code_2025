import os
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv


"""
    - Send message
    - Recive message
    - Process message
    - verification
"""

load_dotenv()


class WhatsAppModel(BaseModel):
    to: str
    message: str

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
URL = os.getenv("URL")


async def send_whatsapp_message(msg: WhatsAppModel):

    headers ={
        'Authorization':f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json',
        }

    payload = {
            "messaging_product": "whatsapp",
            "to": msg.to,
            "text":{"body": msg.message}
            }

    response = requests.post(URL, json=payload, headers=headers)

    if response.status_code == 200:
        return {"status":"success", "message":"Message sent"}
    else:
         raise HTTPException(status_code = response.status_code, detail=response.json())
