from enum import Enum

class CheckpointFormat(str, Enum):
    TORCH_PT = "torch_pt"
    HUGGINGFACE = "huggingface"
    SAFETENSORS = "safetensors"
    ONNX = "onnx"
    PICKLE = "pickle"

class DataKind(str, Enum):
    TENSOR = "tensor"
    DICTIONARY = "dictionary"
    IMAGE = "image"
    LIST = "list"
    VIDEO = "video"
    AUDIO = "audio"
    TEXT = "text"
    OTHER = "other"