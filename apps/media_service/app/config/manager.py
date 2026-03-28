import os
import yaml

from .registry import ConfigRegistry
from .representations import REPRESENTATIONS_BY_ID

from python.structs.general import IdName
from python.enums import DataKind
from python.structs.config import AppConfig, TaskConfig
from python.functions.validation import validate_references


class ConfigManager:
    def __init__(self, model_path: str):

        self.config: AppConfig | None = None
        self.registry: ConfigRegistry | None = None

        self._load_config(model_path)
        self._load_registry()

    def _load_config(self, model_path: str) -> None:
        full_path = os.path.join(model_path, "config.yaml")
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Config file not found: {full_path}")
        with open(full_path, "r", encoding="utf-8") as f:
            raw_config = yaml.safe_load(f)
            self.config = AppConfig.model_validate(raw_config)
            self._add_representation_to_config()

    def _add_representation_to_config(self) -> None:
        for idx in range(len(self.config.data_types)):
            if self.config.data_types[idx].representation is not None:
                self.config.data_types[idx].representation = REPRESENTATIONS_BY_ID[self.config.data_types[idx].representation]

    def _load_registry(self) -> None:
        self.registry = ConfigRegistry(self.config)
        validate_references(self.registry)

    def extract_ids_and_names(self, key: str) -> list[IdName] | IdName:
        elem = getattr(self.config, key, None)
        if elem is None:
            raise ValueError(f"Element {key} not found in config")

        if isinstance(elem, list):
            return [IdName(id=item.id, name=item.name) for item in elem]

        if hasattr(elem, "id") and hasattr(elem, "name"):
            return IdName(id=elem.id, name=elem.name)

        if isinstance(elem, dict):
            return IdName(id=elem["id"], name=elem["name"])

        raise ValueError(f"Element {key} is not a supported config shape")

    def get_modality_ids_by_task_id_and_phase(self, task_id: str, phase: str) -> list[str]:
        modality_ids: list[str] = []
        task: TaskConfig = self.registry.tasks_by_id[task_id]

        # data_samples
        if phase == "data_samples":
            # data_samples
            modality_ids.append(task.data_samples.modality_id)
            # selected_data_samples
            if task.selected_data_samples.display:
                if task.selected_data_samples.display_multiple_modalities_simultaneously:
                    modality_ids.extend(task.selected_data_samples.modality_ids)
                else:
                    modality_ids.append(task.selected_data_samples.modality_id)

        # data_outputs
        if phase == "data_outputs":
            if task.data_outputs.display_multiple_modalities_simultaneously:
                modality_ids.extend(task.data_outputs.modality_ids)
            else:
                modality_ids.append(task.data_outputs.modality_id)
            if task.data_outputs.enable_switch_modalities:
                modality_ids.extend(task.data_outputs.switch_modality_ids)

        # delete duplicates
        modality_ids = list(set(modality_ids))

        return modality_ids

    def get_kind_by_modality_id(self, modality_id: str) -> DataKind:
        data_type_id = self.registry.modalities_by_id[modality_id].data_type_id
        return DataKind(self.registry.data_types_by_id[data_type_id].kind)

    def get_kind_by_data_type_id(self, data_type_id: str) -> DataKind:
        return DataKind(self.registry.data_types_by_id[data_type_id].kind)