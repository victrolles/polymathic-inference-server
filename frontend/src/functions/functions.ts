import type { MediaFile, MediaFiles } from "../types/types";


export default function selectMediaFile(mediaFiles: MediaFiles, selectedMediaFile: MediaFile, multipleSelection: boolean) {
    if (multipleSelection) {
        return mediaFiles.map((mediaFile    ) => {
            if (mediaFile.name === selectedMediaFile.name) {
                return { ...mediaFile, isSelected: !mediaFile.isSelected };
            }
            return mediaFile;
        });
    } else {
        return mediaFiles.map((mediaFile) => {
            if (mediaFile.name === selectedMediaFile.name) {
                return { ...mediaFile, isSelected: true };
            }
            return { ...mediaFile, isSelected: false };
        });
    }
}

export function getSelectedMediaFiles(mediaFiles: MediaFiles) {
    return mediaFiles.filter((mediaFile) => mediaFile.isSelected);
}

export function getSelectedMediaFileNames(mediaFiles: MediaFiles): string[] {
    return mediaFiles.filter((mediaFile) => mediaFile.isSelected).map((mediaFile) => mediaFile.name);
}