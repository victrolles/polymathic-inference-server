from .structs import IdName
from .config_structs import AppConfig

def extract_model(config: AppConfig) -> IdName:
    return IdName(id=config.model.id, name=config.model.name)

def extract_sizes(config: AppConfig) -> list[IdName]:
    return [IdName(id=size.id, name=size.name) for size in config.sizes]

def extract_tasks(config: AppConfig) -> list[IdName]:
    return [IdName(id=task.id, name=task.name) for task in config.tasks]