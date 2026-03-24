import os
import sys
import importlib.util
from types import ModuleType

from shared.structs import Packet

def extend_url(url: str, path: str) -> str:
    return url.rstrip("/") + path



def convert_path_to_url(path: str, host: str, port: int, model_id: str) -> str:
    file_name = os.path.basename(path)
    return f"http://{host}:{port}/media_files/{model_id}/{file_name}"

def convert_packets_to_url(packets: list[Packet], host: str, port: int, model_id: str) -> list[Packet]:
    for idx, packet in enumerate(packets):
        modalities = packet.modalities  
        for idx2, modality in enumerate(modalities):
            path = convert_path_to_url(modality.media_file.path, host, port, model_id)
            packets[idx].modalities[idx2].media_file.path = path
    return packets

def load_module(model_src: str, module_name: str, file_name: str) -> ModuleType:
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
