import { useState, useEffect } from "react";
import type { ConfigDict, MediaFiles, MediaType, ModelSizeTaskId, ResultStatus } from "../types/types";
// import type { MediaFiles, ResultStatus, Task } from "../types/types";
// import { requestRandomImages, requestInference, requestConfigDictForATask } from "../requests/fast_api_requests";
import ImageSelector from "../components/ImageSelector";
// import SubmitButton from "../components/SubmitButton";
import anim_spinner from "../assets/anim_spinner.svg";
// // import { getSelectedMediaFileNames } from "../functions/functions";
// import type { InferenceProps } from "../types/interfaces";
import ResultsContainer from "../components/ResultsContainer";
import { useParams } from "react-router-dom";
import { requestAModelConfigDict, requestInference, requestRandomDataSamples } from "../requests/fast_api_requests";
// import { getSelectedMediaFileNames } from "../functions/functions";


function Inference() {
    const { model_id, size_id, task_id } = useParams();
    const [config_dict, setConfigDict] = useState<ConfigDict | null>(null);
    const [data_samples, setDataSamples] = useState<MediaFiles>([]);
    const [data_results, setDataResults] = useState<MediaFiles>([]);
    const [status, setStatus] = useState<ResultStatus>("no");

    useEffect(() => {
        if (model_id && size_id && task_id) {

            //reset variables
            setDataSamples([]);
            setDataResults([]);
            setStatus("no");
            setConfigDict(null);

            // Get new config dictionary
            requestAModelConfigDict(model_id)
            .then((data: ConfigDict) => {
                setConfigDict(data);
            }).catch((error) => {
                console.error(error);
            });
        
            // // Get new random data samples
            // requestRandomDataSamples({ model_id, size_id, task_id })
            // .then((data: MediaFiles) => {
            //     setDataSamples(data);
            //     console.log("data_samples", data);
            // }).catch((error) => {
            //     console.error(error);
            // });
        }
    }, [model_id, size_id, task_id]);

    // const submitInferenceRequest = () => {
    //     if (!model_id || !size_id || !task_id) {
    //         setStatus("no");
    //         return;
    //     }
    //     setStatus("loading");
    //     requestInference({ model_id, size_id, task_id }, getSelectedMediaFileIds(data_samples))
    //     .then((data: MediaFiles) => {
    //         setDataResults(data);
    //         setStatus("done");
    //         console.log("data_results", data);
    //     }).catch((error) => {
    //         console.error(error);
    //         setStatus("no");
    //     });
    // };

    if (!config_dict) {
        return null;
    }

    return (
        <div className="inference">
            {/* <p className="slogan">{config_dict['ui']['text-top-screen']}</p>
            <ImageSelector mediaFiles={data_samples} setMediaFiles={setDataSamples} displayName={config_dict['ui']['data-inputs']['display-name']} displaySelectedImage={config_dict['ui']['data-inputs']['display-selected-data']} imageSize={{ width: config_dict['ui']['data-inputs']['data-size']['width'], height: config_dict['ui']['data-inputs']['data-size']['height'] }} selectedImageSize={{ width: config_dict['ui']['data-inputs']['selected-data-size']['width'], height: config_dict['ui']['data-inputs']['selected-data-size']['height'] }} multipleSelection={config_dict['ui']['data-inputs']['multiple-data']} mediaType={config_dict['ui']['data-inputs']['type'] as MediaType}/>
            <hr />
            {status === 'loading' && <img src={anim_spinner} alt="AI Processing" style={{ width: 45, height: 45 }} /> }
            {status === 'done' && 
                <ResultsContainer mediaFiles={data_results} multipleResults={config_dict['ui']['data-outputs']['multiple-data']} dataHeight={config_dict['ui']['data-inputs']['data-size']['height']} selectedDataHeight={config_dict['ui']['data-inputs']['selected-data-size']['height']} displaySelectedData={config_dict['ui']['data-inputs']['display-selected-data']} displayName={config_dict['ui']['data-outputs']['display-name']} mediaType={config_dict['ui']['data-outputs']['type'] as MediaType} />
            }
            <SubmitButton submitAction={submitInferenceRequest} submitText={config_dict['ui']['submit-button']['text']} /> */}
        </div>
    );
}

export default Inference;