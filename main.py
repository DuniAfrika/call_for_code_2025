from fastapi import FastAPI
from app.api.webhook_handler import router as webhook_router

app = FastAPI()

@app.get("/")
def read_root():
    retrun {"Status":"OK"}


