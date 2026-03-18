export type MediaKind = 'image' | 'video' | 'audio' | 'text' | 'other';

export type MediaFileName = string;

export type MediaFile = {
    kind: MediaKind;
    path: string;
    id: string;
    dataset_index: number;
    name: MediaFileName;
}

export type MediaFileNames = MediaFileName[];

export type MediaFiles = MediaFile[];

export type mediaSize = {
    width: string;
    height: string;
}

export type selectableMediaFile = {
    mediaFile: MediaFile;
    isSelected: boolean;
}

export type SelectableMediaFiles = selectableMediaFile[];

export type ResultStatus = 'no' | 'loading' | 'done';

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

export type ModelTask = {
    model_name: string;
    task_name: string;
}

export type ModelSizeTaskId = {
    model_id: string;
    size_id: string;
    task_id: string;
}

export type ModelTasks = ModelTask[];

export type Dict = {
    [key: string]: any;
}

export type ConfigTasks = Dict[];