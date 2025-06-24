"""
Relay Servers For Meta  Callback URL
"""
import asyncio
import requests as re


"""
1. Receive callback from META"i
2. Send Payload to Target Tunnels
"""

global HOST_NGROK
HOST_NGROK = "https://expert-cod-rarely.ngrok-free.app"

global TARGET_TUNNELS
TARGET_TUNNELS = ["http://127.0.0.0:8000", "NGROK_2", "NGROK_2"]

def receive_callback():
    response = re.get(HOST_NGROK)
    if response.status_code == 200:
        return response.text
    else:
        return response.status_code

def parse_payload(Payload):
    response = re.post(TARGET_TUNNELS, data = {Payload})
    return response.status_code

async def main():
    callback_payload = receive_callback()
    _payload = parse_payload(callback_payload)

if __name__ == '__main__':
    asyncio.run(main())
