"""Main File :Entry point of the app."""
from fastapi import FastAPI
from app.api import webhook_handler
from app.users.routes import router as users_router
from app.db.config import create_db_and_tables

app = FastAPI()
create_db_and_tables()

app.get("/")
def isAlive():
    return {"status": "server running"}

app.include_router(users_router)
app.include_router(webhook_handler.router, prefix="", tags=["webhook"])
