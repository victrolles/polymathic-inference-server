from pydantic import BaseModel
from media_service.data_kind import DataKind

class IdName(BaseModel):
    id: str
    name: str

class ServerInfo(BaseModel):
    url: str
    model_id: str
    size_id: str

class Model(BaseModel):
    model: IdName
    sizes: list[IdName]
    tasks: list[IdName]

class MediaFile(BaseModel):
    kind: DataKind
    id: str
    dataset_index: int
    name: str
    path: str

class ModelConfigTaskRequest(BaseModel):
    model_id: str
    size_id: str
    task_id: str

class ModelSizeTaskId(BaseModel):
    model_id: str
    size_id: str
    task_id: str

class ModelSizeTaskRequest(BaseModel):
    model_size_task_id: ModelSizeTaskId

class RandomDataSamplesRequest(BaseModel):
    model_size_task_id: ModelSizeTaskId

from pydantic import BaseModel
from typing import Any
from .data_kind import DataKind
class IdName(BaseModel):
    id: str
    name: str

class ServerInfo(BaseModel):
    url: str
    model_id: str
    size_id: str

class Model(BaseModel):
    model: IdName
    sizes: list[IdName]
    tasks: list[IdName]

class ModelConfigTaskRequest(BaseModel):
    task_id: str

class RandomDataSamplesRequest(BaseModel):
    task_id: str

class Dataset(BaseModel):
    id: str
    data: Any

class MediaFile(BaseModel):
    kind: DataKind
    id: str
    dataset_index: int
    name: str
    path: str

from pydantic import BaseModel
from dataclasses import dataclass, field
from typing import Dict, List, Union
from PIL import PngImagePlugin
import matplotlib.figure

class ServerInfo(BaseModel):
    url: str
    model_id: str
    size_id: str

class RandomDataSamplesRequest(BaseModel):
    input: dict
    task_id: str