from pydantic import BaseModel, Field, model_validator, field_serializer
from typing import Optional, Any

from .data_kind import CheckpointFormat

class NamedObject(BaseModel):
    id: str
    name: str

class DataField(BaseModel):
    id: str
    data_type_id: str

class ElementType(BaseModel):
    data_type_id: str

class DataTypeConfig(BaseModel):
    id: str
    kind: str
    representation: Optional[str] = None
    element_type: Optional[ElementType] = None
    fields: list[DataField] = Field(default_factory=list)

    @field_serializer("representation")
    def _serialize_representation(self, rep: Any):
        if rep is None:
            return None
        if isinstance(rep, str):
            return rep
        # Be robust: sometimes runtime code may attach a Representation object
        rep_id = getattr(rep, "id", None)
        if isinstance(rep_id, str):
            return rep_id
        return str(rep)

    @field_serializer("element_type")
    def _serialize_element_type(self, element_type: ElementType) -> str:
        if element_type is None:
            return None
        return element_type.data_type_id

class VisualizerIO(BaseModel):
    data_type_id: str

class VisualizerConfig(BaseModel):
    id: str
    input: VisualizerIO
    output: VisualizerIO

class DatasetConfig(BaseModel):
    id: str
    name: str
    path: str
    data_type_id: str
    checkpoint_format: CheckpointFormat
    
class ModalityConfig(BaseModel):
    id: str
    name: str
    data_type_id: str

class UISize(BaseModel):
    width: str
    height: str

class DataSamplesConfig(BaseModel):
    modality_id: str
    multiple_data_selection: bool = False
    sample_size: int = 10
    display_name: bool = False

class SwitchModalitiesConfig(BaseModel):
    modality_ids: list[str]
    default_modality_id: str


class DisplayDataConfig(BaseModel):
    display: bool = False
    display_name: bool = False
    display_modalities_names: bool = False
    display_multiple_modalities_simultaneously: bool = False
    display_multiple_results: bool = False
    enable_switch_modalities: bool = False
    modality_id: Optional[str] = None
    modality_ids: Optional[list[str]] = None
    switch_modality_ids: Optional[list[str]] = None

    @model_validator(mode="after")
    def validate_display(cls, values: "DisplayDataConfig") -> "DisplayDataConfig":
        if values.display:
            if values.display_multiple_modalities_simultaneously:
                if values.modality_ids is None:
                    raise ValueError(
                        "modality_ids must be provided when display_multiple_modalities_simultaneously is True"
                    )
            else:
                if values.modality_id is None:
                    raise ValueError(
                        "modality_id must be provided when display_multiple_modalities_simultaneously is False"
                    )
            if values.enable_switch_modalities:
                if values.switch_modality_ids is None:
                    raise ValueError(
                        "switch_modality_ids must be provided when enable_switch_modalities is True"
                    )
        return values

class InferenceConfig(BaseModel):
    input: VisualizerIO
    output: VisualizerIO

class TaskUIConfig(BaseModel):
    text_top_screen: str
    data_size: UISize
    selected_data_size: Optional[UISize] = None
    output_data_size: UISize
    submit_button_text: str

class TaskConfig(BaseModel):
    id: str
    name: str
    data_samples: DataSamplesConfig
    selected_data_samples: DisplayDataConfig
    data_outputs: DisplayDataConfig
    ui: TaskUIConfig
    inference: InferenceConfig
    
    @model_validator(mode="after")
    def sync_selected_display_multiple_results(cls, values: "TaskConfig") -> "TaskConfig":
        """display_multiple_results (selected) suit multiple_data_selection (data_samples)."""
        expected = values.data_samples.multiple_data_selection
        raw = values.selected_data_samples.model_dump()
        raw["display_multiple_results"] = expected
        synced = DisplayDataConfig.model_validate(raw)
        return values.model_copy(update={"selected_data_samples": synced})

    @model_validator(mode="after")
    def force_data_outputs_display_true(cls, values: "TaskConfig") -> "TaskConfig":
        """Les sorties sont toujours affichées : display forcé à True."""
        raw = values.data_outputs.model_dump()
        raw["display"] = True
        return values.model_copy(
            update={"data_outputs": DisplayDataConfig.model_validate(raw)}
        )

class ModelConfig(BaseModel):
    id: str
    name: str

class AppConfig(BaseModel):
    model: ModelConfig
    sizes: list[NamedObject]
    data_types: list[DataTypeConfig]
    visualizers: list[VisualizerConfig]
    datasets: list[DatasetConfig]
    modalities: list[ModalityConfig]
    tasks: list[TaskConfig]