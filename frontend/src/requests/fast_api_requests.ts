import type { Dict, MediaFiles, ModelSizeTaskId, ModelsSizesTasks } from "../types/types";

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

export async function requestRandomDataSamples(model_size_task_id: ModelSizeTaskId): Promise<MediaFiles> {
    const response = await fetch("http://localhost:8000/api/request_random_data_samples", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ model_size_task_id }),
    });

    if (!response.ok) {
        throw new Error(`HTTP error ${response.status}`);
    }

    const data = await response.json();
    return data.media_files as MediaFiles;
}

export async function requestInference(model_size_task_id: ModelSizeTaskId, media_file_ids: string[]): Promise<MediaFiles> {
    const response = await fetch("http://localhost:8000/api/request_inference_by_media_file_ids", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ model_size_task_id, media_file_ids }),
    });

    if (!response.ok) {
        throw new Error(`HTTP error ${response.status}`);
    }

    const data = await response.json();
    return data as MediaFiles;
}