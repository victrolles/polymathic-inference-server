from task_request import TaskRequestBase
from model_inference import ModelInference
from schemas import Media

class TaskRequestClass(TaskRequestBase):
    def __init__(self, model_inference: ModelInference, task_name: str):
        super().__init__(model_inference, task_name)

    def get_random_data_samples(self) -> list[Media]:
        print(f"Getting random data samples for {self.task_name}")
        medias = self.model_inference.get_random_data_samples(task_name=self.task_name)
        names = [m.name for m in medias]
        print(f"Sending random data samples: {names}")
        return medias

    def infer(self, list_media_names: list[str]) -> list[Media]:
        print(f"Inferring : {list_media_names}")
        medias = self.model_inference.get_redshift_prediction(list_media_names)
        names = [m.name for m in medias]
        print(f"Sending redshift prediction: {names}")
        return medias