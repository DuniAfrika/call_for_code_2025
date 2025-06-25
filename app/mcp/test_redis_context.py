from redis_client import save_context, load_context
from chat_context import ChatContext
from chat_context import Message  # Make sure to import Message

# Create a dummy context
user_id = "254700123456"
context = ChatContext(
    user_id=user_id,
    history=[
        Message(role="user", content="Hi"),
        Message(role="assistant", content="Hello!"),
        Message(role="user", content="How can I help you?")
    ]
)


# Save the context
save_context(user_id, context)
print("✅ Context saved to Redis.")

# Load the context
loaded_context = load_context(user_id)
print("🧠 Loaded Context:", loaded_context)
print("🔁 History:", [f"{m.role}: {m.content}" for m in loaded_context.history])
