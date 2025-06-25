from prompt_builder import build_prompt
from chat_context import Message

# Dummy data
user_input = "What's my favorite color?"
history = [
    Message(role="user", content="Hi"),
    Message(role="assistant", content="Hello! How can I help?")
]
memory = {"favorite_color": "blue"}
rules = {"tone": "friendly", "keep replies under": "50 words"}

# Build prompt
prompt = build_prompt(user_input, history, memory, rules)
print(prompt)
