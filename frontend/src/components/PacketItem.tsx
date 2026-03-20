import type { PacketItemProps } from "../types/interfaces";
import ModalityItem from "./ModalityItem";

function PacketItem({ packet, configDict, media_size }: PacketItemProps) {
    return (
        <div className="packet-item">
            {packet.modalities.map((modality) =>
                (configDict.display_multiple_modalities_simultaneously &&
                    configDict.modality_ids.includes(modality.id)) ||
                !configDict.display_multiple_modalities_simultaneously ? (
                    <ModalityItem
                        key={modality.media_file.id}
                        modality={modality}
                        configDict={configDict}
                        media_size={media_size}
                    />
                ) : null
            )}
        </div>
    );
}

export default PacketItem;