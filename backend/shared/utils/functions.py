import os

from .structs import MediaFile, ServerInfo

def extend_url(url: str, path: str) -> str:
    return url.rstrip("/") + path

def prints(info):
    print(f"[GATEWAY]:    {info}")

def add_server(
    servers: list[ServerInfo],
    new_server: ServerInfo,
    *,
    servers_by_model_size: dict[tuple[str, str], ServerInfo] | None = None,
) -> None:
    for server in list(servers):
        if (server.model_id == new_server.model_id) and (server.size_id == new_server.size_id):
            prints(f"Old server {server.model_id} : {server.size_id} has been replaced : {server.url} -> {new_server.url}")
            servers.remove(server)
            break
    servers.append(new_server)
    key = (new_server.model_id, new_server.size_id)
    if servers_by_model_size is not None:
        servers_by_model_size[key] = new_server
    prints(f"New server registered: {new_server.url} ({key[0]} / {key[1]})")


def get_media_service(
    servers_by_model_size: dict[tuple[str, str], ServerInfo],
    model_id: str,
    size_id: str,
) -> ServerInfo | None:
    """One media service instance per (model_id, size_id); serves all tasks for that pair."""
    return servers_by_model_size.get((model_id, size_id))

def convert_path_to_url(path: str, host: str, port: int, model_id: str, size_id: str) -> str:
    file_name = os.path.basename(path)
    return f"http://{host}:{port}/media_files/{model_id}/{size_id}/{file_name}"

def convert_media_files_to_url(media_files: list[MediaFile], host: str, port: int, model_id: str, size_id: str) -> list[str]:
    for idx in range(len(media_files)):
        media_files[idx].path = convert_path_to_url(media_files[idx].path, host, port, model_id, size_id)
    return media_files

import base64
import io
import random
import os
import sys
import importlib.util
from types import ModuleType

import torch
from datasets import load_from_disk

def extend_url(url: str, path: str) -> str:
    return url.rstrip("/") + path

def prints(info):
    print(f"[MEDIA_SERVICE]:    {info}")

def load_dataset_huggingface(dataset_path: str):
    return load_from_disk(dataset_path)

def load_dataset_torch(dataset_path: str):
    return torch.load(dataset_path)

def pil_image_to_jsonable(pil_image) -> dict:
    """Encode a PIL Image as JSON-serializable dict (base64 PNG)."""
    buf = io.BytesIO()
    pil_image.save(buf, format="PNG")
    buf.seek(0)
    return {"content_type": "image/png", "data_base64": base64.b64encode(buf.getvalue()).decode()}

def load_module(full_path: str) -> ModuleType:
    """Load a Python module from a file path (e.g. visualizer.py)."""
    module_path = os.path.abspath(full_path)
    parent_dir = os.path.dirname(module_path)
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    name = os.path.splitext(os.path.basename(module_path))[0]
    spec = importlib.util.spec_from_file_location(name, module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module

    import os
import sys
import importlib
import importlib.util
from types import ModuleType

from .template.inference_base import InferenceBase

def prints(info):
    print(f"[WORKER]:   {info}")

def _load_module(models_path: str, model_id: str, module_name: str, file_name: str) -> ModuleType:
    model_src = os.path.abspath(os.path.join(models_path, model_id, "src"))
    module_path = os.path.join(model_src, file_name)
    if not os.path.isfile(module_path):
        raise FileNotFoundError(f"Module not found: {module_path}")
    if model_src not in sys.path:
        sys.path.insert(0, model_src)
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

def load_inference(models_path: str, model_id: str, size_id: str) -> InferenceBase:
    inference_module = _load_module(models_path, model_id, "inference", "inference.py")
    prints(f"Loading {model_id} - {size_id} ...")
    inference = inference_module.Inference(size_id=size_id)
    prints(f"Loading {model_id} - {size_id} done")
    return inference
