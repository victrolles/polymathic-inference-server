export type MediaKind = 'image' | 'video' | 'audio' | 'text' | 'other';

export type ModelSizeTaskId = {
    model_id: string;
    size_id: string;
    task_id: string;
}

export type MediaFile = {
    id: string;
    name: string;
    path: string;
}

export type DatasetLocation = {
    id: string;
    index: number;
}

export type DatasetLocations = DatasetLocation[];

export type Modality = {
    id: string;
    name: string;
    kind: MediaKind;
    media_file: MediaFile;
}

export type Packet = {
    origin: ModelSizeTaskId | DatasetLocation;
    modalities: Modality[];
}

export type Packets = Packet[];

export type MediaSize = {
    width: string;
    height: string;
}

export type SelectablePacket = {
    packet: Packet;
    is_selected: boolean;
}

export type SelectablePackets = SelectablePacket[];

export type Status = 'no' | 'loading' | 'done' | 'error';

export type IdName = {
    id: string;
    name: string;
}

export type ModelSizesTasks =  {
    model: IdName;
    sizes: IdName[];
    tasks: IdName[];
}

export type ModelsSizesTasks = ModelSizesTasks[];

export type Dict = {
    [key: string]: any;
}

export type ConfigTasks = Dict[];