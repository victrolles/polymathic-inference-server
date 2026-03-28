import ast
import random
import os
from typing import Any

import torch
from datasets import load_from_disk
from aion.codecs import CodecManager
from aion import AION
from sklearn.metrics.pairwise import cosine_similarity
from aion.modalities import Z

from utils import find_object_in_subset, prepare_query, prepare_queries, prepare_all_queries

from python.templates.inference_base import InferenceBase

class Inference(InferenceBase):
    def __init__(self, size_id: str):
        super().__init__(size_id)
        #Check if CUDA is available
        if torch.cuda.is_available():
            print("CUDA is available")
            self.device = torch.device("cuda")
        else:
            raise RuntimeError("CUDA is not available")

        # No gradient computation
        torch.set_grad_enabled(False)

        #Load the subset
        print("Loading the subset")
        subset_path = "/mnt/home/vgoudal/aion-inference/datasets/MultimodalUniverse/legacysurvey/subset_1000"
        self.subset = load_from_disk(subset_path)
        print("Subset loaded")

        # Decode the object_id from bytes to string: "b'0421p022-7410'" -> "0421p022-7410"
        # decoded_ids = [ast.literal_eval(oid).decode('utf-8') for oid in list(subset['object_id'])  ]
        # self.subset = subset.remove_columns('object_id').add_column('object_id', decoded_ids)

        #Load the codec manager
        print("Loading the codec manager")
        self.codec_manager = CodecManager(device=self.device)
        print("Codec manager loaded")

        #Load the model
        print("Loading the model")
        model_path = "/mnt/home/vgoudal/ceph/huggingface/models/polymathic-ai/aion-base"
        self.model = AION.from_pretrained(model_path)
        self.model.to(self.device)
        self.model.eval()
        print("Model loaded")

        print("Preparing all embeddings for similarity search on Legacy Survey subset")
        self._prepare_all_embeddings()
        print("All embeddings prepared")
        print("====== Ready to use ======")

    def _prepare_all_embeddings(self):
        all_tokens = prepare_all_queries(self.subset, self.codec_manager)
        all_embeddings = self.model.encode(all_tokens).cpu().numpy()
        self.all_embeddings = all_embeddings.reshape(all_embeddings.shape[0], -1)

    def _get_similarity_search(self, inputs: Any, number_of_images: int = 4) -> list:
        idx = find_object_in_subset(self.subset, inputs['object_id'])
        query_tokens = prepare_query(self.subset[idx], self.codec_manager)
        query_embedding = self.model.encode(query_tokens).cpu().numpy()
        query_embedding = query_embedding.reshape(1, -1)
        similarity_scores = cosine_similarity(query_embedding, self.all_embeddings)
        similar_objects = similarity_scores.argsort(axis=1)[:, ::-1][0][:number_of_images]
        similar_images = []
        for ids in similar_objects:
            similar_images.append(self.subset['rgb'][ids])
        return similar_images

    def _get_redshift_prediction(self, inputs: Any):
        tokens, new_object_ids = prepare_queries(inputs, self.codec_manager, [input['object_id'] for input in inputs])
        tokens_Z = self.model(tokens, target_modality=Z)
        predictions = torch.softmax(tokens_Z["tok_z"][:].squeeze(), 0).detach().cpu().numpy()
        return dict(
            predictions=predictions,
            object_ids=new_object_ids
        )

    def infer(self, input: Any, task_id: str):
        if task_id == "redshift-prediction":
            return self._get_redshift_prediction(input)
        elif task_id == "similarity-search":
            return self._get_similarity_search(input)
        else:
            raise ValueError(f"Unknown task ID: {task_id}")