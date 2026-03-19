import type { PacketItemProps } from "../types/interfaces";
import ModalityItem from "./ModalityItem";

function PacketItem({ packet, configDict, media_size }: PacketItemProps) {
    return (
        <div className="packet-item">
            {packet.modalities.map((modality) => (
                <ModalityItem
                    key={modality.media_file.id}
                    modality={modality}
                    configDict={configDict}
                    media_size={media_size}
                />
            ))}
        </div>
    );
}

export default PacketItem;