import { setPacketSelection } from "../functions/functions";
import type { MediaSelectorProps } from "../types/interfaces";
import LoadingItem from "./LoadingItem";
import MediaItem from "./SelectableMediaItem";
import { useState, useEffect } from "react";

function MediaSelector({ selectable_packets, setSelectablePackets, data_samples, media_size }: MediaSelectorProps) {
    const [index_modality, setIndexModality] = useState<number>(0);

    useEffect(() => {
        if (selectable_packets.length === 0 || !data_samples.modality_id) return;
        setIndexModality(selectable_packets[0].packet.modalities.findIndex((modality) => modality.id === data_samples.modality_id));
    }, [selectable_packets]);

    return (
        <div className="media-selector">
            {selectable_packets.length === 0 &&
                Array.from({ length: Number(data_samples.sample_size) }).map((_, i) => (
                    <LoadingItem
                        key={i}
                        media_size={{ width: media_size.width, height: media_size.height }}
                    />
                ))}
            {selectable_packets.length > 0 && selectable_packets.map((sp) => (
                <MediaItem
                    key={sp.packet.modalities[index_modality].media_file.id}
                    media_file={sp.packet.modalities[index_modality].media_file}
                    display_name={data_samples.display_name}
                    is_selected={sp.is_selected}
                    kind={sp.packet.modalities[index_modality].kind}
                    onClick={() =>
                        setSelectablePackets(
                            setPacketSelection(
                                selectable_packets,
                                sp,
                                Boolean(data_samples.multiple_data_selection),
                                index_modality
                            )
                        )
                    }
                    media_size={{ width: media_size.width, height: media_size.height }}
                />
            ))}
        </div>
    );
}

export default MediaSelector;