import inspect
import os

import yaml

def get_var_name(x):
    frame = inspect.currentframe().f_back
    for name, val in frame.f_locals.items():
        if val is x:
            return name

def get_model_sizes_from_config(models_path: str, model_name: str):
    path_to_yaml = os.path.join(models_path, model_name, "config.yaml")
    if not os.path.exists(path_to_yaml):
        raise FileNotFoundError(f"Config file not found for model {model_name} at {path_to_yaml}")

    with open(path_to_yaml, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    return config["sizes"]
        