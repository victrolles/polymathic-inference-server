import os

from shared.structs import Packet, ModelSizeTaskId, DatasetLocation, MediaFile

class MediaManager:
    def __init__(self, media_files_path: str):
        self.media_files_path = media_files_path
        self.cached_packets: list[Packet] = []
        self.cached_packets_by_location: dict[tuple[str, int], Packet] = {}

        self.clear_cache()

    def clear_cache(self) -> None:
        self.cached_packets = []
        self.cached_packets_by_location = {}
        for file in os.listdir(self.media_files_path):
            os.remove(os.path.join(self.media_files_path, file))
        print(f"Cleared cache from {self.media_files_path}")

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

    def print_cache(self) -> None:
        print(f"Cached indices: {[x.origin.index for x in self.cached_packets]}")