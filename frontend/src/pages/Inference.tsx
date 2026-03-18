import { useState, useEffect } from "react";
import type { ConfigTasks, Dict, MediaFile, MediaFiles, ModelSizeTaskId, ResultStatus, selectableMediaFile } from "../types/types";
// import type { MediaFiles, ResultStatus, Task } from "../types/types";
// import { requestRandomImages, requestInference, requestConfigDictForATask } from "../requests/fast_api_requests";
import ImageSelector from "../components/MediaSelector";
// import SubmitButton from "../components/SubmitButton";
import anim_spinner from "../assets/anim_spinner.svg";
// // import { getSelectedMediaFileNames } from "../functions/functions";
// import type { InferenceProps } from "../types/interfaces";
import ResultsContainer from "../components/ResultsContainer";
import { useParams } from "react-router-dom";
import { requestAModelConfigTask, requestInference, requestRandomDataSamples } from "../requests/fast_api_requests";
import SelectedMediasDisplay from "../components/SelectedMediasDisplay";
// import { getSelectedMediaFileNames } from "../functions/functions";


function Inference() {
    const { model_id, size_id, task_id } = useParams();
    const [configTask, setConfigTask] = useState<Dict | null>(null);
    const [selectableMediaFiles, setSelectableMediaFiles] = useState<selectableMediaFile[]>([]);
    const [data_results, setDataResults] = useState<MediaFiles>([]);
    const [status, setStatus] = useState<ResultStatus>("no");

    useEffect(() => {
        if (model_id && size_id && task_id) {

            //reset variables
            setSelectableMediaFiles([]);
            setStatus("no");

            // Get new config dictionary
            requestAModelConfigTask({ model_id, size_id, task_id })
            .then((data: Dict) => {
                setConfigTask(data);
                console.log("config_dict", data);
            }).catch((error) => {
                console.error(error);
            });
        
            // Get new random data samples
            requestRandomDataSamples({ model_id, size_id, task_id })
            .then((data: MediaFiles) => {
                console.log("data_samples", data);
                setSelectableMediaFiles(data.map((mediaFile: MediaFile) => ({ mediaFile, isSelected: false })));
            }).catch((error) => {
                console.error(error);
            });
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

    if (!configTask) {
        return null;
    }

    return (
        <div className="inference">
            <p className="slogan">{configTask.ui.text_top_screen}</p>
            <ImageSelector
                selectableMediaFiles={selectableMediaFiles}
                setSelectableMediaFiles={setSelectableMediaFiles}
                dataSamples={configTask.data_samples}
                dataSize={configTask.ui.data_size}
            />
            <SelectedMediasDisplay
                selectableMediaFiles={selectableMediaFiles}
                selectedDataSamples={configTask.selected_data_samples}
                mediaSize={configTask.ui.data_size}
            />
            <hr />
            {/* {status === 'loading' && <img src={anim_spinner} alt="AI Processing" style={{ width: 45, height: 45 }} /> }
            {status === 'done' && 
                <ResultsContainer mediaFiles={data_results} multipleResults={config_dict['ui']['data-outputs']['multiple-data']} dataHeight={config_dict['ui']['data-inputs']['data-size']['height']} selectedDataHeight={config_dict['ui']['data-inputs']['selected-data-size']['height']} displaySelectedData={config_dict['ui']['data-inputs']['display-selected-data']} displayName={config_dict['ui']['data-outputs']['display-name']} mediaType={config_dict['ui']['data-outputs']['type'] as MediaType} />
            }
            <SubmitButton submitAction={submitInferenceRequest} submitText={config_dict['ui']['submit-button']['text']} /> */}
        </div>
    );
}

export default Inference;