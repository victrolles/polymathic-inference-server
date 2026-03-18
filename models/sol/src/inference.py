import torch
from typing import Dict

from worker.template.inference_base import InferenceBase

class Inference(InferenceBase):
    def __init__(self, size_id: str):
        self.size_id = size_id

    def infer(self, input: Dict, task_id: str) -> torch.Tensor:
        print("====== Infering ======")
        print("Task ID: ", task_id)
        return input['x_gen'][0]