import os

from fastapi import FastAPI, HTTPException
import httpx
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from shared.structs import ServerInfo, ModelInfo, ModelSizeTaskRequest, Packet, InferenceRequest, ModelRequest
from media_service.config.structs import InformationConfig
from shared.server_manager import ServerManager
from shared.utils.requests import extend_url
from shared.utils.functions import convert_packets_to_url, convert_path_to_url
from python.structs.general import ServerInfo, ModelInfo, ModelSizeTaskRequest, Packet, InferenceRequest, ModelRequest
from python.functions.server_manager import ServerManager
from python.functions.utils import extend_url, convert_packets_to_url

GATEWAY_HOST = os.getenv("GATEWAY_HOST", "unknown")
GATEWAY_PORT = os.getenv("GATEWAY_PORT", "unknown")
MEDIA_FILES_PATH = os.getenv("MEDIA_FILES_PATH", "unknown")

print(f"GATEWAY_HOST: {GATEWAY_HOST}")
print(f"GATEWAY_PORT: {GATEWAY_PORT}")
print(f"MEDIA_FILES_PATH: {MEDIA_FILES_PATH}")

server_manager = ServerManager()

app = FastAPI(title="gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/media_files", StaticFiles(directory=MEDIA_FILES_PATH), name="media_files")

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/api/healthz")
def api_healthz():
    return {"status": "ok", "service": "gateway"}

@app.get("/health")
async def health():
    return {"ok": True}

@app.post("/add-server")
async def add_server(info: ServerInfo):
    server_manager.add_server(info)
    print(f"Added Media Service {info} to server manager {server_manager.servers}")
    return {"registered": True}

@app.post("/remove-server")
async def remove_server(info: ServerInfo):
    server_manager.remove_server(info)
    print(f"Removed Media Service {info} from server manager {server_manager.servers}")
    return {"removed": True}

@app.get("/api/request_all_models_sizes_tasks")
async def request_all_models_sizes_tasks():
    
    # --- ASK to all Media Services ---
    models_sizes_tasks: list[ModelInfo] = []
    for server in server_manager.servers:
        try:
            async with httpx.AsyncClient(timeout=3600) as client:
                r = await client.get(
                    extend_url(server.url, "/api/request_model_sizes_tasks")
                )
                r.raise_for_status()
                data = r.json()
                models_sizes_tasks.append(ModelInfo(**data))
        except httpx.HTTPError as e:
            error_message = f"Error requesting all models sizes tasks from {server.url}: {e}"
            print(error_message)
            raise HTTPException(status_code=500, detail=error_message)

    return {
        "ok": True,
        "models_sizes_tasks": models_sizes_tasks
    }

@app.post("/api/request_a_model_config_task")
async def request_a_model_config_task(request: ModelSizeTaskRequest):
    mst = request.model_size_task_id
    server = server_manager.registry.get_server_by_model(mst.model_id)
    if server is None:
        error_message = (
            f"No media service for model_id={mst.model_id}"
        )
        print(error_message)
        raise HTTPException(status_code=404, detail=error_message)
    try:
        async with httpx.AsyncClient(timeout=3600) as client:
            r = await client.post(extend_url(server.url, "/api/request_config_task"),json={"task_id": mst.task_id},)
            r.raise_for_status()
            return {"ok": True, "config_task": r.json()}
    except httpx.HTTPError as e:
        error_message = (
            f"Error requesting config task from {server.url} for "
            f"model {mst.model_id} task {mst.task_id}: {e}"
        )
        print(error_message)
        raise HTTPException(status_code=500, detail=error_message)

@app.post("/api/request_model_information")
async def request_model_information(request: ModelRequest):
    server = server_manager.registry.get_server_by_model(request.model_id)
    if server is None:
        error_message = (
            f"No media service for model_id={request.model_id}"
        )
        print(error_message)
        raise HTTPException(status_code=404, detail=error_message)
    try:
        async with httpx.AsyncClient(timeout=3600) as client:
            r = await client.get(extend_url(server.url, "/api/request_model_information"))
            r.raise_for_status()
            information = InformationConfig(**r.json())
            if information.display:
                information.cover_image_path = convert_path_to_url(information.cover_image_path, GATEWAY_HOST, GATEWAY_PORT)
            return information.model_dump(mode="json")
    except httpx.HTTPError as e:
        error_message = (
            f"Error requesting model information from {server.url} for "
            f"model {request.model_id}: {e}"
        )
        print(error_message)
        raise HTTPException(status_code=500, detail=error_message)

@app.get("/api/request_all_models_information")
async def request_all_models_information():
    
    # --- ASK to all Media Services ---
    models_information: list[InformationConfig] = []
    for server in server_manager.servers:
        try:
            async with httpx.AsyncClient(timeout=3600) as client:
                r = await client.get(
                    extend_url(server.url, "/api/request_model_information")
                )
                r.raise_for_status()
                data = r.json()
                information_config = InformationConfig(**data)
                if information_config.display:
                    information_config.cover_image_path = convert_path_to_url(information_config.cover_image_path, GATEWAY_HOST, GATEWAY_PORT)
                    models_information.append(information_config.model_dump(mode="json"))
        except httpx.HTTPError as e:
            error_message = f"Error requesting all models information from {server.url}: {e}"
            print(error_message)
            raise HTTPException(status_code=500, detail=error_message)

    return {
        "ok": True,
        "models_information": models_information
    }

@app.post("/api/request_random_data_samples")
async def request_random_data_samples(request: ModelSizeTaskRequest):
    mst = request.model_size_task_id
    server = server_manager.registry.get_server_by_model(mst.model_id)
    if server is None:
        error_message = (
            f"No media service for model_id={mst.model_id}"
        )
        print(error_message)
        raise HTTPException(status_code=404, detail=error_message)
    try:
        async with httpx.AsyncClient(timeout=3600) as client:
            r = await client.post(
                extend_url(server.url, "/api/request_random_data_samples"),
                json={"task_id": mst.task_id},
            )
            r.raise_for_status()
            packets = [Packet(**packet) for packet in r.json()]
            new_packets = convert_packets_to_url(packets, GATEWAY_HOST, GATEWAY_PORT)
            return {"ok": True, "packets": new_packets}
    except httpx.HTTPError as e:
        error_message = (
            f"Error requesting random data samples from {server.url} for "
            f"model {mst.model_id} size {mst.size_id} task {mst.task_id}: {e}"
        )
        print(error_message)
        raise HTTPException(status_code=500, detail=error_message)

@app.post("/api/request_inference")
async def request_inference(request: InferenceRequest):
    mst = request.model_size_task_id
    server = server_manager.registry.get_server_by_model(mst.model_id)
    if server is None:
        error_message = (
            f"No media service for model_id={mst.model_id}"
        )
        print(error_message)
        raise HTTPException(status_code=404, detail=error_message)
    try:
        async with httpx.AsyncClient(timeout=3600) as client:
            r = await client.post(
                extend_url(server.url, "/api/request_inference"),
                json=request.model_dump(mode="json"),
            )
            r.raise_for_status()
            packets = [Packet(**packet) for packet in r.json()]
            new_packets = convert_packets_to_url(packets, GATEWAY_HOST, GATEWAY_PORT)
            return {"ok": True, "packets": new_packets}
    except httpx.HTTPError as e:
        error_message = (
            f"Error requesting random data samples from {server.url} for "
            f"model {mst.model_id} size {mst.size_id} task {mst.task_id}: {e}"
        )
        print(error_message)
        raise HTTPException(status_code=500, detail=error_message)