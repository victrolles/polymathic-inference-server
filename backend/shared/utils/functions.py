import os
import sys
import importlib.util
from types import ModuleType

def extend_url(url: str, path: str) -> str:
    return url.rstrip("/") + path



# def convert_path_to_url(path: str, host: str, port: int, model_id: str, size_id: str) -> str:
#     file_name = os.path.basename(path)
#     return f"http://{host}:{port}/media_files/{model_id}/{size_id}/{file_name}"

# def convert_media_files_to_url(media_files: list[MediaFile], host: str, port: int, model_id: str, size_id: str) -> list[str]:
#     for idx in range(len(media_files)):
#         media_files[idx].path = convert_path_to_url(media_files[idx].path, host, port, model_id, size_id)
#     return media_files

def load_module(model_path: str, module_name: str, file_name: str) -> ModuleType:
    model_src = os.path.abspath(os.path.join(model_path, "src"))
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
