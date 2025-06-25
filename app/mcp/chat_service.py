# chat_service.py
from redis_client import load_context, save_context

def handle_user_message(user_id: str, user_input: str):
    ctx = load_context(user_id)

    ctx.add_message("user", user_input)

    # Here you'd call your model and get a response
    bot_reply = "This is a dummy reply."

    ctx.add_message("assistant", bot_reply)

    save_context(user_id, ctx)

    return bot_reply
