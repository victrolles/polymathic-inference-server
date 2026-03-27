import os
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, HTTPException

from .media_service import MediaService

from python.structs.general import ServerInfo, TaskRequest, InferenceRequest, InferenceDataInput
from python.functions.utils import prints
from python.functions.requests import (
    wait_for_server,
    add_server as register_server,
    remove_server as unregister_server,
    extend_url,
)
from python.functions.binary_transport import to_binary_payload, from_binary_payload
from python.functions.server_manager import ServerManager

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
    packets = media_service.get_random_data_samples(request.task_id)
    return [packet.model_dump(mode="json") for packet in packets]

@app.post("/api/request_inference")
async def request_inference(request: InferenceRequest):
    mst = request.model_size_task_id
    prints("Step 1 / 12 : Pre processing inference", "MEDIA_SERVICE")
    data_inputs = media_service.pre_process_inference(mst.task_id, request.dataset_locations)
    

    # call inference function
    server = server_manager.registry.get_server_by_model_size(mst.model_id, mst.size_id)
    inference_data_input = InferenceDataInput(
        input=data_inputs,
        task_id=mst.task_id
    )
    prints("Step 2 / 12 : Serializing", "MEDIA_SERVICE")
    request_kwargs: dict = {}
    request_kwargs["content"] = to_binary_payload(inference_data_input)
    prints("Step 3 / 12 : Sending to worker", "MEDIA_SERVICE")
    try:
        async with httpx.AsyncClient(timeout=3600) as client:
            r = await client.post(
                extend_url(server.url, "/api/request_inference"),
                **request_kwargs,
            )
            r.raise_for_status()
            prints("Step 9 / 12 : Receiving from worker", "MEDIA_SERVICE")
            inference_result = from_binary_payload(r.content)
            prints("Step 10 / 12 : Deserializing", "MEDIA_SERVICE")
    except httpx.HTTPError as e:
        error_message = (
            f"Error requesting random data samples from {server.url} for "
            f"model {mst.model_id} size {mst.size_id} task {mst.task_id}: {e}"
        )
        print(error_message)
        raise HTTPException(status_code=500, detail=error_message)

    #Post process inference result
    prints("Step 11 / 12 : Post process inference", "MEDIA_SERVICE")
    packets = media_service.post_process_inference(inference_result, mst)
    prints("Step 12 / 12 : Returning packets to gateway", "MEDIA_SERVICE")
    return [packet.model_dump(mode="json") for packet in packets]