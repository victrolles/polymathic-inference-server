import type { ConfigDict, MediaFiles, MediaType, ModelSizeTaskId, ModelsSizesTasks } from "../types/types";

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

export async function requestAModelConfigDict(model_id: string): Promise<ConfigDict> {
    const response = await fetch("http://localhost:8000/api/request_a_model_config_dict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ model_id }),
    });
    
    if (!response.ok) {
        throw new Error(`HTTP error ${response.status}`);
    }
    
    const data = await response.json();
    const config_dict: ConfigDict = data.config_dict as ConfigDict;
    return config_dict;
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
    const mediaFiles: MediaFiles = data.media_files.map((media_file: any) => ({ name: media_file.name, path: media_file.path, type: media_file.type as MediaType, isSelected: false }));
    return mediaFiles;
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
    const mediaFiles: MediaFiles = data.media_files.map((media_file: any) => ({ name: media_file.name, path: media_file.path, type: media_file.type as MediaType, isSelected: false }));
    return mediaFiles;
}