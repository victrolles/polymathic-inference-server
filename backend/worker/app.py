import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response

from shared.structs import ServerInfo, InferenceDataInput
from shared.utils.functions import load_module
from shared.utils.requests import wait_for_server, add_server, remove_server
from shared.utils.binary_transport import from_binary_payload, to_binary_payload
from worker.template.inference_base import InferenceBase

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
model_src = os.path.abspath(os.path.join(model_path, "src"))
if not os.path.exists(model_src):
    raise FileNotFoundError(f"Model src not found: {model_src}")
inference_module = load_module(model_src, "inference", "inference.py")
inference: InferenceBase = inference_module.Inference(size_id=SIZE_ID)

@app.post("/api/request_inference")
async def request_inference(request: Request):
    print(f"========== Receiving request ==========")
    body = await request.body()
    print(f"========== Deserializing ==========")
    payload = from_binary_payload(body)
    parsed_request = InferenceDataInput.model_validate(payload)

    input = parsed_request.input
    task_id = parsed_request.task_id
    print("========== inferring ==========")
    inference_result = inference.infer(input, task_id)
    print("========== Serializing ==========")
    binary_response = to_binary_payload(inference_result)
    print(f"========== Returning response ==========")
    return Response(content=binary_response, media_type="application/octet-stream")
