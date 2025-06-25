from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ChatRequest(BaseModel):
    user_id: str
    message: str

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    return {"response": f"You said: {request.message}"}
