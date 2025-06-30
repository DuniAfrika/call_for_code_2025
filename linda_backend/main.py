"""Main File :Entry point of the app."""
from fastapi import FastAPI
from app.api import webhook_handler
from app.users.routes import router as users_router
from app.db.config import create_db_and_tables

app = FastAPI()
create_db_and_tables()

app.include_router(users_router)
def main():
    return {"server_status":"Running"}


app.include_router(webhook_handler.router, prefix="", tags=["webhook"])
