import os
import asyncio
from contextlib import asynccontextmanager
import sys

import httpx
from fastapi import FastAPI, HTTPException

from shared.structs import ServerInfo, TaskRequest
from shared.utils.requests import (
    wait_for_server,
    add_server as register_server,
    remove_server as unregister_server,
)
from .media_service import MediaService
from shared.server_manager import ServerManager

GATEWAY_PORT = os.getenv("GATEWAY_PORT", "8000")
GATEWAY_HOST = os.getenv("GATEWAY_HOST", "localhost")
GATEWAY_URL = f"http://{GATEWAY_HOST}:{GATEWAY_PORT}/"

MEDIA_SERVICE_HOST = os.getenv("MEDIA_SERVICE_HOST", "localhost")
MEDIA_SERVICE_PORT = os.getenv("MEDIA_SERVICE_PORT", "6000")
MEDIA_SERVICE_URL = f"http://{MEDIA_SERVICE_HOST}:{MEDIA_SERVICE_PORT}/"

MODEL_ID = os.getenv("MODEL_ID", "unknown")

MEDIA_FILES_PATH = os.getenv("MEDIA_FILES_PATH", "unknown")
MODELS_PATH = os.getenv("MODELS_PATH", "unknown")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await wait_for_server(GATEWAY_URL)
    info = ServerInfo(
        url=MEDIA_SERVICE_URL,
        model_id=MODEL_ID
    )
    await register_server(GATEWAY_URL, info)
    yield
    await unregister_server(GATEWAY_URL, info)

app = FastAPI(lifespan=lifespan)

server_manager = ServerManager()
media_service = MediaService(MEDIA_FILES_PATH, MODELS_PATH, MODEL_ID)

@app.get("/health")
async def health():
    return {"ok": True}

@app.post("/add-server")
async def add_server(info: ServerInfo):
    server_manager.add_server(info)
    print(f"Added Worker {info.model_id} {info.size_id} to server manager")
    return {"registered": True}

@app.post("/remove-server")
async def remove_server(info: ServerInfo):
    server_manager.remove_server(info)
    print(f"Removed Worker {info.model_id} {info.size_id} from server manager")
    return {"removed": True}

@app.get("/api/request_model_sizes_tasks")
async def request_model_sizes_tasks():
    return media_service.get_model_sizes_tasks()

@app.post("/api/request_config_task")
async def request_config_task(request: TaskRequest):
    return media_service.get_config_task(request.task_id)

@app.post("/api/request_random_data_samples")
async def request_random_data_samples(request: TaskRequest):
    media_files = media_service.get_random_data_samples(request.task_id)
    return [media_file.model_dump() for media_file in media_files]