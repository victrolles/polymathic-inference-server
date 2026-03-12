import ImagesContainer from "../components/ImagesContainer";
import { getSelectedMediaFiles } from "../functions/functions";
import type { ImagesSelectorProps } from "../types/interfaces";

function ImageSelector({ mediaFiles, setMediaFiles, displaySelectedImage, imageSize, selectedImageSize, multipleSelection, displayName }: ImagesSelectorProps) {
    const selected = getSelectedMediaFiles(mediaFiles);
    return (
        <div className="image-selector">
            <ImagesContainer mediaFiles={mediaFiles} setMediaFiles={setMediaFiles} multipleSelection={multipleSelection} imageSize={imageSize} displayName={displayName} />
            {displaySelectedImage && (
                <div className="image-selector-image-container">
                    {selected.length > 0 ? (
                        selected.map((mediaFile) => (
                            <img key={mediaFile.name} className="image-selector-image" src={mediaFile.path} alt="Selected Image" style={{ width: selectedImageSize.width, height: selectedImageSize.height }} />
                        ))
                    ) : (
                        <p className="image-selector-text">{multipleSelection ? "Select multiple images" : "Select an image"}</p>
                    )}
                </div>
            )}
        </div>
    );
}

export default ImageSelector;