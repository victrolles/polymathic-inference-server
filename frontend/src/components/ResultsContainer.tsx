import { useEffect, useState } from "react";
import type { ResultsContainerProps } from "../types/interfaces";
import type { MediaFile } from "../types/types";

function ResultsContainer({ mediaFiles, multipleResults, dataHeight, selectedDataHeight, displaySelectedData, displayName }: ResultsContainerProps) {
    const [remainingSpace, setRemainingSpace] = useState<string>("");
    const [dataHeightStyle, setDataHeightStyle] = useState<string>("");
    
    useEffect(() => {
        const height2 = `${selectedDataHeight} - 20px`;
        const newRemainingSpace = `calc(100vh - ${dataHeight} - ${displaySelectedData ? height2 : "0px"} - ${multipleResults ? "30px" : "0px"} - 300px)`;
        setRemainingSpace(newRemainingSpace);
        setDataHeightStyle(`${displayName ? '85%' : '100%'}`);
    }, [dataHeight, selectedDataHeight, displaySelectedData, displayName]);
    return (
        <div className={`results-container ${multipleResults ? "results-multiple-datas" : "results-single-data"}` } style={{ height: remainingSpace }}>
            {mediaFiles.map((mediaFile: MediaFile) => (
                <div key={mediaFile.name} className="results-item">
                    <img className="results-data" src={mediaFile.path} alt="Result data" style={{ height: dataHeightStyle }} />
                    {displayName && <p className="results-name">{mediaFile.name}</p>}
                </div>
            ))}
        </div>
    );
}

export default ResultsContainer;