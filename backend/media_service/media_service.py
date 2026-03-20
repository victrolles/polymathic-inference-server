import os
import random
from typing import Any

from .config.manager import ConfigManager
from .data_manager import DataManager, convert_to_file_format
from shared.structs import ModelInfo, Packet, DatasetLocation, Modality, DataKind, MediaFile, ModelSizeTaskId
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

    def get_random_data_samples(self, task_id: str) -> list[Packet]:
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
            does_modality_use_visualizer, new_data_type_id, _ = self.config_manager.does_modality_use_visualizer(data_type_id)
            if does_modality_use_visualizer:
                data_type_id = new_data_type_id

            key: str | None = None
            tmp_data = None
            dataset_id_for_modality: str | None = None

            # Find which dataset/key holds data for this modality.
            for dataset_cfg in self.config_manager.registry.datasets_by_id.values():
                data_type_cfg_list = self.config_manager.registry.data_types_by_id[dataset_cfg.data_type_id]
                data_type_cfg = self.config_manager.registry.data_types_by_id[data_type_cfg_list.element_type.data_type_id]
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
                n = min(task.data_samples.sample_size, len(tmp_data))
                sample_indices = random.sample(range(len(tmp_data)), n)
                print(f"Sample indices: {sample_indices}")
                self.media_manager.print_cache()

                for idx2, index in enumerate(sample_indices):
                    dataset_location = DatasetLocation(
                        id=dataset_id_for_modality,
                        index=index,
                    )
                    does_media_file_exist, media_file = self.media_manager.get_media_files(
                        dataset_location,
                        modality_id
                    )
                    if not does_media_file_exist:
                        media_file = self.data_manager.generate_media_file(
                            dataset_id_for_modality,
                            index,
                            key,
                            modality_id,
                            kind,
                            does_modality_use_visualizer,
                        )
                    else:
                        print(f"Using cached - skipping generation")
                    packet = Packet(
                        origin=dataset_location,
                        modalities=[Modality(
                            id=modality_id,
                            name=self.config_manager.registry.modalities_by_id[modality_id].name,
                            kind=kind,
                            media_file=media_file)]
                    )
                    packets.append(packet)
                    if not does_media_file_exist:
                        self.media_manager.cache_packet(packet)
            else:
                if sample_indices is None:
                    raise RuntimeError("Internal error: sample_indices not initialized")

                for idx2, index in enumerate(sample_indices):
                    if index >= len(tmp_data):
                        continue
                    dataset_location = DatasetLocation(
                        id=dataset_id_for_modality,
                        index=index,
                    )
                    does_media_file_exist, media_file = self.media_manager.get_media_files(
                        dataset_location,
                        modality_id
                    )
                    if not does_media_file_exist:
                        media_file = self.data_manager.generate_media_file(
                            dataset_id_for_modality,
                            index,
                            key,
                            modality_id,
                            kind,
                            does_modality_use_visualizer,
                        )
                    else:
                        print(f"Using cached - skipping generation")
                    modality = Modality(
                        id=modality_id,
                        name=self.config_manager.registry.modalities_by_id[modality_id].name,
                        kind=kind,
                        media_file=media_file
                    )
                    packets[idx2].modalities.append(modality)
                    if not does_media_file_exist:
                        packet = Packet(
                            origin=dataset_location,
                            modalities=[modality]
                        )
                        self.media_manager.cache_packet(packet)

        return packets

    def process_inference(self, task_id: str, dataset_locations: list[DatasetLocation]) -> Any:
        print(f"Task ID: {task_id}")
        for dataset_location in dataset_locations:
            print(f"Dataset location: {dataset_location}")

        task = self.config_manager.registry.tasks_by_id[task_id]
        input_data_type_id = task.inference.input.data_type_id
        print(f"Input data type ID: {input_data_type_id}")
        output_data_type_id = task.inference.output.data_type_id
        print(f"Output data type ID: {output_data_type_id}")

        input_data_type_cfg = self.config_manager.registry.data_types_by_id[input_data_type_id]
        print(f"Input data type cfg: {input_data_type_cfg}")
        output_data_type_cfg = self.config_manager.registry.data_types_by_id[output_data_type_id]
        print(f"Output data type cfg: {output_data_type_cfg}")

        multiple_input = False
        if input_data_type_cfg.kind == "list":
            multiple_input = True
            input_data_type_cfg = self.config_manager.registry.data_types_by_id[input_data_type_cfg.element_type.data_type_id]
            print(f"Input data type cfg2: {input_data_type_cfg}")


        # starting from dataset
        dataset_id = dataset_locations[0].id
        dataset_data_type = self.config_manager.registry.datasets_by_id[dataset_id].data_type_id
        dataset_data_type_cfg_list = self.config_manager.registry.data_types_by_id[dataset_data_type]
        dataset_data_type_cfg = self.config_manager.registry.data_types_by_id[dataset_data_type_cfg_list.element_type.data_type_id]

        if input_data_type_cfg != dataset_data_type_cfg:
            raise ValueError(f"Input data type cfg {input_data_type_cfg} does not match dataset data type cfg {dataset_data_type_cfg}")
        
        if multiple_input:
            input_data = []
            for dataset_location in dataset_locations:
                dataset_index = dataset_location.index
                print(f"Dataset index: {dataset_index}")
                dataset_data = self.data_manager.datasets_by_id[dataset_id].data[dataset_index]
                input_data.append(dataset_data)
        else:
            input_data = self.data_manager.datasets_by_id[dataset_id].data[dataset_locations[0].index]

        return input_data


    def post_process_inference(self, inference_result: Any, mst: ModelSizeTaskId) -> list[Packet]:
        packets: list[Packet] = []
        modality_ids = self.config_manager.get_modality_ids_by_task_id_and_phase(mst.task_id, "data_outputs")
        
        task = self.config_manager.registry.tasks_by_id[mst.task_id]
        input_data_type_id = task.inference.input.data_type_id
        print(f"Input data type ID: {input_data_type_id}")
        output_data_type_id = task.inference.output.data_type_id
        print(f"Output data type ID: {output_data_type_id}")

        input_data_type_cfg = self.config_manager.registry.data_types_by_id[input_data_type_id]
        print(f"Input data type cfg: {input_data_type_cfg}")
        output_data_type_cfg = self.config_manager.registry.data_types_by_id[output_data_type_id]
        print(f"Output data type cfg: {output_data_type_cfg}")

        input_kind = input_data_type_cfg.kind
        output_kind = output_data_type_cfg.kind

        if output_kind == "list":
            output_data_type_cfg = self.config_manager.registry.data_types_by_id[output_data_type_cfg.element_type.data_type_id]
            print(f"Output data type cfg: {output_data_type_cfg}")
        else:
            inference_result=[inference_result]

        for inference_result_item in inference_result:
            modalities: list[Modality] = []
            for modality_id in modality_ids:
                print(f"Modality ID: {modality_id}")

                data_type_id = self.config_manager.registry.modalities_by_id[modality_id].data_type_id
                does_modality_use_visualizer, input_visualizer_data_type_id, output_visualizer_data_type_id = self.config_manager.does_modality_use_visualizer(data_type_id)
                if does_modality_use_visualizer:
                    if input_visualizer_data_type_id == output_data_type_cfg.id:
                        print(f"use visualizer")
                        inference_result_item2 = self.data_manager.visualize(inference_result_item, modality_id)
                        output_data_type_cfg2 = self.config_manager.registry.data_types_by_id[output_visualizer_data_type_id]
                    else:
                        raise ValueError(f"Input visualizer data type ID {input_visualizer_data_type_id} does not match output data type cfg2 {output_data_type_cfg2.id}")
                else:
                    output_data_type_cfg2 = output_data_type_cfg
                    inference_result_item2 = inference_result_item


                if data_type_id == output_data_type_cfg2.id:
                    rand_id = random.randint(0, 1000000)
                    file_name = f"{modality_id}_{rand_id}"
                    # Match the output container format to the kind.
                    file_ext = ".png"
                    if output_data_type_cfg2.kind == DataKind.VIDEO:
                        file_ext = ".gif"
                    file_name_extended = f"{file_name}{file_ext}"
                    full_path = os.path.join(self.data_manager.media_files_path, file_name_extended)
                    print(f"save to {full_path}")
                    convert_to_file_format(full_path, inference_result_item2, output_data_type_cfg2.kind)
                    media_file = MediaFile(
                        path=full_path,
                        id=file_name,
                        name=file_name,
                    )
                    modality = Modality(
                        id=modality_id,
                        name=self.config_manager.registry.modalities_by_id[modality_id].name,
                        kind=output_data_type_cfg2.kind,
                        media_file=media_file
                    )
                    modalities.append(modality)
                else:
                    raise ValueError(f"Data type ID {data_type_id} does not match output data type cfg2 {output_data_type_cfg2.id}")

            packet = Packet(
                origin=ModelSizeTaskId(
                    model_id=mst.model_id,
                    size_id=mst.size_id,
                    task_id=mst.task_id),
                modalities=modalities
            )
            packets.append(packet)
        
        return packets