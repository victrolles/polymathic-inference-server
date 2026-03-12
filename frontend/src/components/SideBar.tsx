import { Link, useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import type { ResultStatus } from "../types/types";
import { requestAllTasksNameForAModel } from "../requests/fast_api_requests";
import anim_spinner from "../assets/anim_spinner.svg";

function SideBar() {
    const { model_name, task_name } = useParams();
    const [status, setStatus] = useState<ResultStatus>("no");
    const [task_names, setTaskNames] = useState<string[]>([]);

    useEffect(() => {
        if (model_name && task_name) {
            setStatus("loading");
            requestAllTasksNameForAModel(model_name).then((task_names) => {
                setTaskNames(task_names);
            }).catch(() => {
                setStatus("no");
            }).finally(() => {
                setStatus("done");
            });
        }
    }, [model_name, task_name]);
    
    return (
        <>
            {status !== "no" && (
                <div className="side-bar">
                    <h1 className="side-bar-title">{`${model_name}'s tasks`}</h1>
                    <hr />
                    {status === "loading" && <img src={anim_spinner} alt="AI Processing" style={{ width: 32, height: 32 }} />}
                    {status === "done" && task_names.map((task_name) => (
                        <Link key={`${model_name}-${task_name}`} to={`/inference/${model_name}/${task_name}`}>
                            <div className="side-bar-item">{task_name}</div>
                        </Link>
                    ))}
                </div>
            )}
        </>
    );
}

export default SideBar;