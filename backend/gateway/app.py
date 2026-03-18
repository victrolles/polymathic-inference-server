import os

from fastapi import FastAPI, HTTPException
import httpx
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .structs import Model, ServerInfo, ModelSizeTaskRequest, RandomDataSamplesRequest, MediaFile
from .utils import prints, add_server, extend_url, convert_media_files_to_url, get_media_service

GATEWAY_HOST = os.getenv("GATEWAY_HOST", "localhost")
GATEWAY_PORT = os.getenv("GATEWAY_PORT", "8000")
MEDIA_FILES_PATH = os.getenv("MEDIA_FILES_PATH", "unknown")

servers: list[ServerInfo] = []
# (model_id, size_id) -> media service (O(1) lookup)
servers_by_model_size: dict[tuple[str, str], ServerInfo] = {}

app = FastAPI()

origins = [
    "http://localhost:7999",
    "http://127.0.0.1:7999"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/media_files", StaticFiles(directory=MEDIA_FILES_PATH), name="media_files")


@app.get("/health")
async def health():
    return {"ok": True}

@app.post("/add-server-info")
async def receive_server_info(server: ServerInfo):
    add_server(servers, server, servers_by_model_size=servers_by_model_size)
    return {"registered": True}

@app.get("/api/request_all_models_sizes_tasks")
async def request_all_models_sizes_tasks():
    
    # --- ASK to all Media Services ---
    models_sizes_tasks: list[Model] = []
    models_done: set[str] = set()
    for (_model_id, _size_id), server in servers_by_model_size.items():
        if server.model_id in models_done:
            continue
        models_done.add(server.model_id)
        try:
            async with httpx.AsyncClient() as client:
                r = await client.get(
                    extend_url(server.url, "/api/request_model_sizes_tasks")
                )
                r.raise_for_status()
                data = r.json()
                models_sizes_tasks.append(Model(**data))
        except httpx.HTTPError as e:
            error_message = f"Error requesting all models sizes tasks from {server.url}: {e}"
            prints(error_message)
            raise HTTPException(status_code=500, detail=error_message)

    return {
        "ok": True,
        "models_sizes_tasks": models_sizes_tasks
    }

@app.post("/api/request_a_model_config_task")
async def request_a_model_config_task(request: ModelSizeTaskRequest):
    mst = request.model_size_task_id
    server = get_media_service(servers_by_model_size, mst.model_id, mst.size_id)
    if server is None:
        error_message = (
            f"No media service for model_id={mst.model_id!r} size_id={mst.size_id!r}"
        )
        prints(error_message)
        raise HTTPException(status_code=404, detail=error_message)
    try:
        async with httpx.AsyncClient() as client:
            r = await client.post(extend_url(server.url, "/api/request_config_task"),json={"task_id": mst.task_id},)
            r.raise_for_status()
            return {"ok": True, "config_task": r.json()}
    except httpx.HTTPError as e:
        error_message = (
            f"Error requesting config task from {server.url} for "
            f"model {mst.model_id} size {mst.size_id} task {mst.task_id}: {e}"
        )
        prints(error_message)
        raise HTTPException(status_code=500, detail=error_message)

@app.post("/api/request_random_data_samples")
async def request_random_data_samples(request: RandomDataSamplesRequest):
    mst = request.model_size_task_id
    server = get_media_service(servers_by_model_size, mst.model_id, mst.size_id)
    if server is None:
        error_message = f"No media service for model_id={mst.model_id!r} size_id={mst.size_id!r}"
        prints(error_message)
        raise HTTPException(status_code=404, detail=error_message)
    try:
        async with httpx.AsyncClient() as client:
            r = await client.post(
                extend_url(server.url, "/api/request_random_data_samples"),
                json={"task_id": mst.task_id},
            )
            r.raise_for_status()
            media_files = [MediaFile(**media_file) for media_file in r.json()]
            media_files_urls = convert_media_files_to_url(
                media_files,
                GATEWAY_HOST,
                GATEWAY_PORT,
                mst.model_id,
                mst.size_id,
            )
            return {"ok": True, "media_files": media_files_urls}
    except httpx.HTTPError as e:
        error_message = (
            f"Error requesting random data samples from {server.url} for "
            f"model {mst.model_id} size {mst.size_id} task {mst.task_id}: {e}"
        )
        prints(error_message)
        raise HTTPException(status_code=500, detail=error_message)