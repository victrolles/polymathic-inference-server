import torch
from torch import load
from typing import Dict

from python.templates.inference_base import InferenceBase

class Inference(InferenceBase):
    def __init__(self, size_id: str):
        self.size_id = size_id
        path = "/data/datasets/sol/item.pt"
        self.data = load(path, weights_only=False)

    def infer(self, input: Dict, task_id: str) -> torch.Tensor:
        return self.data['x_gen'][0].clone()