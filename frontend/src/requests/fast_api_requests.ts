import type { InferenceRequestProps } from "../types/interfaces";
import type { Dict, Packets, ModelSizeTaskId, ModelsSizesTasks } from "../types/types";

export async function requestAllModelsSizesTasks(): Promise<ModelsSizesTasks> {
    const response = await fetch("http://localhost:8000/api/request_all_models_sizes_tasks", {
        method: "GET",
    });

    if (!response.ok) {
        throw new Error(`HTTP error ${response.status}`);
    }

    const data = await response.json();
    return data.models_sizes_tasks as ModelsSizesTasks;
}

export async function requestAModelConfigTask(model_size_task_id: ModelSizeTaskId): Promise<Dict> {
    const response = await fetch("http://localhost:8000/api/request_a_model_config_task", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ model_size_task_id }),
    });
    
    if (!response.ok) {
        throw new Error(`HTTP error ${response.status}`);
    }
    const data = await response.json();
    return data.config_task as Dict;
}

export async function requestModelInformation(model_id: string): Promise<Dict> {
    const response = await fetch("http://localhost:8000/api/request_model_information", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ model_id }),
    });
    
    if (!response.ok) {
        throw new Error(`HTTP error ${response.status}`);
    }

    const data = await response.json();
    return data as Dict;
}

export async function requestRandomDataSamples(model_size_task_id: ModelSizeTaskId): Promise<Packets> {
    const response = await fetch("http://localhost:8000/api/request_random_data_samples", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ model_size_task_id }),
    });

    if (!response.ok) {
        throw new Error(`HTTP error ${response.status}`);
    }

    const data = await response.json();
    return data.packets as Packets;
}

export async function requestInference(inference_requests: InferenceRequestProps): Promise<Packets> {
    const response = await fetch("http://localhost:8000/api/request_inference", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(inference_requests),
    });

    if (!response.ok) {
        throw new Error(`HTTP error ${response.status}`);
    }

    const data = await response.json();
    return data.packets as Packets;
}