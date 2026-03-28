from abc import ABC, abstractmethod

class InferenceBase(ABC):
    def __init__(self, size_id: str):
        self.size_id = size_id

    @abstractmethod
    def infer(self, input, task_id: str):
        """Infer the model"""
        ...