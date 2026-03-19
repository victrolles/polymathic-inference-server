import type { Dict, IdName, MediaSize, ModelSizeTaskId, DatasetLocations, MediaKind, ModelsSizesTasks, SelectablePackets, Packets, MediaFile, Packet, Modality } from './types';

export interface MediaSelectorProps {
    selectable_packets: SelectablePackets;
    setSelectablePackets: (selectable_packets: SelectablePackets) => void;
    data_samples: Dict;
    media_size: Dict;
}

export interface SelectableMediaItemProps {
    media_file: MediaFile;
    display_name: boolean;
    is_selected: boolean;
    kind: MediaKind;
    onClick: () => void;
    media_size: MediaSize;
}
export interface MediaItemProps {
    media_file: MediaFile;
    display_name: boolean;
    kind: MediaKind;
    media_size: MediaSize;
}

export interface SubmitButtonProps {
    submitAction: () => void;
    submit_text: string;
}   

export interface InferenceRequestProps {
    model_size_task_id: ModelSizeTaskId;
    dataset_locations: DatasetLocations;
}

export interface ModelSelectorProps {
    models_sizes_tasks: ModelsSizesTasks;
    setIsModelSelectorOpen: (open: boolean) => void;
}

export interface SizeSelectorProps {
    model: IdName;
    sizes: IdName[];
    task: IdName;
    setIsModelSelectorOpen: (open: boolean) => void;
}

export interface PacketsContainerProps {
    packets: Packets;
    configDict: Dict;
    media_size: MediaSize;
}

export interface PacketItemProps {
    packet: Packet;
    configDict: Dict;
    media_size: MediaSize;
}

export interface ModalityItemProps {
    modality: Modality;
    configDict: Dict;
    media_size: MediaSize;
}