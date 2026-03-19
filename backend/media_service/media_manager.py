import os

from shared.structs import CachedFile

class MediaManager:
    def __init__(self, media_files_path: str):
        self.media_files_path = media_files_path
        self.cached_files: list[CachedFile] = []
        self.cached_files_by_dataset_index: dict[int, list[CachedFile]] = {}

        self.clear_cache()

    def clear_cache(self) -> None:
        self.cached_files = []
        self.cached_files_by_dataset_index = {}
        for file in os.listdir(self.media_files_path):
            os.remove(os.path.join(self.media_files_path, file))
        print(f"Cleared cache from {self.media_files_path}")

    def cache_file(self, file: str) -> None:
        pass