import type { ModalityItemProps } from "../types/interfaces";
import MediaItem from "./MediaItem";

function ModalityItem({ modality, configDict, media_size }: ModalityItemProps) {
    return (
        <div className="modality-item">
            {configDict.display_modalities_names &&
            <p className="modality-item-name">{modality.name}</p>}
            <MediaItem
                key={modality.media_file.id}
                media_file={modality.media_file}
                display_name={false}
                kind={modality.kind}
                media_size={media_size}
            />
        </div>
    );
}

export default ModalityItem;