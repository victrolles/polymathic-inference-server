import type { SideArrowProps } from "../types/interfaces";

function SideArrowImage() {
    return (
        <svg width="40px" height="80px" viewBox="0 0 100 200" >
            <path d="M 90 100 L 10 10" strokeWidth="16" strokeLinecap="round" />
            <path d="M 90 100 L 10 190" strokeWidth="16" strokeLinecap="round" />
        </svg>
    );
}

function SideArrow({ showInformation, setShowInformation }: SideArrowProps) {

    const handleClick = () => {
        setShowInformation(!showInformation);
    }

    return (
        <div className="side-arrow" onClick={handleClick}>
            <div className={`side-arrow-image ${!showInformation ? "side-arrow-image-open" : ""}`}>
                <SideArrowImage />
            </div>
            {!showInformation && (
            <span className="tooltip-text">Show model <br /> information</span>
            )}
            {showInformation && (
                <span className="tooltip-text">Hide model <br /> information</span>
            )}
        </div>
    );
}

export default SideArrow;