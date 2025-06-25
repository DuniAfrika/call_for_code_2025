from chat_context import ChatContext

# Create a new context
ctx = ChatContext(user_id="user123")

# Add a user message
ctx.add_message("user", "Hello, chatbot!")

# Add a bot response
ctx.add_message("assistant", "Hello, user!")

# Print recent history
print("\n--- Recent Chat History ---")
for msg in ctx.get_recent_history():
    print(f"{msg.role.capitalize()}: {msg.content}")

# Check memory usage
ctx.memory["favorite_color"] = "blue"
print("\n--- Memory ---")
print(ctx.memory)
