import { useState, useEffect } from "react";
import type { ConfigTasks, DatasetLocations, Dict, ModelSizeTaskId, Packet, Packets, SelectablePackets, Status } from "../types/types";
import ImageSelector from "../components/MediaSelector";
import { useParams } from "react-router-dom";
import { requestAModelConfigTask, requestRandomDataSamples, requestInference } from "../requests/fast_api_requests";
import { getSelectedPackets, getSelectedDatasetLocations } from "../functions/functions";
import type { InferenceRequestProps } from "../types/interfaces";
import PacketsContainer from "../components/PacketsContainer";
import SubmitButton from "../components/SubmitButton";

function Inference() {
    const { model_id, size_id, task_id } = useParams();
    const [config_task, setConfigTask] = useState<Dict | null>(null);
    const [selectable_packets, setSelectablePackets] = useState<SelectablePackets>([]);
    const [inference_packets, setInferencePackets] = useState<Packets>([]);
    const [samples_status, setSamplesStatus] = useState<Status>("no");
    const [inference_status, setInferenceStatus] = useState<Status>("no");

    useEffect(() => {
        if (model_id && size_id && task_id) {

            //reset variables
            setConfigTask(null);
            setSelectablePackets([]);
            setInferencePackets([]);
            setSamplesStatus("loading");
            setInferenceStatus("no");

            // Get new config dictionary
            requestAModelConfigTask({ model_id, size_id, task_id })
            .then((data: Dict) => {
                setConfigTask(data);
                console.log("config_dict", data);
            }).catch((error) => {
                console.error(error);
                setSamplesStatus("error");
            });
        
            // Get new random data samples
            requestRandomDataSamples({ model_id, size_id, task_id })
            .then((packets: Packets) => {
                setSelectablePackets(packets.map((packet: Packet) => ({ packet, is_selected: false })) as SelectablePackets);
                setSamplesStatus("done");
            }).catch((error) => {
                console.error(error);
                setSamplesStatus("error");
            });
        }
    }, [model_id, size_id, task_id]);

    const submitInferenceRequest = () => {
        if (!model_id || !size_id || !task_id) {
            setInferenceStatus("no");
            return;
        }
        setInferenceStatus("loading");
        const inference_request: InferenceRequestProps = {
            model_size_task_id: { model_id, size_id, task_id } as ModelSizeTaskId,
            dataset_locations: getSelectedDatasetLocations(selectable_packets) as DatasetLocations
        }

        requestInference(inference_request)
        .then((packets: Packets) => {
            setInferencePackets(packets);
            setInferenceStatus("done");
            console.log("inference_packets", packets);
        }).catch((error) => {
            console.error(error);
            setInferenceStatus("error");
        });
    };

    if (!config_task) {
        return null;
    }

    return (
        <div className="inference">
            <p className="slogan">{config_task.ui.text_top_screen}</p>
            <ImageSelector
                selectable_packets={selectable_packets}
                setSelectablePackets={setSelectablePackets}
                data_samples={config_task.data_samples}
                media_size={config_task.ui.data_size}
            />
            {config_task.selected_data_samples.display && <PacketsContainer
                packets={getSelectedPackets(selectable_packets)}
                configDict={config_task.selected_data_samples as Dict}
                status={"no"}
                media_size={config_task.ui.selected_data_size}
            />
            }
            <hr />
            {inference_status !== "no" && <PacketsContainer
                packets={inference_packets}
                configDict={config_task.data_outputs as Dict}
                media_size={config_task.ui.output_data_size}
                status={inference_status}
            />}
            <SubmitButton
                submitAction={submitInferenceRequest}
                submit_text={config_task.ui.submit_button_text}
            />
        </div>
    );
}

export default Inference;