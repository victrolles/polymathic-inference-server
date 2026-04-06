import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import InferenceContainer from "../components/InferenceContainer";
import SideArrowContainer from "../components/sideArrow";
import ShowInformation from "../components/ShowInformation";
import type { Dict } from "../types/types";
import { requestModelInformation } from "../requests/fast_api_requests";

function Inference() {
    const [showInformation, setShowInformation] = useState(false);
    const { model_id, size_id, task_id } = useParams();
    const [model_information, setModelInformation] = useState<Dict | null>(null);

    useEffect(() => {
        if (model_id && size_id && task_id) {

            // Reset variables
            setModelInformation(null);
            setShowInformation(false);

            requestModelInformation(model_id)
            .then((data: Dict) => {
                setModelInformation(data);
                console.log("model_information", data);
            }).catch((error) => {
                console.error(error);
            });
        }
    }, [model_id, size_id, task_id]);
    
    return (
        <div className="inference-page">
            <div className={`inference-container-width ${showInformation ? "show-information-half-width" : ""}`}>
                <InferenceContainer />
            </div>
            {(model_information !== null && model_information.display === true) && (
                <>
                    {showInformation && (
                        <div className="show-information-container">
                            <ShowInformation model_information={model_information} />
                        </div>
                    )}
                    <SideArrowContainer showInformation={showInformation} setShowInformation={setShowInformation} />
                </>
            )}
        </div>
    );
}

export default Inference;