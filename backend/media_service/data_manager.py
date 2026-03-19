import os
from typing import Any
import random

import torch
from datasets import load_from_disk
from PIL import Image as PILImage
import PIL
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
from matplotlib.animation import FFMpegWriter

from .config.manager import ConfigManager
from .config.data_kind import CheckpointFormat, DataKind
from shared.structs import Dataset, MediaFile
from shared.utils.functions import load_module

def load_dataset_huggingface(dataset_path: str):
    return load_from_disk(dataset_path)

def load_dataset_torch(dataset_path: str):
    return torch.load(dataset_path, weights_only=False)

def convert_to_file_format(full_path: str, data: Any, kind: str) -> MediaFile:
    if kind == DataKind.IMAGE:
        if type(data) == PILImage or type(data) == PIL.PngImagePlugin.PngImageFile:
            data.save(full_path)
        elif type(data) == Figure:
            data.savefig(full_path)
        else:
            raise ValueError(f"Unsupported object type: {type(data)}")
    elif kind == DataKind.VIDEO:
        if type(data) == type(FuncAnimation()):
            writer = FFMpegWriter(fps=4)
            data.save(full_path, writer=writer, dpi=100)
        else:
            raise ValueError(f"Unsupported object type: {type(data)}")


class DataManager:
    def __init__(self, media_files_path: str, model_path: str, config_manager: ConfigManager):
        self.media_files_path = media_files_path
        self.model_path = model_path
        self.config_manager = config_manager

        self.datasets: list[Dataset] = []
        self.datasets_by_id: dict[str, Dataset] = {}
        self.visualize = None

        self._load_datasets()
        self._load_visualizers()

    def _load_datasets(self) -> None:
        # datasets_by_id must store the loaded dataset (with `.data`),
        # not the DatasetConfig, otherwise callers can't access `.data`.
        for dataset_config in self.config_manager.config.datasets:
            dataset_path = dataset_config.path
            if not os.path.exists(dataset_path):
                raise FileNotFoundError(f"Dataset not found: {dataset_path}")
            if dataset_config.checkpoint_format == CheckpointFormat.HUGGINGFACE:
                data = load_dataset_huggingface(dataset_path)
            elif dataset_config.checkpoint_format == CheckpointFormat.TORCH_PT:
                data = load_dataset_torch(dataset_path)
            else:
                raise ValueError(
                    f"Unsupported checkpoint format: {dataset_config.checkpoint_format}"
                )

            dataset_obj = Dataset(id=dataset_config.id, data=data)
            self.datasets.append(dataset_obj)
            self.datasets_by_id[dataset_config.id] = dataset_obj

    def _load_visualizers(self) -> None:
        if len(self.config_manager.config.visualizers) == 0:
            return
        full_path = os.path.join(self.model_path, "src", "visualizer.py")
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Visualizer file not found: {full_path}")
        module = load_module(self.model_path, "visualizer", "visualizer.py")
        self.visualize = getattr(module, "visualize", None)
        if self.visualize is None:
            raise AttributeError(f"Module {full_path} has no 'visualize' function")

    def generate_media_file(self, dataset_id: str, index: int, key: str, modality_id: str, kind: DataKind, use_visualizer: bool) -> MediaFile:
        data = self.datasets_by_id[dataset_id].data[index][key]
        
        if use_visualizer:
            data = self.visualize(data, modality_id)

        rand_id = random.randint(0, 1000000)
        file_name = f"{modality_id}_{rand_id}"
        # Match the output container format to the kind.
        file_ext = ".png"
        if kind == DataKind.VIDEO:
            file_ext = ".mp4"
        file_name_extended = f"{file_name}{file_ext}"
        full_path = os.path.join(self.media_files_path, file_name_extended)

        convert_to_file_format(full_path, data, kind)

        return MediaFile(
            path=full_path,
            id=file_name,
            dataset_index=index,
        )