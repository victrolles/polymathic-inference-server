import os
import asyncio
from contextlib import asynccontextmanager
import sys

import httpx
from fastapi import FastAPI

from .structs import ServerInfo
from .utils import extend_url, prints
from .data_manager import DataManager

GATEWAY_PORT = os.getenv("GATEWAY_PORT", "8000")
GATEWAY_HOST = os.getenv("GATEWAY_HOST", "localhost")
GATEWAY_URL = f"http://{GATEWAY_HOST}:{GATEWAY_PORT}/"

MEDIA_SERVICE_HOST = os.getenv("MEDIA_SERVICE_HOST", "localhost")
MEDIA_SERVICE_PORT = os.getenv("MEDIA_SERVICE_PORT", "6000")
MEDIA_SERVICE_URL = f"http://{MEDIA_SERVICE_HOST}:{MEDIA_SERVICE_PORT}/"

WORKER_HOST = os.getenv("WORKER_HOST", "localhost")
WORKER_PORT = os.getenv("WORKER_PORT", "8001")
WORKER_URL = f"http://{WORKER_HOST}:{WORKER_PORT}/"

MODEL_ID = os.getenv("MODEL_ID", "unknown")
SIZE_ID = os.getenv("SIZE_ID", "unknown")

MEDIA_FILES_PATH = os.getenv("MEDIA_FILES_PATH", "unknown")
MODELS_PATH = os.getenv("MODELS_PATH", "unknown")

async def wait_for_server(server_name: str, server_url: str, interval: float = 1.0, request_timeout: float = 5.0):
    async with httpx.AsyncClient(timeout=request_timeout) as client:
        while True:
            try:
                r = await client.get(extend_url(server_url, "/health"))
                if r.status_code < 500:
                    prints(f"{server_name} {server_url} is ready.")
                    return
            except Exception:
                pass

            prints(f"{server_name} {server_url} not ready yet, retrying in {interval}s...")
            await asyncio.sleep(interval)


async def send_server_info(server_name: str, server_url: str, info: ServerInfo, request_timeout: float = 5.0,):
    async with httpx.AsyncClient(timeout=request_timeout) as client:
        r = await client.post(extend_url(server_url, "/add-server-info"), json=info.model_dump())
        r.raise_for_status()
        prints(f"Sent ServerInfo to {server_name}: {server_url}")

async def remove_server_info(server_name: str, server_url: str, request_timeout: float = 5.0):
    async with httpx.AsyncClient(timeout=request_timeout) as client:
        try:
            r = await client.post(extend_url(server_url, "/remove-server-info"))
            r.raise_for_status()
            prints(f"Deregistered from {server_name}: {server_url}")
        except Exception as e:
            # Do not crash shutdown if worker is already gone
            prints(f"Failed to deregister from {server_name}: {server_url}: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await wait_for_server("Worker", WORKER_URL)
    await wait_for_server("Gateway", GATEWAY_URL)

    info = ServerInfo(
        url=MEDIA_SERVICE_URL,
        model_id=MODEL_ID,
        size_id=SIZE_ID,
    )
    await send_server_info("Worker", WORKER_URL, info)
    await send_server_info("Gateway", GATEWAY_URL, info)

    yield
    await remove_server_info("Worker", WORKER_URL)
    await remove_server_info("Gateway", GATEWAY_URL)

app = FastAPI(lifespan=lifespan)

model_path = os.path.join(MODELS_PATH, MODEL_ID)
sys.path.insert(0, model_path)

data_manager = DataManager(MEDIA_FILES_PATH, model_path)

@app.get("/api/request_model_sizes_tasks")
async def request_model_sizes_tasks():
    return data_manager.get_model_sizes_tasks().model_dump()

@app.get("/api/request_config_dict")
async def request_config_dict():
    return data_manager.get_config_dict()