import type { MediaItemProps } from "../types/interfaces";

function MediaItem({ media_file, display_name, media_size }: MediaItemProps) {
    return (
        <div className="media-item">
            {display_name && <p className="media-item-name">{media_file.name}</p>}
            {<img src={media_file.path} alt={media_file.name} style={{ width: media_size.width, height: media_size.height }} />}
        </div>
    );
}

export default MediaItem;