import os
import yaml

from .structs import AppConfig
from .registry import ConfigRegistry
from .validation import validate_references
from .data_kind import REPRESENTATIONS_BY_ID

class ConfigManager:
    def __init__(self, media_files_path: str, model_path: str):

        self.config: AppConfig | None = None
        self.registry: ConfigRegistry | None = None

        

    def _load_config(self, media_files_path: str, model_path: str) -> None:
        full_path = os.path.join(model_path, "config.yaml")
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Config file not found: {full_path}")
        with open(full_path, "r", encoding="utf-8") as f:
            raw_config = yaml.safe_load(f)
            self.config = AppConfig.model_validate(raw_config)
            self.add_representation_to_config()

    def add_representation_to_config(self) -> None:
        for idx in range(len(self.config.data_types)):
            if self.config.data_types[idx].representation is not None:
                self.config.data_types[idx].representation = REPRESENTATIONS_BY_ID[self.config.data_types[idx].representation]

    def _load_registry(self) -> None:
        self.registry = ConfigRegistry(self.config)
        validate_references(self.registry)