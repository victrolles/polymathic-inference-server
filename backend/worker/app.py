import os

from fastapi import FastAPI

GATEWAY_PORT = os.getenv("GATEWAY_PORT", "8000")
GATEWAY_HOST = os.getenv("GATEWAY_HOST", "localhost")
GATEWAY_URL = f"http://{GATEWAY_HOST}:{GATEWAY_PORT}"

WORKER_HOST = os.getenv("WORKER_HOST", "localhost")
WORKER_PORT = os.getenv("WORKER_PORT", "8001")
WORKER_URL = f"http://{WORKER_HOST}:{WORKER_PORT}"

MODEL_NAME = os.getenv("MODEL_NAME", "unknown")
TASK_NAME = os.getenv("TASK_NAME", "default")

MEDIA_FILES_PATH = os.getenv("MEDIA_FILES_PATH", "unknown")
SRC_PATH = os.getenv("SRC_PATH", "unknown")

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": f"Hello from Worker Server {WORKER_HOST}!"}