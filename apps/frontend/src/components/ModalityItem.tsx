import { useEffect, useState } from "react";
import type { ModalityItemProps } from "../types/interfaces";
import DropList from "./DropList";
import MediaItem from "./MediaItem";
import type { Modality } from "../types/types";
import DropBox from "./DropBox";

function ModalityItem({ modality, switchable_modalities, configDict, media_size }: ModalityItemProps) {
    const [current_modality, setCurrentModality] = useState<Modality>(modality);

    return (
        <div className="modality-item">
            {configDict.display_modalities_names &&
            <p className="modality-item-name">{current_modality.name}</p>}
            <MediaItem
                key={current_modality.media_file.id}
                media_file={current_modality.media_file}
                display_name={configDict.display_name}
                kind={current_modality.kind}
                media_size={media_size}
            />
            {configDict.enable_switch_modalities && <DropBox
                    setCurrentModality={setCurrentModality}
                    switchable_modalities={switchable_modalities}
                />
            }
        </div>
    );
}

export default ModalityItem;