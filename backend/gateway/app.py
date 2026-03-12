import os

from fastapi import FastAPI, HTTPException
import httpx
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .structs import Model, ServerInfo, ModelConfigDictRequest
from .utils import prints, add_server, extend_url

GATEWAY_HOST = os.getenv("GATEWAY_HOST", "localhost")
GATEWAY_PORT = os.getenv("GATEWAY_PORT", "8000")
MEDIA_FILES_PATH = os.getenv("MEDIA_FILES_PATH", "unknown")

servers: list[ServerInfo] = []

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
    add_server(servers, server)
    return {"registered": True}

@app.get("/api/request_all_models_sizes_tasks")
async def request_all_models_sizes_tasks():
    
    # --- ASK to all Media Services ---
    models_sizes_tasks: list[Model] = []
    models_done: list[str] = []
    for server in servers:
        if server.model_id not in models_done:
            models_done.append(server.model_id)
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

@app.post("/api/request_a_model_config_dict")
async def request_a_model_config_dict(request: ModelConfigDictRequest):
    for server in servers:
        if server.model_id == request.model_id:
            try:
                async with httpx.AsyncClient() as client:
                    r = await client.get(extend_url(server.url, "/api/request_config_dict"))
                    r.raise_for_status()
                    return {
                        "ok": True,
                        "config_dict": r.json()
                    }
            except httpx.HTTPError as e:
                error_message = f"Error requesting config dict from {server.url} for model {request.model_id}: {e}"
                prints(error_message)
                raise HTTPException(status_code=500, detail=error_message)
    error_message = f"Model {request.model_id} not found"
    prints(error_message)
    raise HTTPException(status_code=404, detail=error_message)