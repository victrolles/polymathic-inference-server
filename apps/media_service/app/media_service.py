import os
import random
from typing import Any

from .config.manager import ConfigManager
from .data_manager import DataManager
from .media_manager import MediaManager
from .path_finder import StepType

from python.enums import DataKind
from python.structs.general import ModelInfo, Packet, DatasetLocation, Modality, ModelSizeTaskId

def setup_paths(media_files_path: str, models_path: str, datasets_path: str, model_id: str) -> None:
    media_files_path = os.path.join(media_files_path, model_id)
    model_path = os.path.join(models_path, model_id)
    datasets_path = os.path.join(datasets_path, model_id)
    if not os.path.exists(media_files_path):
        os.makedirs(media_files_path)
    if not os.path.exists(model_path):
        os.makedirs(model_path)
    if not os.path.exists(datasets_path):
        os.makedirs(datasets_path)
    return media_files_path, model_path, datasets_path

class MediaService:
    def __init__(self, media_files_path: str, models_path: str, datasets_path: str, model_id: str):
        media_files_path, model_path, datasets_path = setup_paths(media_files_path, models_path, datasets_path, model_id)
        self.config_manager = ConfigManager(model_path)
        self.data_manager = DataManager(media_files_path, model_path, datasets_path, self.config_manager)
        self.media_manager = MediaManager(media_files_path)
        

    def get_model_sizes_tasks(self) -> ModelInfo:
        return ModelInfo(
            model=self.config_manager.extract_ids_and_names("model"),
            sizes=self.config_manager.extract_ids_and_names("sizes"),
            tasks=self.config_manager.extract_ids_and_names("tasks"),
        )

    def get_config_task(self, task_id: str) -> dict:
        return self.config_manager.registry.tasks_by_id[task_id].model_dump()

    def get_model_information(self) -> dict:
        return self.config_manager.config.information

    def get_random_data_samples(self, task_id: str) -> list[Packet]:
        modality_ids = self.config_manager.get_modality_ids_by_task_id_and_phase(task_id, "data_samples")
        task = self.config_manager.registry.tasks_by_id[task_id]
        print(f"Modality IDs: {modality_ids}")
        packets: list[Packet] = []

        path = self.data_manager.path_finder.paths_dataset_to_modalities[(task_id, modality_ids[0])]
        dataset_id = path.steps[0].info.id
        tmp_data = self.data_manager.datasets.datasets_by_id[dataset_id].data
        length = len(tmp_data)
        n = min(task.data_samples.sample_size, length)
        sample_indices = random.sample(range(length), n)

        for idx_n in range(n):
            sample_index = sample_indices[idx_n]

            dataset_location = DatasetLocation(
                id=dataset_id,
                index=sample_index,
            )

            is_packet_cached = self.media_manager.has_index_dataset_been_cached(dataset_location)
            if is_packet_cached:
                print(f"Using cached packet for dataset location: {dataset_location}")

            modalities: list[Modality] = []
            for modality_id in modality_ids:
                path = self.data_manager.path_finder.paths_dataset_to_modalities[(task_id, modality_id)]
                data = None
                does_media_file_exist = False
                media_file = None
                for step in path.steps:
                    if step.step_type == StepType.DATASET:
                        data = self.data_manager.datasets.datasets_by_id[step.info.id].data[sample_index]
                    elif step.step_type == StepType.DICTIONARY:
                        data = data[step.info.key]
                    elif step.step_type == StepType.VISUALIZER:
                        data = self.data_manager.visualize(data, step.info.id, step.info.modality_id)

                modality_cfg = self.config_manager.registry.modalities_by_id[modality_id]
                kind = self.config_manager.registry.data_types_by_id[modality_cfg.data_type_id].kind
                if is_packet_cached:
                    does_media_file_exist, media_file = self.media_manager.get_media_files(dataset_location, modality_id)
                if not does_media_file_exist:
                    media_file = self.data_manager.generate_media_file(data, modality_cfg)
                else:
                    print(f"Using cached - skipping generation")
                modalities.append(Modality(
                    id=modality_id,
                    name=modality_cfg.name,
                    kind=kind,
                    media_file=media_file
                ))
            packet = Packet(
                origin=dataset_location,
                modalities=modalities
            )
            if not does_media_file_exist:
                print(f"Caching packet")
                self.media_manager.cache_packet(packet)

            packets.append(packet)
        return packets

    def pre_process_inference(self, task_id: str, dataset_locations: list[DatasetLocation]) -> Any:
        task = self.config_manager.registry.tasks_by_id[task_id]
        multiple_data_selection = task.data_samples.multiple_data_selection
        path = self.data_manager.path_finder.paths_dataset_to_inference[task_id]
        data = None
        for step in path.steps:
            if step.step_type == StepType.DATASET:
                if multiple_data_selection:
                    data = [self.data_manager.datasets.datasets_by_id[step.info.id].data[dataset_location.index] for dataset_location in dataset_locations]
                else:
                    data = self.data_manager.datasets.datasets_by_id[step.info.id].data[dataset_locations[0].index]
            elif step.step_type == StepType.DICTIONARY:
                if multiple_data_selection:
                    data = [data[i][step.info.key] for i in range(len(dataset_locations))]
                else:
                    data = data[step.info.key]
            elif step.step_type == StepType.PREPROCESSOR:
                if multiple_data_selection:
                    if self.config_manager.registry.data_types_by_id[step.input_output_type.input_data_type_id].kind == DataKind.LIST:
                        data = self.data_manager.preprocess(data)
                    else:
                        data = [self.data_manager.preprocess(data[i]) for i in range(len(dataset_locations))]
                else:
                    data = self.data_manager.preprocess(data)

        return data

    def post_process_inference(self, data: Any, mst: ModelSizeTaskId) -> Any:
        task = self.config_manager.registry.tasks_by_id[mst.task_id]
        display_multiple_results = task.data_outputs.display_multiple_results
        modality_ids = self.config_manager.get_modality_ids_by_task_id_and_phase(mst.task_id, "data_outputs")
        path = self.data_manager.path_finder.paths_inference_to_modalities[(mst.task_id, modality_ids[0])]
        packets: list[Packet] = []
        # Align types
        length = 0
        if display_multiple_results:
            if not isinstance(data, list):
                data = [data]
            length = len(data)
        else:
            if isinstance(data, list):
                data = data[0]

        # Apply postprocessors if needed
        if task.inference.postprocessor_id is not None:
            postprocessor = self.config_manager.registry.postprocessors_by_id[task.inference.postprocessor_id]

            if display_multiple_results:
                if self.config_manager.registry.data_types_by_id[postprocessor.input_data_type_id].kind == DataKind.LIST:
                    data = self.data_manager.postprocess(data, mst.task_id)
                else:
                    data = [self.data_manager.postprocess(data[i], mst.task_id) for i in range(length)]
                    
            else:
                data = self.data_manager.postprocess(data, mst.task_id)

        # Align data_type to visualizer
        for step in path.steps:
            if step.step_type == StepType.DICTIONARY:
                if display_multiple_results:
                    data = [data[i][step.info.key] for i in range(length)]
                else:
                    data = data[step.info.key]

        # Apply visualizers
        if not isinstance(data, list):
                data = [data]

        origin=ModelSizeTaskId(
            model_id=mst.model_id,
            size_id=mst.size_id,
            task_id=mst.task_id)

        for item in data:

            modalities: list[Modality] = []
            
            for modality_id in modality_ids:
                path = self.data_manager.path_finder.paths_inference_to_modalities[(mst.task_id, modality_id)]
                modified_item = item
                media_file = None
                for step in path.steps:
                    if step.step_type == StepType.DICTIONARY:
                        modified_item = modified_item[step.info.key]
                    elif step.step_type == StepType.VISUALIZER:
                        modified_item = self.data_manager.visualize(modified_item, step.info.id, step.info.modality_id)

                modality_cfg = self.config_manager.registry.modalities_by_id[modality_id]
                kind = self.config_manager.registry.data_types_by_id[modality_cfg.data_type_id].kind
                media_file = self.data_manager.generate_media_file(modified_item, modality_cfg)
                modalities.append(Modality(
                    id=modality_id,
                    name=modality_cfg.name,
                    kind=kind,
                    media_file=media_file
                ))
            packets.append(Packet(
                origin=origin,
                modalities=modalities
            ))
        return packets