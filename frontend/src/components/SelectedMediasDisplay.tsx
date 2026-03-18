import type { SelectedMediasDisplayProps } from "../types/interfaces";
import MediaItem from "./MediaItem";

function SelectedMediasDisplay({ selectableMediaFiles, selectedDataSamples, mediaSize }: SelectedMediasDisplayProps) {

    console.log("selectableMediaFiles", selectableMediaFiles);

    if (!selectedDataSamples.display) {
        return null;
    }
    return (
        <div className="selected-medias-display">
            {selectableMediaFiles.map((smf) => (smf.isSelected && (
                <MediaItem
                key={smf.mediaFile.id}
                mediaFile={smf.mediaFile}
                displayName={false}
                isSelected={smf.isSelected}
                onClick={() => {}}
                mediaSize={{ width: mediaSize.width, height: mediaSize.height }}
                />
            )))}
        </div>
    );
}

export default SelectedMediasDisplay;