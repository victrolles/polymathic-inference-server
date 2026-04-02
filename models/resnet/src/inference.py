import pickle

import torch
import torch.nn as nn
import torchvision.models as models
import torch.nn.functional as F

from python.templates.inference_base import InferenceBase

class Inference(InferenceBase):
    def __init__(self, size_id: str):
        self.size_id = size_id

        # Device
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Load subset
        path_to_subset = "/data/datasets/resnet/data.pkl"
        with open(path_to_subset, "rb") as f:
            self.subset = pickle.load(f)

        # Load model
        model = models.resnet18(weights=None)
        model.load_state_dict(torch.load("/data/weights/resnet/resnet18/resnet18.pth"))
        model.fc = nn.Identity()
        model.eval()
        self.model = model.to(self.device)

        # Precompute embeddings
        self._precompute_embeddings()

    def _embed(self, item: torch.Tensor) -> torch.Tensor:
        with torch.no_grad():
            emb = self.model(item)
            return F.normalize(emb, dim=1)

    def _precompute_embeddings(self):
        loader = torch.utils.data.DataLoader(
            dataset=[item["tensor"] for item in self.subset],    
            batch_size=32,
            num_workers=4,
            shuffle=False
        )
        embeddings = []
        for batch in loader:
            batch = batch.to(self.device)
            embedding = self._embed(batch)
            embeddings.append(embedding)
        self.embeddings_trch = torch.cat(embeddings, dim=0)

    def infer(self, data, task_id: str):
        input = data.to(self.device)
        input = input.unsqueeze(0)
        embedding = self._embed(input)
        sim = F.cosine_similarity(embedding, self.embeddings_trch, dim=1)
        similar_object = sim.argsort()[-2]
        return self.subset[similar_object]["image"]
