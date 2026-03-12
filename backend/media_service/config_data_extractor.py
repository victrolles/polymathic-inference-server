from typing import Dict

from .structs import IdName

def extract_model(config: Dict) -> IdName:
    return IdName(id=config["model"]["id"], name=config["model"]["name"])

def extract_sizes(config: Dict) -> list[IdName]:
    return [IdName(id=size["id"], name=size["name"]) for size in config["sizes"]]

def extract_tasks(config: Dict) -> list[IdName]:
    return [IdName(id=task["id"], name=task["name"]) for task in config["tasks"]]