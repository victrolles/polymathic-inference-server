import torch
from torch import load
from typing import Dict

from worker.template.inference_base import InferenceBase

class Inference(InferenceBase):
    def __init__(self, size_id: str):
        self.size_id = size_id
        path = "/mnt/home/vgoudal/polymathic-inference/aion-inference/datasets/sol/item.pt"
        self.data = load(path, weights_only=False)

    def infer(self, input: Dict, task_id: str) -> torch.Tensor:
        output = self.data['x_gen'][0]
        print(f"Shape of output: {output.shape}")
        return output