"""Main File :Entry point of the app."""

from fastapi import FastAPI
from app.api import webhook_handler

app = FastAPI()
app.get("/")
def isAlive():
    return {"status": "server running"}
app.include_router(webhook_handler.router, prefix="", tags=["webhook"])
