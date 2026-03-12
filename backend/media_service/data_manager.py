import os
from typing import Dict

import yaml

from .structs import Model
from .config_data_extractor import extract_model, extract_sizes, extract_tasks

class DataManager:
    def __init__(self, media_files_path: str, model_path: str):
        self.media_files_path = media_files_path
        self.model_path = model_path

        self._load_config()

    def _load_config(self) -> None:
        full_path = os.path.join(self.model_path, "config.yaml")
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Config file not found: {full_path}")
        with open(full_path, "r") as f:
            self.config: Dict = yaml.load(f, Loader=yaml.FullLoader)

    def get_model_sizes_tasks(self) -> Model:
        return Model(
            model=extract_model(self.config),
            sizes=extract_sizes(self.config),
            tasks=extract_tasks(self.config),
        )

    def get_config_dict(self) -> Dict:
        return self.config