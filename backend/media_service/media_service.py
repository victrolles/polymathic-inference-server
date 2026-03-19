import os
import random

from .config.manager import ConfigManager
from .data_manager import DataManager
from shared.structs import ModelInfo, MediaFile, Packet, DatasetLocation, Modality
from .media_manager import MediaManager

def setup_paths(media_files_path: str, models_path: str, model_id: str) -> None:
    media_files_path = os.path.join(media_files_path, model_id)
    model_path = os.path.join(models_path, model_id)
    if not os.path.exists(media_files_path):
        os.makedirs(media_files_path)
    if not os.path.exists(model_path):
        os.makedirs(model_path)
    return media_files_path, model_path

class MediaService:
    def __init__(self, media_files_path: str, models_path: str, model_id: str):
        media_files_path, model_path = setup_paths(media_files_path, models_path, model_id)
        self.config_manager = ConfigManager(model_path)
        self.data_manager = DataManager(media_files_path, model_path, self.config_manager)
        self.media_manager = MediaManager(media_files_path)

    def get_model_sizes_tasks(self) -> ModelInfo:
        return ModelInfo(
            model=self.config_manager.extract_ids_and_names("model"),
            sizes=self.config_manager.extract_ids_and_names("sizes"),
            tasks=self.config_manager.extract_ids_and_names("tasks"),
        )

    def get_config_task(self, task_id: str) -> dict:
        return self.config_manager.registry.tasks_by_id[task_id].model_dump()

    def get_random_data_samples(self, task_id: str) -> list[MediaFile]:
        modality_ids = self.config_manager.get_modality_ids_by_task_id_and_phase(task_id, "data_samples")
        task = self.config_manager.registry.tasks_by_id[task_id]
        print(f"Modality IDs: {modality_ids}")
        packets: list[Packet] = []

        sample_indices: list[int] | None = None

        for idx, modality_id in enumerate(modality_ids):
            kind = self.config_manager.get_kind_by_modality_id(modality_id)
            if kind is None:
                raise ValueError(f"Kind {modality_id} not found")

            # Find path
            data_type_id = self.config_manager.registry.modalities_by_id[modality_id].data_type_id
            does_modality_use_visualizer, new_data_type_id = self.config_manager.does_modality_use_visualizer(data_type_id)
            if does_modality_use_visualizer:
                data_type_id = new_data_type_id
                print(f"Using visualizer")
            else:
                print(f"No visualizer")

            key: str | None = None
            tmp_data = None
            dataset_id_for_modality: str | None = None

            # Find which dataset/key holds data for this modality.
            for dataset_cfg in self.config_manager.registry.datasets_by_id.values():
                data_type_cfg = self.config_manager.registry.data_types_by_id[dataset_cfg.data_type_id]
                for field in data_type_cfg.fields:
                    if field.data_type_id == data_type_id:
                        key = field.id
                        dataset_id_for_modality = dataset_cfg.id
                        tmp_data = self.data_manager.datasets_by_id[dataset_id_for_modality].data
                        break
                if key is not None:
                    break

            if key is None or tmp_data is None or dataset_id_for_modality is None:
                raise ValueError(
                    f"Key {data_type_id} not found for modality {modality_id} in loaded datasets"
                )

            if idx == 0:
                # Sample indices once and reuse them across modalities so each packet
                # contains aligned items (same dataset index).
                n = min(task.data_samples.sample_size, len(tmp_data))
                sample_indices = random.sample(range(len(tmp_data)), n)

                for idx2, index in enumerate(sample_indices):
                    media_file = self.data_manager.generate_media_file(
                        dataset_id_for_modality,
                        index,
                        key,
                        modality_id,
                        kind,
                        does_modality_use_visualizer,
                    )
                    packets.append(
                        Packet(
                            origin=DatasetLocation(
                                id=dataset_id_for_modality,
                                index=index,
                            ),
                            modalities=[
                                Modality(
                                    id=modality_id,
                                    kind=kind,
                                    data=media_file,
                                )
                            ],
                        )
                    )
            else:
                if sample_indices is None:
                    raise RuntimeError("Internal error: sample_indices not initialized")

                for idx2, index in enumerate(sample_indices):
                    if index >= len(tmp_data):
                        continue
                    media_file = self.data_manager.generate_media_file(
                        dataset_id_for_modality,
                        index,
                        key,
                        modality_id,
                        kind,
                        does_modality_use_visualizer,
                    )
                    packets[idx2].modalities.append(
                        Modality(
                            id=modality_id,
                            kind=kind,
                            data=media_file,
                        )
                    )

        print(f"Packets: {packets}")
        return packets