from fastapi import FastAPI
from app.api import webhook_handler

app = FastAPI()

@app.get("/")
def read_root():
    return {"Status":"OK"}

app.include_router(webhook_handler.router, prefix="/webhook")
