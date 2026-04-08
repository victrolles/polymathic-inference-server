import os
import sys
import importlib.util
from pathlib import Path
from types import ModuleType
import shutil

from ..structs.general import Packet

def find_file_in_path(path: str, file_name: str) -> str:
    matches = sorted(Path(path).glob(f"{file_name}.*"))
    if len(matches) == 0:
        raise FileNotFoundError(f"File not found: {file_name} in {path}")
    return str(matches[0])
    
def copy_file_to_path(source_path: str, destination_path: str) -> None:
    shutil.copy(Path(source_path), Path(destination_path))

def extend_url(url: str, path: str) -> str:
    return url.rstrip("/") + path

def prints(message: str, server_type: str):
    if server_type == "GATEWAY":
        print(f"[GATEWAY]: {message}")
    elif server_type == "MEDIA_SERVICE":
        print(f"[MEDIA_SERVICE]: {message}")
    elif server_type == "WORKER":
        print(f"[WORKER]: {message}")
    else:
        raise ValueError(f"Invalid server type: {server_type}")

def convert_path_to_url(path: str) -> str:
    split_path = path.split("/")
    for idx in range(len(split_path)):
        if split_path[idx] == "media_files":
            truncated_path = "/".join(split_path[idx:])
            return f"/{truncated_path}" 
    raise ValueError(f"Path not found: {path}")

def convert_packets_to_url(packets: list[Packet]) -> list[Packet]:
    for idx, packet in enumerate(packets):
        modalities = packet.modalities  
        for idx2, modality in enumerate(modalities):
            path = convert_path_to_url(modality.media_file.path)
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
