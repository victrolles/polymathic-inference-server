import os
import random
from typing import Any

import yaml
from PIL.Image import Image as PILImage
from matplotlib.figure import Figure
import PIL.PngImagePlugin
import PIL.Image
from matplotlib.animation import FuncAnimation, FFMpegWriter

from .config_structs import AppConfig
from .structs import Model, Dataset
from .config_data_extractor import extract_model, extract_sizes, extract_tasks
from .config_registry import ConfigRegistry
from .config_validation import validate_references
from .utils import load_dataset_huggingface, load_dataset_torch, load_module, prints
from .data_kind import CheckpointFormat, REPRESENTATIONS_BY_ID, DataKind
from .structs import MediaFile

class DataManager:
    def __init__(self, media_files_path: str, model_path: str):
        self.media_files_path = media_files_path
        if not os.path.exists(media_files_path):
            os.makedirs(media_files_path)
        self.model_path = model_path

        self.datasets: list[Dataset] = []
        self.config: AppConfig | None = None
        self.registry: ConfigRegistry | None = None
        self.visualize = None

        prints("Loading config...")
        self._load_config()
        prints("Config loaded.")
        prints("Loading registry...")
        self._load_registry()
        prints("Registry loaded.")
        prints("Loading datasets...")
        self._load_datasets()
        prints("Datasets loaded.")
        prints("Loading visualizers...")
        self._load_visualizers()
        prints("Visualizers loaded.")

    

    def _load_datasets(self) -> None:
        for dataset in self.config.datasets:
            dataset_path = dataset.path
            if not os.path.exists(dataset_path):
                raise FileNotFoundError(f"Dataset not found: {dataset_path}")
            if dataset.checkpoint_format == CheckpointFormat.HUGGINGFACE:
                data = load_dataset_huggingface(dataset_path)
            elif dataset.checkpoint_format == CheckpointFormat.TORCH_PT:
                data = load_dataset_torch(dataset_path)
            else:
                raise ValueError(f"Unsupported checkpoint format: {dataset.checkpoint_format}")
            self.datasets.append(Dataset(id=dataset.id, data=data))

    def _load_visualizers(self) -> None:
        if len(self.config.visualizers) == 0:
            return
        full_path = os.path.join(self.model_path, "src", "visualizer.py")
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Visualizer file not found: {full_path}")
        module = load_module(full_path)
        self.visualize = getattr(module, "visualize", None)
        if self.visualize is None:
            raise AttributeError(f"Module {full_path} has no 'visualize' function")

    def get_model_sizes_tasks(self) -> Model:
        return Model(
            model=extract_model(self.config),
            sizes=extract_sizes(self.config),
            tasks=extract_tasks(self.config),
        )

    def get_config_task(self, task_id: str) -> dict:
        return self.registry.tasks_by_id[task_id].model_dump()

    def _get_dataset_and_column_for_task(self, task_id: str):
        task = self.registry.tasks_by_id[task_id]
        modality_id = task.data_samples.modality_id
        sample_size = task.data_samples.sample_size
        if not modality_id:
            raise ValueError(f"Task '{task_id}' has no data_samples.modality_id")
        modality = self.registry.modalities_by_id[modality_id]
        data_type_id = modality.data_type_id
        # Find a dataset whose data_type has a field with this data_type_id
        for ds_config in self.config.datasets:
            dt = self.registry.data_types_by_id[ds_config.data_type_id]
            for field in dt.fields:
                if field.data_type_id == data_type_id:
                    dataset = next((d for d in self.datasets if d.id == ds_config.id), None)
                    if dataset is None:
                        raise FileNotFoundError(f"Dataset '{ds_config.id}' not loaded")
                    return dataset, field.id, modality_id, sample_size
        raise ValueError(
            f"No dataset field found for task '{task_id}' modality '{modality_id}' (data_type_id={data_type_id})"
        )

    def convert_to_files_format(self, indices: list[int], obj: Any, kind: DataKind) -> Any:
        media_files = []
        if isinstance(obj, list):
            for idx, item in zip(indices, obj):
                media_files.append(self.convert_to_file_format(idx, item, kind))
        elif isinstance(obj, dict):
            for idx, item in zip(indices, obj.items()):
                media_files.append(self.convert_to_file_format(idx, item, kind))
        elif isinstance(obj, tuple):
            for idx, item in zip(indices, obj):
                media_files.append(self.convert_to_file_format(idx, item, kind))
        return media_files

    def convert_to_file_format(self, idx: int, obj: Any, kind: DataKind) -> MediaFile:
        rand_id = random.randint(0, 1000000)
        file_name = f"image_{rand_id}"
        file_name_extended = f"{file_name}.png"
        full_path = os.path.join(self.media_files_path, file_name_extended)
        if kind == DataKind.IMAGE:
            if type(obj) == PILImage or type(obj) == PIL.PngImagePlugin.PngImageFile:
                obj.save(full_path)
            elif type(obj) == Figure:
                obj.savefig(full_path)
            else:
                raise ValueError(f"Unsupported object type: {type(obj)}")
        elif kind == DataKind.VIDEO:
            if type(obj) == type(FuncAnimation()):
                writer = FFMpegWriter(fps=4)
                obj.save(full_path, writer=writer, dpi=100)
            else:
                raise ValueError(f"Unsupported object type: {type(obj)}")

        media_file = MediaFile(
            kind=kind,
            id=str(rand_id),
            dataset_index=idx,
            name=file_name,
            path=full_path,
        )
        return media_file

    def clear_media_files(self) -> None:
        for file in os.listdir(self.media_files_path):
            os.remove(os.path.join(self.media_files_path, file))
        prints(f"Cleared media files from {self.media_files_path}")

    def get_random_data_samples(self, task_id: str) -> list[MediaFile]:
        self.clear_media_files()
        dataset, column_name, _, sample_size = self._get_dataset_and_column_for_task(task_id)
        data = dataset.data
        n = len(data)
        size = min(sample_size, n)
        indices = random.sample(range(n), size)
        elements = []
        for idx in indices:
            row = data[idx]
            obj = row[column_name]
            elements.append(obj)

        task = self.registry.tasks_by_id[task_id]
        modality_id = task.data_samples.modality_id
        media_modality = self.registry.modalities_by_id[modality_id]
        media_data_type_id = media_modality.data_type_id
        media_data_type = self.registry.data_types_by_id[media_data_type_id]
        media_kind = media_data_type.kind
        media_files = self.convert_to_files_format(indices, elements, media_kind)
        return media_files