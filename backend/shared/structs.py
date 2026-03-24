from pydantic import BaseModel
from typing import Any, Optional, Callable

from media_service.config.data_kind import DataKind
from media_service.config.structs import VisualizerConfig, PreprocessorConfig, PostprocessorConfig, DatasetFormatterConfig

class IdName(BaseModel):
    id: str
    name: str

class ServerInfo(BaseModel):
    url: str
    model_id: str
    size_id: Optional[str] = None

class ModelInfo(BaseModel):
    model: IdName
    sizes: list[IdName]
    tasks: list[IdName]

class TaskRequest(BaseModel):
    task_id: str

class ModelSizeTaskId(BaseModel):
    model_id: str
    size_id: str
    task_id: str

class ModelSizeTaskRequest(BaseModel):
    model_size_task_id: ModelSizeTaskId

# --------- DATA ---------

class DatasetLocation(BaseModel):
    id: str
    index: int

class MediaFile(BaseModel):
    id: str
    name: str
    path: str

class Modality(BaseModel):
    id: str
    name: str
    kind: DataKind
    media_file: MediaFile

class Packet(BaseModel):
    origin: ModelSizeTaskId | DatasetLocation
    modalities: list[Modality]

class Dataset(BaseModel):
    id: str
    data: Any

class InferenceRequest(BaseModel):
    model_size_task_id: ModelSizeTaskId
    dataset_locations: list[DatasetLocation]

class InferenceDataInput(BaseModel):
    input: Any
    task_id: str

class ScriptFunction(BaseModel):
    config : VisualizerConfig | PreprocessorConfig | PostprocessorConfig | DatasetFormatterConfig
    callable: Callable