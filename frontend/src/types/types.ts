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

export type ModelTask = {
    model_name: string;
    task_name: string;
}

export type ModelTasks = ModelTask[];

export type ConfigDict = {
    [key: string]: any;
}