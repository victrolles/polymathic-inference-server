import anim_spinner from "../assets/anim_spinner.svg";
import type { MediaSize } from "../types/types";

function LoadingItem({ media_size }: { media_size: MediaSize }) {
    return (
        <div className="media-item">
            <div className="media-item-content" style={{ width: media_size.width, height: media_size.height }}>
                <img src={anim_spinner} alt="Loading" className="loading-image" />
            </div>
        </div>
    );
}

export default LoadingItem;