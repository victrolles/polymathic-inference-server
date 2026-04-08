import os
import shutil

from python.structs.general import Packet, ModelSizeTaskId, DatasetLocation, MediaFile
from shared.structs import Packet, ModelSizeTaskId, DatasetLocation, MediaFile
from shared.utils.functions import copy_file_to_path

class MediaManager:
    def __init__(self, media_files_path: str):
        self.media_files_path = media_files_path
        self.cached_packets: list[Packet] = []
        self.cached_packets_by_location: dict[tuple[str, int], Packet] = {}

        self.clear_all_cache()

    def clear_all_cache(self) -> None:
        self.cached_packets = []
        self.cached_packets_by_location = {}
        if os.path.exists(self.media_files_path):
            for name in os.listdir(self.media_files_path):
                path = os.path.join(self.media_files_path, name)
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
            print(f"Cleared all cache from {self.media_files_path}")
        else:
            print(f"Media files path does not exist: {self.media_files_path}")

    def cache_packet(self, packet: Packet) -> None:
        if isinstance(packet.origin, ModelSizeTaskId):
            return

        location = (packet.origin.id, packet.origin.index)
        cached_packet = self.cached_packets_by_location.get(location)
        if cached_packet is None:
            self.cached_packets.append(packet)
            self.cached_packets_by_location[location] = packet
        else:
            cached_modalities = [x.id for x in cached_packet.modalities]
            for modality in packet.modalities:
                if modality.id not in cached_modalities:
                    cached_packet.modalities.append(modality)
            self.cached_packets_by_location[location] = cached_packet

    def get_media_files(self, location: DatasetLocation, modality_id: str) -> [bool, MediaFile | None]:
        cached_packet = self.cached_packets_by_location.get((location.id, location.index))
        if cached_packet is None:
            return False, None
        for modality in cached_packet.modalities:
            if modality.id == modality_id:
                return True, modality.media_file
        return False, None

    def has_index_dataset_been_cached(self, location: DatasetLocation) -> bool:
        return (location.id, location.index) in self.cached_packets_by_location

    def print_cache(self) -> None:
        print(f"Cached indices: {[x.origin.index for x in self.cached_packets]}")

    def save_cover_image(self, cover_image_path: str) -> str:
        static_media_files_path = os.path.join(self.media_files_path, "static")
        if not os.path.exists(static_media_files_path):
            os.makedirs(static_media_files_path)
        new_cover_image_path = os.path.join(static_media_files_path, os.path.basename(cover_image_path))
        copy_file_to_path(cover_image_path, new_cover_image_path)
        return new_cover_image_path