import selectMediaFile from "../functions/functions";
import type { ImagesContainerProps, ImagesItemProps } from "../types/interfaces";

function ImagesItem({ image, displayName, isSelected, onClick, imageSize }: ImagesItemProps) {
    return (
        <div>
            {displayName && <p className="images-item-name">{image.name}</p>}
            <div className={`images-item${isSelected ? "-selected" : ""}`}>
                <img src={image.path} alt={image.name} onClick={onClick} style={{ width: imageSize.width, height: imageSize.height }} />
            </div>
        </div>
    );
}

function ImagesContainer({ mediaFiles, setMediaFiles, multipleSelection, imageSize, displayName }: ImagesContainerProps) {
    return (
        <div className="images-container">
            {mediaFiles.map((image) => (
                <ImagesItem
                    key={image.name}
                    image={image}
                    displayName={displayName}
                    isSelected={image.isSelected}
                    onClick={() => {setMediaFiles(selectMediaFile(mediaFiles, image, multipleSelection));}}
                    imageSize={imageSize}
                />
            ))}
        </div>
    );
}
  
export default ImagesContainer;