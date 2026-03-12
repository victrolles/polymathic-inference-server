export type MediaType = 'image' | 'video' | 'audio' | 'text' | 'other';

export type MediaFileName = string;

export type MediaFile = {
    type: MediaType;
    path: string;
    name: MediaFileName;
    isSelected: boolean;
}

export type MediaFileNames = MediaFileName[];

export type MediaFiles = MediaFile[];

export type imageSize = {
    width: string;
    height: string;
}

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

export type ConfigDict = {
    [key: string]: any;
}