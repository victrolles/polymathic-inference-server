import type { Dict, IdName, mediaSize, MediaFile, MediaFileNames, MediaFiles, MediaKind, ModelsSizesTasks, ModelTask, selectableMediaFile } from './types';

export interface MediaSelectorProps {
    selectableMediaFiles: selectableMediaFile[];
    setSelectableMediaFiles: (selectableMediaFiles: selectableMediaFile[]) => void;
    dataSamples: Dict;
    dataSize: Dict;
}

export interface SelectedMediasDisplayProps {
    selectableMediaFiles: selectableMediaFile[];
    selectedDataSamples: Dict;
    mediaSize: Dict;
}

export interface ImagesContainerProps {
    mediaFiles: MediaFiles;
    setMediaFiles: (mediaFiles: MediaFiles) => void;
    multipleSelection: boolean;
    displayName: boolean;
    mediaSize: mediaSize;
}

export interface ResultsContainerProps {
    mediaFiles: MediaFiles;
    multipleResults: boolean;
    dataHeight: number;
    selectedDataHeight: number;
    displaySelectedData: boolean;
    displayName: boolean;
    mediaKind: MediaKind;
}

export interface MediaItemProps {
    mediaFile: MediaFile;
    displayName: boolean;
    isSelected: boolean;
    onClick: () => void;
    mediaSize: mediaSize;
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