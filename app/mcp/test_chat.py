from chat_service import handle_user_message
from redis_client import load_context

# Step 1: Send a message and get a reply
reply = handle_user_message("user123", "Hi, who are you?")
print("Bot Reply:", reply)

# Step 2: Load the context and print the chat history
ctx = load_context("user123")
print("\nChat History:")
for msg in ctx.get_recent_history():
    print(f"{msg.role}: {msg.content}")
