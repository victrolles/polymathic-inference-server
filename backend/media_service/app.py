import os
import sys
from contextlib import asynccontextmanager
import httpx
from fastapi import FastAPI

from schemas import WorkerInfo


GATEWAY_PORT = os.getenv("GATEWAY_PORT", "8000")
GATEWAY_HOST = os.getenv("GATEWAY_HOST", "localhost")
GATEWAY_URL = f"http://{GATEWAY_HOST}:{GATEWAY_PORT}"

MEDIA_SERVICE_HOST = os.getenv("MEDIA_SERVICE_HOST", "localhost")
MEDIA_SERVICE_PORT = os.getenv("MEDIA_SERVICE_PORT", "6000")
MEDIA_SERVICE_URL = f"http://{MEDIA_SERVICE_HOST}:{MEDIA_SERVICE_PORT}"

WORKER_HOST = os.getenv("WORKER_HOST", "localhost")
WORKER_PORT = os.getenv("WORKER_PORT", "8001")
WORKER_URL = f"http://{WORKER_HOST}:{WORKER_PORT}"

MODEL_NAME = os.getenv("MODEL_NAME", "unknown")
TASK_NAME = os.getenv("TASK_NAME", "default")

MEDIA_FILES_PATH = os.getenv("MEDIA_FILES_PATH", "unknown")
MODELS_PATH = os.getenv("MODELS_PATH", "unknown")


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": f"Hello from Media Service Server {MEDIA_SERVICE_HOST}!"}