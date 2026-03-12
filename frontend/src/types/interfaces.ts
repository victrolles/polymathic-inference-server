import type { IdName, imageSize, MediaFile, MediaFileNames, MediaFiles, MediaType, ModelsSizesTasks, ModelTask } from './types';

export interface ImagesSelectorProps {
    mediaFiles: MediaFiles;
    setMediaFiles: (mediaFiles: MediaFiles) => void;
    displaySelectedImage: boolean;
    imageSize: imageSize;
    selectedImageSize: imageSize;
    multipleSelection: boolean;
    displayName: boolean;
    mediaType: MediaType;
}

export interface ImagesContainerProps {
    mediaFiles: MediaFiles;
    setMediaFiles: (mediaFiles: MediaFiles) => void;
    multipleSelection: boolean;
    displayName: boolean;
    imageSize: imageSize;
}

export interface ResultsContainerProps {
    mediaFiles: MediaFiles;
    multipleResults: boolean;
    dataHeight: number;
    selectedDataHeight: number;
    displaySelectedData: boolean;
    displayName: boolean;
    mediaType: MediaType;
}

export interface ImagesItemProps {
    image: MediaFile;
    displayName: boolean;
    isSelected: boolean;
    onClick: () => void;
    imageSize: imageSize;
}

export interface SubmitButtonProps {
    submitAction: () => void;
    submitText: string;
}

export interface InferenceProps {
    model_task: ModelTask;
}

export interface InferenceRequestProps {
    model_task: ModelTask;
    names: MediaFileNames;
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