def build_prompt(user_input: str, chat_history: list, memory: dict, rules: dict) -> str:
    history_text = "\n".join(
        [f"{msg.role}: {msg.content}" for msg in chat_history]
    )
    
    memory_text = "\n".join(
        [f"{key}: {value}" for key, value in memory.items()]
    ) if memory else "None"

    rules_text = "\n".join(
        [f"{key}: {value}" for key, value in rules.items()]
    ) if rules else "None"

    prompt = f"""
You are a helpful assistant.

Rules:
{rules_text}

Memory:
{memory_text}

Recent Chat:
{history_text}

User: {user_input}
Assistant:"""

    return prompt.strip()
