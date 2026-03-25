from enum import Enum
from dataclasses import dataclass

import numpy as np
import torch
from PIL.Image import Image as PILImage
from matplotlib.figure import Figure
from matplotlib.animation import Animation
import PIL.PngImagePlugin

class CheckpointFormat(str, Enum):
    TORCH_PT = "torch_pt"
    HUGGINGFACE = "huggingface"
    SAFETENSORS = "safetensors"
    ONNX = "onnx"
    

class DataKind(str, Enum):
    TENSOR = "tensor"
    DICTIONARY = "dictionary"
    IMAGE = "image"
    LIST = "list"
    VIDEO = "video"
    AUDIO = "audio"
    TEXT = "text"
    OTHER = "other"

@dataclass(frozen=True)
class Representation:
    id: str
    python_path: str
    python_types: tuple[type, ...]

REPRESENTATIONS = {
    "numpy_array": Representation(
        id="numpy_array",
        python_path="numpy.ndarray",
        python_types=(np.ndarray,),
    ),
    "torch_tensor": Representation(
        id="torch_tensor",
        python_path="torch.Tensor",
        python_types=(torch.Tensor,),
    ),
    "pil_image": Representation(
        id="pil_image",
        python_path="PIL.Image.Image",
        python_types=(PILImage, PIL.PngImagePlugin.PngImageFile),
    ),
    "matplotlib_figure": Representation(
        id="matplotlib_figure",
        python_path="matplotlib.figure.Figure",
        python_types=(Figure,),
    ),
    "matplotlib_animation": Representation(
        id="matplotlib_animation",
        python_path="matplotlib.animation.Animation",
        python_types=(Animation,),
    ),
    "python_dict": Representation(
        id="python_dict",
        python_path="dict",
        python_types=(dict,),
    ),
    "python_list": Representation(
        id="python_list",
        python_path="list",
        python_types=(list,),
    ),
}

REPRESENTATIONS_BY_ID = {v.id: v for v in REPRESENTATIONS.values()}

DATA_KIND_REPRESENTATIONS = {
    DataKind.TENSOR: [
        "numpy_array",
        "torch_tensor",
    ],
    DataKind.DICTIONARY: [
        "python_dict",
    ],
    DataKind.IMAGE: [
        "pil_image",
        "matplotlib_figure",
        "numpy_array",
    ],
    DataKind.LIST: [
        "python_list",
    ],
    DataKind.VIDEO: [
        "matplotlib_animation",
    ],
}