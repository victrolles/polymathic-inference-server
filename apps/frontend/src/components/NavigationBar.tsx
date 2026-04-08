import { useState, useEffect } from "react";
import { Link, useLocation } from "react-router-dom";
import { requestAllModelsSizesTasks } from "../requests/fast_api_requests";
import type { IdName, ModelSizesTasks, ModelsSizesTasks } from "../types/types";
import type { ModelSelectorProps, SizeSelectorProps } from "../types/interfaces";
import logo from "../assets/logo_dark_mode.png";

function SizeSelector({model, sizes, task, setIsModelSelectorOpen}: SizeSelectorProps) {
    return (
        <div className="size-selector">
            {sizes.map((size: IdName) => (
                <Link
                    key={size.id}
                    to={`/inference/${model.id}/${size.id}/${task.id}`}
                    onClick={() => {
                        setIsModelSelectorOpen(false);
                    }}
                    className="size-selector-item"
                >
                    {size.name}
                </Link>
            ))}
        </div>
    );
}

function ModelSelector({models_sizes_tasks, setIsModelSelectorOpen} : ModelSelectorProps) {
    const [isSizeSelectorOpen, setIsSizeSelectorOpen] = useState(false);
    const [selectedModel, setSelectedModel] = useState<IdName | null>(null);
    return (
        <div className="model-selector">
            {models_sizes_tasks.map((model_sizes_tasks: ModelSizesTasks) => (
                <div key={model_sizes_tasks.model.id} onClick={() => setSelectedModel(model_sizes_tasks.model)}>
                    <div
                        className="model-selector-item"
                        onClick={() => setIsSizeSelectorOpen(!isSizeSelectorOpen)}
                    >
                        {model_sizes_tasks.model.name}
                    </div>
                    {selectedModel && selectedModel.id === model_sizes_tasks.model.id && (
                        <SizeSelector
                            model={model_sizes_tasks.model}
                            sizes={model_sizes_tasks.sizes}
                            task={model_sizes_tasks.tasks[0]}
                            setIsModelSelectorOpen={setIsModelSelectorOpen}
                        />
                    )}
                </div>
            ))}
        </div>
    );
}

function NavigationBar() {
    const [isModelSelectorOpen, setIsModelSelectorOpen] = useState(false);
    const [models_sizes_tasks, setModelsSizesTasks] = useState<ModelsSizesTasks>([]);
    const location = useLocation();
    const isHome = location.pathname === "/";
    const isInference = location.pathname.startsWith("/inference");

    useEffect(() => {
        requestAllModelsSizesTasks()
            .then(setModelsSizesTasks)
    }, []);

    return (
        <div className="navigation-bar">
            <img src={logo} alt="SciMLDemo Logo" className="navigation-bar-logo" />
            <ul className="navigation-bar-container">
                <li><Link to="/" className={`navigation-bar-item${isHome ? "-selected" : ""}`}><span>Home</span></Link></li>
                <li className={`navigation-bar-item${isInference ? "-selected" : ""}`} >
                  <div className="model-selector-dropdown">
                    <span onClick={() => setIsModelSelectorOpen(!isModelSelectorOpen)}>Models</span>
                    {isModelSelectorOpen && <ModelSelector models_sizes_tasks={models_sizes_tasks} setIsModelSelectorOpen={setIsModelSelectorOpen} />}
                  </div>
                </li>
            </ul>
        </div>
    );
}

export default NavigationBar;