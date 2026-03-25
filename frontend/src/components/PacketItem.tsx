import type { PacketItemProps } from "../types/interfaces";
import ModalityItem from "./ModalityItem";
import { useEffect, useState } from "react";
import type { Modality } from "../types/types";
function PacketItem({ packet, configDict, media_size }: PacketItemProps) {
    const [switchable_modalities, setSwitchableModalities] = useState<Modality[] | null>(null);

    useEffect(() => {
        if (configDict.enable_switch_modalities) {
            setSwitchableModalities(packet.modalities.filter((modality) => configDict.switch_modality_ids.includes(modality.id)));
        }
    }, [configDict.enable_switch_modalities, packet.modalities, configDict.switch_modality_ids]);

    return (
        <div className="packet-item">
            {packet.modalities.map((modality) =>
                (configDict.display_multiple_modalities_simultaneously &&
                    configDict.modality_ids.includes(modality.id)) ||
                !configDict.display_multiple_modalities_simultaneously ? (
                    <ModalityItem
                        key={modality.media_file.id}
                        switchable_modalities={switchable_modalities}
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