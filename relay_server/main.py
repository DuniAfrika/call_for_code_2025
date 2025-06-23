"""
Listen for incoming webhook requests from Meta on a fixed public URL (e.g., via your ngrok tunnel).

Accept and parse the webhook payload (usually JSON).

Read a list of target URLs (from an .env file or config) — these include:

    Your local server (http://localhost:3000/webhook)

    Your teammates’ ngrok URLs (https://friend1.ngrok.io/webhook, etc.)

Forward the same webhook payload to each URL in the list.

Send proper HTTP headers (e.g., Content-Type: application/json) when forwarding.

Log the success/failure of each forwarding attempt.

Respond 200 OK to Meta regardless of downstream success (to avoid retries).

(Optional) Allow dynamic updates to the list of forwarding targets (via API or config reload).

(Optional) Validate or sign requests (e.g., verify Meta webhook signature).

(Optional) Store logs or payloads for replay/debugging later.
"""

import requests

host_ngrok_tunnel = "https://expert-cod-rarely.ngrok-free.app"

target_hosts = "http://127.0.0.0:8000/webhook, {NGROk_1}, {NGROK 2},..."

result = request.get(host_ngrok_url)

result.headers['content-type]



