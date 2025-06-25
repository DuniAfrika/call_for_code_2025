from pydantic import BaseModel
from typing import List, Dict, Any

class Message(BaseModel):
    role: str  # 'user' or 'assistant'
    content: str

class ChatContext(BaseModel):
    user_id: str
    history: List[Message] = []
    memory: Dict[str, Any] = {}

    def add_message(self, role: str, content: str):
        self.history.append(Message(role=role, content=content))

    def clear_history(self):
        self.history = []

    def get_recent_history(self, limit: int = 5) -> List[Message]:
        return self.history[-limit:]
