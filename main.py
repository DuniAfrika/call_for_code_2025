from fastapi import FastAPI
from app.api import webhook_handler

app = FastAPI()


app.include_router(webhook_handler.router, prefix="", tags=["webhook"])

