import type { SelectableMediaItemProps } from "../types/interfaces";

function SelectableMediaItem({ media_file, display_name, is_selected, kind, onClick, media_size }: SelectableMediaItemProps) {
    return (
        <div className={`selectable-media-item${is_selected ? "-selected" : ""}`}>
            {display_name && <p className="selectable-media-item-name">{media_file.name}</p>}
            {<img src={media_file.path} alt={media_file.name} onClick={onClick} style={{ width: media_size.width, height: media_size.height }} />}
        </div>
    );
}

export default SelectableMediaItem;