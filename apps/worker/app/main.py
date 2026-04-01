import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response

from python.templates.inference_base import InferenceBase
from python.structs.general import ServerInfo, InferenceDataInput
from python.functions.utils import load_module, prints
from python.functions.requests import wait_for_server, add_server, remove_server
from python.functions.binary_transport import from_binary_payload, to_binary_payload

WORKER_HOST = os.getenv("WORKER_HOST", "unknown")
WORKER_PORT = os.getenv("WORKER_PORT", "unknown")
WORKER_URL = f"http://{WORKER_HOST}:{WORKER_PORT}/"

MEDIA_SERVICE_PORT = os.getenv("MEDIA_SERVICE_PORT", "unknown")
MEDIA_SERVICE_HOST = os.getenv("MEDIA_SERVICE_HOST", "unknown")
MEDIA_SERVICE_URL = f"http://{MEDIA_SERVICE_HOST}:{MEDIA_SERVICE_PORT}/"

MODELS_PATH = os.getenv("MODELS_PATH", "unknown")
DATASETS_PATH = os.getenv("DATASETS_PATH", "unknown")
WEIGHTS_PATH = os.getenv("WEIGHTS_PATH", "unknown")

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
    prints("Step 4 / 12 : Receiving from media service", "WORKER")
    body = await request.body()
    prints("Step 5 / 12 : Deserializing", "WORKER")
    payload = from_binary_payload(body)
    parsed_request = InferenceDataInput.model_validate(payload)

    input = parsed_request.input
    task_id = parsed_request.task_id
    prints("Step 6 / 12 : Inferring", "WORKER")
    inference_result = inference.infer(input, task_id)
    prints("Step 7 / 12 : Serializing", "WORKER")
    binary_response = to_binary_payload(inference_result)
    prints("Step 8 / 12 : Returning response to media service", "WORKER")
    return Response(content=binary_response, media_type="application/octet-stream")
