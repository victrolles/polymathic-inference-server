import type { MediaItemProps } from "../types/interfaces";

function MediaItem({ mediaFile, displayName, isSelected, onClick, mediaSize }: MediaItemProps) {
    return (
        <div className={`media-item${isSelected ? "-selected" : ""}`}>
            {displayName && <p className="media-item-name">{mediaFile.name}</p>}
            <img src={mediaFile.path} alt={mediaFile.name} onClick={onClick} style={{ width: mediaSize.width, height: mediaSize.height }} />
        </div>
    );
}

export default MediaItem;