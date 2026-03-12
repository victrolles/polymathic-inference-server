import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { requestAllModelsAndTheirFirstTask } from "../requests/fast_api_requests";
import type { ModelTask, ModelTasks } from "../types/types";

function ModelSelector({ model_tasks, loading, setIsModelSelectorOpen }: { model_tasks: ModelTasks; loading: boolean; setIsModelSelectorOpen: (isModelSelectorOpen: boolean) => void }) {
    if (loading) return <select disabled><option>...</option></select>;
    return (
        <div className="model-selector">
          {loading ? <div className="model-selector-item">Loading...</div> : (
            model_tasks.map((model_task: ModelTask) => (
                <Link key={`${model_task.model_name}-${model_task.task_name}`} to={`/inference/${model_task.model_name}/${model_task.task_name}`} className="model-selector-item" onClick={() => setIsModelSelectorOpen(false)}>{model_task.model_name}</Link>
            ))
          )}
        </div>
    );  
}

function NavigationBar() {
    const [isModelSelectorOpen, setIsModelSelectorOpen] = useState(false);
    const [model_tasks, setModelTasks] = useState<ModelTasks>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        requestAllModelsAndTheirFirstTask()
            .then(setModelTasks)
            .finally(() => setLoading(false));
    }, []);

    return (
        <div className="navigation-bar">
            <p  className="navigation-bar-logo">Polymathic</p>
            <ul className="navigation-bar-container">
                <li><Link to="/" className="navigation-bar-item"><span>Home</span></Link></li>
                <li className="navigation-bar-item" >
                  <div className="model-selector-dropdown">
                    <span onClick={() => setIsModelSelectorOpen(!isModelSelectorOpen)}>Models</span>
                    {isModelSelectorOpen && <ModelSelector model_tasks={model_tasks} loading={loading} setIsModelSelectorOpen={setIsModelSelectorOpen} />}
                  </div>
                </li>
            </ul>
        </div>
    );
}

export default NavigationBar;