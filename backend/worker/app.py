import os
import sys
import importlib

from fastapi import FastAPI

from .structs import ServerInfo
from .utils import prints, load_inference

WORKER_HOST = os.getenv("WORKER_HOST", "localhost")
WORKER_PORT = os.getenv("WORKER_PORT", "8001")
WORKER_URL = f"http://{WORKER_HOST}:{WORKER_PORT}/"

MODELS_PATH = os.getenv("MODELS_PATH", "unknown")
MODEL_ID = os.getenv("MODEL_ID")
SIZE_ID = os.getenv("SIZE_ID")

app = FastAPI()

REGISTERED_MEDIA_SERVICE: ServerInfo | None = None

inference = load_inference(MODELS_PATH, MODEL_ID, SIZE_ID)

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

# @app.post("/api/request_inference")
# async def request_inference(request: RequestInference):
#     prints(f"Requesting inference for task {request.task_id}")
#     return inference.infer(request.input, request.task_id)