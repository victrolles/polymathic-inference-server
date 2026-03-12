import ast
import random
import os

import torch
from datasets import load_from_disk
from aion.codecs import CodecManager
from aion import AION
from sklearn.metrics.pairwise import cosine_similarity
from aion.modalities import Z
import matplotlib.pyplot as plt

from utils import find_object_in_subset, prepare_query, prepare_queries, prepare_all_queries
from model_inference import ModelInference
from schemas import Media

class Inference(ModelInference):
    def __init__(self, media_files_path: str, model_name: str):
        super().__init__(media_files_path, model_name)
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
        subset = load_from_disk(subset_path)
        print("Subset loaded")

        # Decode the object_id from bytes to string: "b'0421p022-7410'" -> "0421p022-7410"
        decoded_ids = [ast.literal_eval(oid).decode('utf-8') for oid in list(subset['object_id'])  ]
        self.subset = subset.remove_columns('object_id').add_column('object_id', decoded_ids)

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

    def get_tasks_names(self) -> list[str]:
        return ["redshift-prediction", "similarity-search"]

    def _prepare_all_embeddings(self):
        all_tokens = prepare_all_queries(self.subset, self.codec_manager)
        all_embeddings = self.model.encode(all_tokens).cpu().numpy()
        self.all_embeddings = all_embeddings.reshape(all_embeddings.shape[0], -1)

    def get_random_data_samples(self, task_name: str) -> list[Media]:
        random_data_samples: list[Media] = []
        for _ in range(10):
            random_index = random.randint(0, len(self.subset) - 1)
            item = self.subset[random_index]
            file_name = f"image_{item['object_id']}.png"
            data_path = os.path.join(self.media_files_path, self.model_name, task_name)
            if not os.path.exists(data_path):
                os.makedirs(data_path)
            path = os.path.join(data_path, file_name)
            item['rgb'].save(path)
            media = Media(name=item['object_id'], path=path)
            random_data_samples.append(media)

        return random_data_samples

    def get_similarity_search(self, name: str, number_of_images: int = 4) -> list[Media]:
        print("====== Getting similar images ======")
        print("Find object in subset")
        data = find_object_in_subset(self.subset, name)
        print("Object found")

        print("Encoding object into embeddings")
        query_tokens = prepare_query(data, self.codec_manager)
        query_embedding = self.model.encode(query_tokens).cpu().numpy()
        query_embedding = query_embedding.reshape(1, -1)
        print("Object embeddings prepared")

        print("Calculate similarity scores")
        similarity_scores = cosine_similarity(query_embedding, self.all_embeddings)
        similar_objects = similarity_scores.argsort(axis=1)[:, ::-1][0][:number_of_images]
        print("Similar objects found")

        print("Get similar objects")
        similar_images: list[Media] = []
        for ids in similar_objects:
            image = self.subset['rgb'][ids]
            image.save(f"image_{ids}.png")
            name = f"similarity_search_{ids}"
            file_name = f"{name}.png"
            data_path = os.path.join(self.media_files_path, self.model_name, "similarity-search")
            if not os.path.exists(data_path):
                os.makedirs(data_path)
            path = os.path.join(data_path, file_name)
            image.save(path)
            media = Media(name=name, path=path)
            similar_images.append(media)
        return similar_images

    def get_redshift_prediction(self, object_ids: list[str]) -> list[Media]:
        print("====== Getting reshift predictions ======")
        print("Prepare queries")
        tokens, new_object_ids = prepare_queries(self.subset, self.codec_manager, object_ids)
        print("Queries prepared")

        print("forward pass queries")
        tokens_Z = self.model(tokens, target_modality=Z)
        print("Predictions obtained")

        print("Calculate predictions")
        predictions = torch.softmax(tokens_Z["tok_z"][:].squeeze(), 0).detach().cpu().numpy()
        print("Predictions calculated")

        for i in range(predictions.shape[0]):
            plt.plot(predictions[i], color="C%d" % i)
        plt.legend(new_object_ids)
        plt.xlim(-0, 150)
        # plt.ylim(0, 0.2)
        plt.xlabel("Tokenized Redshift")
        plt.ylabel("Probability")
        plt.title("AION Redshift Prediction for Photometry+Morphology")
        name = f"redshift_prediction_{'_'.join(new_object_ids)}"
        file_name = f"{name}.png"
        data_path = os.path.join(self.media_files_path, self.model_name, "redshift-prediction")
        if not os.path.exists(data_path):
            os.makedirs(data_path)
        path = os.path.join(data_path, file_name)
        plt.savefig(path)
        plt.close()
        media = Media(name=name, path=path)
        return [media]