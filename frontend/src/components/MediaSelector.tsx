import { setMediaFileSelection } from "../functions/functions";
import type { MediaSelectorProps } from "../types/interfaces";
import MediaItem from "./MediaItem";

function MediaSelector({ selectableMediaFiles, setSelectableMediaFiles, dataSamples, dataSize }: MediaSelectorProps) {
    return (
        <div className="media-selector">
            {selectableMediaFiles.map((smf) => (
                <MediaItem
                    key={smf.mediaFile.id}
                    mediaFile={smf.mediaFile}
                    displayName={dataSamples.display_name}
                    isSelected={smf.isSelected}
                    onClick={() =>
                        setSelectableMediaFiles(
                            setMediaFileSelection(
                                selectableMediaFiles,
                                smf,
                                Boolean(dataSamples.multiple_data_selection)
                            )
                        )
                    }
                    mediaSize={{ width: dataSize.width, height: dataSize.height }}
                />
            ))}
        </div>
    );
}

export default MediaSelector;