# redis_client.py
import redis
from chat_context import ChatContext

redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

def save_context(user_id: str, context: ChatContext):
    redis_client.set(user_id, context.json())

def load_context(user_id: str) -> ChatContext:
    data = redis_client.get(user_id)
    if data:
        return ChatContext.parse_raw(data)
    return ChatContext(user_id=user_id)
