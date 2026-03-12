import type { ConfigDict, MediaFiles, MediaType, ModelTask, ModelTasks } from "../types/types";

export async function requestAllModelsAndTheirFirstTask(): Promise<ModelTasks> {
    const response = await fetch("http://localhost:8000/api/request_all_models_and_their_first_task", {
        method: "GET",
    });

    if (!response.ok) {
        throw new Error(`HTTP error ${response.status}`);
    }

    const data = await response.json();
    const model_tasks: ModelTasks = data.model_tasks.map((model_task: ModelTask) => ({ model_name: model_task.model_name, task_name: model_task.task_name }));
    return model_tasks;
}

export async function requestAllTasksNameForAModel(model_name: string): Promise<string[]> {
    const response = await fetch("http://localhost:8000/api/request_all_tasks_name_for_a_model", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ model_name }),
    });
    
    if (!response.ok) {
        throw new Error(`HTTP error ${response.status}`);
    }

    const data = await response.json();
    const task_names: string[] = data.task_names.map((task_name: string) => task_name);
    return task_names;
}

export async function requestConfigDictForATask(model_task: ModelTask): Promise<ConfigDict> {
    const response = await fetch("http://localhost:8000/api/request_config_dict_for_a_task", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ model_task }),
    });
    
    if (!response.ok) {
        throw new Error(`HTTP error ${response.status}`);
    }
    
    const data = await response.json();
    const config_dict: ConfigDict = data.config_dict;
    return config_dict;
}

export async function requestRandomDataSamples(model_task: ModelTask): Promise<MediaFiles> {
    const response = await fetch("http://localhost:8000/api/request_random_data_samples", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ model_task }),
    });

    if (!response.ok) {
        throw new Error(`HTTP error ${response.status}`);
    }

    const data = await response.json();
    const mediaFiles: MediaFiles = data.media_files.map((media_file: any) => ({ name: media_file.name, path: media_file.path, type: media_file.type as MediaType, isSelected: false }));
    return mediaFiles;
}

export async function requestInference(model_task: ModelTask, names: string[]): Promise<MediaFiles> {
    const response = await fetch("http://localhost:8000/api/request_inference", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ model_task, names }),
    });

    if (!response.ok) {
        throw new Error(`HTTP error ${response.status}`);
    }

    const data = await response.json();
    const mediaFiles: MediaFiles = data.media_files.map((media_file: any) => ({ name: media_file.name, path: media_file.path, type: media_file.type as MediaType, isSelected: false }));
    return mediaFiles;
}