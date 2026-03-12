import os

from fastapi import FastAPI

from .structs import ServerInfo
from .utils import prints

WORKER_HOST = os.getenv("WORKER_HOST", "localhost")
WORKER_PORT = os.getenv("WORKER_PORT", "8001")
WORKER_URL = f"http://{WORKER_HOST}:{WORKER_PORT}/"

app = FastAPI()

REGISTERED_MEDIA_SERVICE: ServerInfo | None = None

@app.get("/health")
async def health():
    return {"ok": True}

@app.post("/add-server-info")
async def receive_server_info(info: ServerInfo):
    global REGISTERED_MEDIA_SERVICE
    REGISTERED_MEDIA_SERVICE = info
    prints(f"Registered media service: {info}")
    return {"registered": True}

@app.post("/remove-server-info")
async def remove_server_info():
    global REGISTERED_MEDIA_SERVICE
    REGISTERED_MEDIA_SERVICE = None
    prints("Deregistered media service.")
    return {"removed": True}