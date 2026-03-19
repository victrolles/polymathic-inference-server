import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from shared.structs import ServerInfo
from shared.utils.functions import load_module
from shared.utils.requests import wait_for_server, add_server, remove_server

WORKER_HOST = os.getenv("WORKER_HOST", "localhost")
WORKER_PORT = os.getenv("WORKER_PORT", "8001")
WORKER_URL = f"http://{WORKER_HOST}:{WORKER_PORT}/"

MEDIA_SERVICE_PORT = os.getenv("MEDIA_SERVICE_PORT", "6000")
MEDIA_SERVICE_HOST = os.getenv("MEDIA_SERVICE_HOST", "localhost")
MEDIA_SERVICE_URL = f"http://{MEDIA_SERVICE_HOST}:{MEDIA_SERVICE_PORT}/"

MODELS_PATH = os.getenv("MODELS_PATH", "unknown")
MODEL_ID = os.getenv("MODEL_ID")
SIZE_ID = os.getenv("SIZE_ID")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await wait_for_server(MEDIA_SERVICE_URL)
    info = ServerInfo(
        url=WORKER_URL,
        model_id=MODEL_ID,
        size_id=SIZE_ID
    )
    await add_server(MEDIA_SERVICE_URL, info)
    yield
    await remove_server(MEDIA_SERVICE_URL, info)

app = FastAPI(lifespan=lifespan)

# Setup inference and load model
model_path = os.path.join(MODELS_PATH, MODEL_ID)
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model not found: {model_path}")
inference_module = load_module(model_path, "inference", "inference.py")
inference = inference_module.Inference(size_id=SIZE_ID)


    