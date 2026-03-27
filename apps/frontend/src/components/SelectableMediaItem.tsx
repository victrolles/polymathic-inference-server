import { useEffect, useRef } from 'react';
import type { SelectableMediaItemProps } from "../types/interfaces";
import Freezeframe from 'freezeframe';

/** Freezeframe's destroy() only removes listeners; the .ff-container, canvas, and loading spinner stay on the DOM. */
function unwrapFreezeframeImage(img: HTMLImageElement | null) {
    if (!img) return;
    while (img.parentElement?.classList.contains("ff-container")) {
        const container = img.parentElement;
        const parent = container.parentElement;
        if (!parent) return;
        parent.insertBefore(img, container);
        container.remove();
    }
    img.classList.remove("ff-image");
}

function SelectableMediaItem({ media_file, display_name, is_selected, is_one_selected, kind, onClick, media_size }: SelectableMediaItemProps) {
    const imgRef = useRef<HTMLImageElement>(null);
    const freezeframeRef = useRef<Freezeframe | null>(null);

    useEffect(() => {
        const shouldFreeze = kind === "video" && !is_selected && is_one_selected;
        const img = imgRef.current;

        if (shouldFreeze && img) {
            freezeframeRef.current?.destroy();
            freezeframeRef.current = null;
            unwrapFreezeframeImage(img);
            freezeframeRef.current = new Freezeframe(img, { responsive: false, warnings: false });
        } else {
            freezeframeRef.current?.destroy();
            freezeframeRef.current = null;
            unwrapFreezeframeImage(img);
        }

        return () => {
            freezeframeRef.current?.destroy();
            freezeframeRef.current = null;
            unwrapFreezeframeImage(imgRef.current);
        };
    }, [kind, is_selected, is_one_selected]);

    return (
        <div className={`selectable-media-item${is_selected ? "-selected" : ""}${is_one_selected && !is_selected ? "-not-selected" : ""}`}>
            {display_name && <p className="selectable-media-item-name">{media_file.name}</p>}
            <img ref={imgRef} src={media_file.path} alt={media_file.name} onClick={onClick} style={{ width: media_size.width, height: media_size.height }} />
        </div>
    );
}

export default SelectableMediaItem;