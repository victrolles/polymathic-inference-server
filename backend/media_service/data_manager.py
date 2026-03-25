import random
from typing import Any

from .config.manager import ConfigManager
from .config.structs import DataTypeConfig, ModalityConfig
from shared.structs import MediaFile
from .dataset_loader import DatasetLoader
from .scripts_loader import ScriptsLoader
from .media_converter import MediaConverter
from .path_finder import PathFinder

class DataManager:
    def __init__(self, media_files_path: str, model_path: str, config_manager: ConfigManager):
        self.media_files_path = media_files_path
        self.model_path = model_path
        self.config_manager = config_manager

        self.scripts = ScriptsLoader(model_path, config_manager)
        self.datasets = DatasetLoader(model_path, config_manager, self.scripts)
        self.media_converter = MediaConverter(media_files_path)
        self.path_finder = PathFinder(model_path, config_manager)

    def visualize(self, data: Any, visualizer_id: str, modality_id: str) -> Any:
        return self.scripts.visualizers_by_id[visualizer_id].callable(data, modality_id)

    def preprocess(self, data: Any, task_id: str) -> Any:
        return self.scripts.preprocessors_by_id[task_id].callable(data, task_id)

    def postprocess(self, data: Any, task_id: str) -> Any:
        return self.scripts.postprocessors_by_id[task_id].callable(data, task_id)

    def generate_media_file(self, data: Any, modality_config: ModalityConfig) -> MediaFile:
        rand_id = random.randint(0, 1000000)
        file_name = f"{modality_config.id}_{rand_id}"
        data_type_config: DataTypeConfig = self.config_manager.registry.data_types_by_id[modality_config.data_type_id]
        full_path = self.media_converter.save_object(data, file_name, data_type_config)

        return MediaFile(
            path=full_path,
            id=file_name,
            name=file_name,
        )