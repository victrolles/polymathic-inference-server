from enum import Enum

from pydantic import BaseModel

from .config.manager import ConfigManager

from python.structs.config import DataTypeConfig
from python.enums import DataKind

class StepType(str, Enum):
    DATASET = "dataset"
    DICTIONARY = "dictionary"
    LIST = "list"
    VISUALIZER = "visualizer"
    PREPROCESSOR = "preprocessor"
    POSTPROCESSOR = "postprocessor"
    DATASET_FORMATTER = "dataset_formatter"
    START = "start"

class DatasetType(BaseModel):
    id: str

class DictionaryType(BaseModel):
    key: str

class ListType(BaseModel):
    element_type: str

class VisualizerType(BaseModel):
    id: str
    modality_id: str

class PreprocessorType(BaseModel):
    id: str

class PostprocessorType(BaseModel):
    id: str

class InputOutputType(BaseModel):
    input_data_type_id: str
    output_data_type_id: str

class Step(BaseModel):
    input_output_type: InputOutputType
    step_type: StepType
    info: DatasetType | DictionaryType | VisualizerType | PreprocessorType | PostprocessorType | ListType | None

class Path(BaseModel):
    steps: list[Step]

    def print_path(self) -> None:
        print(f"=============== Path: ===============")
        for step in self.steps:
            if step.step_type == StepType.DATASET:
                print(f"Dataset: {step.info.id}")
            elif step.step_type == StepType.LIST:
                print(f"List: {step.info.element_type}")
            elif step.step_type == StepType.DICTIONARY:
                print(f"Dictionary: {step.info.key}")
            elif step.step_type == StepType.VISUALIZER:
                print(f"Visualizer: {step.info.id}")
            elif step.step_type == StepType.PREPROCESSOR:
                print(f"Preprocessor: {step.info.id}")
            elif step.step_type == StepType.POSTPROCESSOR:
                print(f"Postprocessor: {step.info.id}")
            elif step.step_type == StepType.START:
                print(f"Start")
            print(f"    {step.input_output_type.input_data_type_id} -> {step.input_output_type.output_data_type_id}")
        print(f"====================================")
class Skip(BaseModel):
    step_type: StepType
    id: str

def reverse_path(path: Path) -> Path:
    return Path(steps=list(reversed(path.steps)))

class PathFinder:
    def __init__(self, model_path: str, config_manager: ConfigManager):
        self.model_path = model_path
        self.config_manager = config_manager

        self.paths_dataset_to_modalities: dict[tuple[str, str], Path] = {}
        self.paths_dataset_to_inference: dict[str, Path] = {}
        self.paths_inference_to_modalities: dict[tuple[str, str], Path] = {}

        self._find_all_paths()

    def _add_visualizer_step(self, path: Path, modality_id: str) -> Path:
        if self.config_manager.registry.visualizers_by_id is None:
            return path
        for visualizer in self.config_manager.registry.visualizers_by_id.values():
            if modality_id in visualizer.output_modalities:
                input_output_type = InputOutputType(
                    input_data_type_id=visualizer.input_data_type_id,
                    output_data_type_id=visualizer.output_data_type_id
                )
                visualizer_type = VisualizerType(
                    id=visualizer.id,
                    modality_id=modality_id
                )
                path.steps.append(Step(
                    input_output_type=input_output_type,
                    step_type=StepType.VISUALIZER,
                    info=visualizer_type
                ))
                # print(f"Added visualizer step: {visualizer.id} -> {modality_id}")
                return path
        return path

    def _add_preprocessor_step(self, path: Path, task_id: str) -> Path:
        if self.config_manager.registry.preprocessors_by_id is None:
            return path
        if self.config_manager.registry.tasks_by_id[task_id].inference.preprocessor_id is not None:
            preprocessor_id = self.config_manager.registry.tasks_by_id[task_id].inference.preprocessor_id
            preprocessor = self.config_manager.registry.preprocessors_by_id[preprocessor_id]
            input_output_type = InputOutputType(
                input_data_type_id=preprocessor.input_data_type_id,
                output_data_type_id=preprocessor.output_data_type_id
            )
            preprocessor_type = PreprocessorType(
                id=preprocessor.id)
            path.steps.append(Step(
                input_output_type=input_output_type,
                step_type=StepType.PREPROCESSOR,
                info=preprocessor_type
            ))
            return path
        return path

    def _add_postprocessor_step(self, path: Path, task_id: str) -> Path:
        if self.config_manager.registry.postprocessors_by_id is None:
            return path
        if self.config_manager.registry.tasks_by_id[task_id].inference.postprocessor_id is not None:
            postprocessor_id = self.config_manager.registry.tasks_by_id[task_id].inference.postprocessor_id
            postprocessor = self.config_manager.registry.postprocessors_by_id[postprocessor_id]
            input_output_type = InputOutputType(
                input_data_type_id=postprocessor.input_data_type_id,
                output_data_type_id=postprocessor.output_data_type_id
            )
            postprocessor_type = PostprocessorType(
                id=postprocessor.id
            )
            path.steps.append(Step(
                input_output_type=input_output_type,
                step_type=StepType.POSTPROCESSOR,
                info=postprocessor_type
            ))
            return path
        return path

    def _find_in_dictionary(self, path: Path, data_type: DataTypeConfig, data_type_id: str) -> Path:
        for field in data_type.fields:
            if field.data_type_id == data_type_id:
                dictionary_type = DictionaryType(
                    key=field.id
                )
                path.steps.append(Step(
                    input_output_type=InputOutputType(
                        input_data_type_id=data_type.id,
                        output_data_type_id=data_type_id
                    ),
                    step_type=StepType.DICTIONARY,
                    info=dictionary_type
                ))
                return path
        return path

    def _find_in_list(self, path: Path, data_type: DataTypeConfig, data_type_id: str) -> Path:
        if data_type.element_type is None:
            return path
        if data_type.id == data_type_id:
            for dataset in self.config_manager.registry.datasets_by_id.values():
                # print(f"Dataset: {dataset.data_type_id} == {data_type.id}")
                if dataset.data_type_id == data_type.id:
                    dataset_type = DatasetType(
                        id=dataset.id
                    )
                    path.steps.append(Step(
                        input_output_type=InputOutputType(
                            input_data_type_id=data_type.id,
                            output_data_type_id=data_type_id
                        ),
                        step_type=StepType.DATASET,
                        info=dataset_type
                    ))
                    # print(f"Added dataset step: {dataset.id} -> {data_type.id}")
                    return path
            return path
        if data_type.element_type.data_type_id == data_type_id:
            for dataset in self.config_manager.registry.datasets_by_id.values():
                # print(f"Dataset: {dataset.data_type_id} == {data_type.id}")
                if dataset.data_type_id == data_type.id:
                    dataset_type = DatasetType(
                        id=dataset.id
                    )
                    path.steps.append(Step(
                        input_output_type=InputOutputType(
                            input_data_type_id=data_type.id,
                            output_data_type_id=data_type_id
                        ),
                        step_type=StepType.DATASET,
                        info=dataset_type
                    ))
                    # print(f"Added dataset step: {dataset.id} -> {data_type.id}")
                    return path
            
            return path
        return path

    def _find_dataset(self, path: Path) -> Path:
        attempts = 0
        while attempts < 10:
            attempts += 1
            data_type_id = path.steps[-1].input_output_type.input_data_type_id
            # print(f"Data type ID: {data_type_id}")
            # print(f"Step type: {path.steps[-1].step_type}")
            if path.steps[-1].step_type == StepType.DATASET:
                # print(f"Found dataset step: {path.steps[-1].info.id}")
                return path
            else:
                for data_type in self.config_manager.registry.data_types_by_id.values():
                    if data_type.kind == DataKind.DICTIONARY:
                        self._find_in_dictionary(path, data_type, data_type_id)
                    elif data_type.kind == DataKind.LIST:
                        self._find_in_list(path, data_type, data_type_id)
        raise ValueError(f"Failed to find dataset for data type {data_type_id} after {attempts} attempts")

    def _align_data_types(self, path: Path, task_id: str) -> Path:
        attempts = 0
        target_data_type_id = None
        if self.config_manager.registry.postprocessors_by_id is not None:
            if self.config_manager.registry.tasks_by_id[task_id].inference.postprocessor_id is not None:
                postprocessor_id = self.config_manager.registry.tasks_by_id[task_id].inference.postprocessor_id
                target_data_type_id = self.config_manager.registry.postprocessors_by_id[postprocessor_id].output_data_type_id

        if target_data_type_id is None:
            target_data_type_id = self.config_manager.registry.tasks_by_id[task_id].inference.output_data_type_id
        # print(f"Target data type ID: {target_data_type_id}")

        while attempts < 10:
            attempts += 1
            for data_type in self.config_manager.registry.data_types_by_id.values():
                current_data_type_id = path.steps[-1].input_output_type.input_data_type_id
                # print(f"Current data type ID: {current_data_type_id}")
                if current_data_type_id == target_data_type_id:
                    return path
                if data_type.kind == DataKind.DICTIONARY:
                    self._find_in_dictionary(path, data_type, current_data_type_id)
                elif data_type.kind == DataKind.LIST:
                    if data_type.element_type.data_type_id == current_data_type_id:
                        list_type = ListType(
                            element_type=data_type.element_type.data_type_id
                        )
                        path.steps.append(Step(
                            input_output_type=InputOutputType(
                                input_data_type_id=data_type.id,
                                output_data_type_id=current_data_type_id
                            ),
                            step_type=StepType.LIST,
                            info=list_type
                        ))
                        # print(f"Added list step: {data_type.id} -> {current_data_type_id}")
                        
        raise ValueError(f"Failed to align data types for task {task_id} after {attempts} attempts")

    def _add_start_step_from_modality(self, modality_id: str) -> Path:
        data_type_id = self.config_manager.registry.modalities_by_id[modality_id].data_type_id
        step = Step(
            input_output_type=InputOutputType(
                input_data_type_id=data_type_id,
                output_data_type_id=data_type_id
            ),
            step_type=StepType.START,
            info=None
        )
        return Path(steps=[step])

    def _add_start_step_from_task(self, task_id: str) -> Path:
        data_type_id = self.config_manager.registry.tasks_by_id[task_id].inference.input_data_type_id
        step = Step(
            input_output_type=InputOutputType(
                input_data_type_id=data_type_id,
                output_data_type_id=data_type_id
            ),
            step_type=StepType.START,
            info=None
        )
        return Path(steps=[step])

    def _find_path_dataset_to_modalities(self, task_id: str) -> None:
        modality_ids = self.config_manager.get_modality_ids_by_task_id_and_phase(task_id, "data_samples")
        for modality_id in modality_ids:
            path = self._add_start_step_from_modality(modality_id)
            # print(f"Path: {path.steps}")
            path = self._add_visualizer_step(path, modality_id)
            # print(f"Path: {path.steps}")
            path = self._find_dataset(path)
            # print(f"Path: {path.steps}")
            self.paths_dataset_to_modalities[(task_id, modality_id)] = reverse_path(path)
            self.paths_dataset_to_modalities[(task_id, modality_id)].print_path()
    def _find_path_dataset_to_inference(self, task_id: str) -> None:
        path = self._add_start_step_from_task(task_id)
        path = self._add_preprocessor_step(path, task_id)
        path = self._find_dataset(path)
        self.paths_dataset_to_inference[task_id] = reverse_path(path)
        self.paths_dataset_to_inference[task_id].print_path()
    def _find_path_inference_to_modalities(self, task_id: str) -> None:
        modality_ids = self.config_manager.get_modality_ids_by_task_id_and_phase(task_id, "data_outputs")
        for modality_id in modality_ids:
            # print(f"Modality ID: {modality_id}")
            path = self._add_start_step_from_modality(modality_id)     
            # print(f"Path: {path.steps}")
            path = self._add_visualizer_step(path, modality_id)
            # print(f"Path: {path.steps}")
            path = self._align_data_types(path, task_id)
            # print(f"Path: {path.steps}")
            path = self._add_postprocessor_step(path, task_id)
            # print(f"Path: {path.steps}")
            self.paths_inference_to_modalities[(task_id, modality_id)] = reverse_path(path)
            self.paths_inference_to_modalities[(task_id, modality_id)].print_path()
    def _find_all_paths(self) -> None:
        for task_id in self.config_manager.registry.tasks_by_id.keys():
            print(f"Finding paths for task: {task_id}")
            self._find_path_dataset_to_modalities(task_id)
            print(f"Found paths for dataset to modalities for task: {task_id}")
            self._find_path_dataset_to_inference(task_id)
            print(f"Found paths for dataset to inference for task: {task_id}")
            self._find_path_inference_to_modalities(task_id)
            print(f"Found paths for inference to modalities for task: {task_id}")