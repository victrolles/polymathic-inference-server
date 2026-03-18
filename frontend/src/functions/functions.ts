import type { SelectableMediaFiles, selectableMediaFile } from "../types/types";


export function setMediaFileSelection(selectableMediaFiles: SelectableMediaFiles, selectableMediaFile: selectableMediaFile, multipleSelection: boolean) {
    if (multipleSelection) {
        return selectableMediaFiles.map((smf) => {
            if (smf.mediaFile.id === selectableMediaFile.mediaFile.id) {
                return { ...smf, isSelected: !smf.isSelected };
            }
            return smf;
        });
    } else {
        return selectableMediaFiles.map((smf) => {
            if (smf.mediaFile.id === selectableMediaFile.mediaFile.id) {
                return { ...smf, isSelected: true };
            }
            return { ...smf, isSelected: false };
        });
    }
}

export function getSelectedMediaFiles(selectableMediaFiles: SelectableMediaFiles) {
    return selectableMediaFiles.filter((smf) => smf.isSelected);
}

export function getSelectedMediaFileNames(selectableMediaFiles: SelectableMediaFiles): string[] {
    return selectableMediaFiles.filter((smf) => smf.isSelected).map((smf) => smf.mediaFile.name);
}