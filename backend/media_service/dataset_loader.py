import os

import torch
from datasets import load_from_disk

from .config.manager import ConfigManager
from .config.structs import DatasetConfig
from .config.structs import CheckpointFormat
from .scripts_loader import ScriptsLoader
from shared.structs import Dataset

def load_dataset_huggingface(dataset_path: str):
    return load_from_disk(dataset_path)

def load_dataset_torch(dataset_path: str):
    return torch.load(dataset_path, weights_only=False)

class DatasetLoader:
    def __init__(self, model_path: str, config_manager: ConfigManager, scripts_loader: ScriptsLoader):
        self.model_path = model_path
        self.config_manager = config_manager
        self.scripts_loader = scripts_loader

        self.datasets: list[Dataset] = []
        self.datasets_by_id: dict[str, Dataset] = {}

        self._load_datasets()

    def _load_datasets(self) -> None:
        for dataset_config in self.config_manager.config.datasets:
            dataset = self._load_dataset(dataset_config)
            self.datasets.append(dataset)
            self.datasets_by_id[dataset_config.id] = dataset

    def _load_dataset(self, dataset_config: DatasetConfig) -> Dataset:
        path = dataset_config.path
        if not os.path.exists(path):
            raise FileNotFoundError(f"Dataset not found: {path}")
        if dataset_config.checkpoint_format == CheckpointFormat.HUGGINGFACE:
            data = load_dataset_huggingface(path)
        elif dataset_config.checkpoint_format == CheckpointFormat.TORCH_PT:
            data = load_dataset_torch(path)
        else:
            raise ValueError(f"Unsupported checkpoint format: {dataset_config.checkpoint_format}")

        if dataset_config.dataset_formatter_id is not None:
            print(f"Dataset formatter detected: {dataset_config.dataset_formatter_id}")
            formatter = self.scripts_loader.dataset_formatters_by_id[dataset_config.dataset_formatter_id]
            data = formatter.callable(data)
            print(f"Dataset formatted: {data[0].keys()}")
            dataset_config.data_type_id = formatter.config.output_data_type_id

        return Dataset(id=dataset_config.id, data=data)