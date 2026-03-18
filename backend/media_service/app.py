import os
import asyncio
from contextlib import asynccontextmanager
import sys

import httpx
from fastapi import FastAPI, HTTPException

from .structs import ServerInfo, RandomDataSamplesRequest, ModelConfigTaskRequest
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

async def wait_for_server(server_name: str, server_url: str, interval: float = 5.0, request_timeout: float = 5.0):
    async with httpx.AsyncClient(timeout=request_timeout) as client:
        timeout=0
        while True:
            try:
                r = await client.get(extend_url(server_url, "/health"))
                if r.status_code < 500:
                    prints(f"{server_name} {server_url} is ready.")
                    return
            except Exception:
                pass

            prints(f"{server_name} {server_url} not ready yet, retrying in {interval}s...")
            timeout += interval
            if timeout > 60:
                raise Exception(f"{server_name} {server_url} not ready after {timeout} seconds")
            await asyncio.sleep(interval)


async def send_server_info(server_name: str, server_url: str, info: ServerInfo, request_timeout: float = 10.0):
    async with httpx.AsyncClient(timeout=request_timeout) as client:
        try:
            r = await client.post(extend_url(server_url, "/add-server-info"), json=info.model_dump())
            r.raise_for_status()
            prints(f"Sent ServerInfo to {server_name}: {server_url}")
        except Exception as e:
            prints(f"Failed to send ServerInfo to {server_name}: {server_url}: {e}")
            raise e

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

media_files_path = os.path.join(MEDIA_FILES_PATH, MODEL_ID, SIZE_ID)
data_manager = DataManager(media_files_path, model_path)

@app.get("/api/request_model_sizes_tasks")
async def request_model_sizes_tasks():
    return data_manager.get_model_sizes_tasks().model_dump()

@app.post("/api/request_config_task")
async def request_config_task(request: ModelConfigTaskRequest):
    return data_manager.get_config_task(request.task_id)

@app.post("/api/request_random_data_samples")
async def request_random_data_samples(request: RandomDataSamplesRequest):
    media_files = data_manager.get_random_data_samples(request.task_id)
    return [media_file.model_dump() for media_file in media_files]