import { Link, useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import type { IdName, ModelsSizesTasks, Status } from "../types/types";
import { requestAllModelsSizesTasks } from "../requests/fast_api_requests";
import anim_spinner from "../assets/anim_spinner.svg";

function SideBar() {
    const { model_id, size_id } = useParams();
    const [status, setStatus] = useState<Status>("no");
    const [models_sizes_tasks, setModelsSizesTasks] = useState<ModelsSizesTasks>([]);
    const [tasks, setTasks] = useState<IdName[]>([]);
    const [size, setSize] = useState<IdName | null>(null);

    useEffect(() => {
        requestAllModelsSizesTasks().then((data) => {
            setModelsSizesTasks(data);
        });
    }, []);

    useEffect(() => {
        if (model_id && size_id && models_sizes_tasks.length > 0) {
            setStatus("loading");
            const match = models_sizes_tasks.find(
                (m) =>
                    m.model.id === model_id &&
                    m.sizes.some((s) => s.id === size_id)
            );
            setTasks(match ? match.tasks : []);
            setSize(match ? match.sizes.find((s) => s.id === size_id) as IdName : null);
            setStatus("done");
        } else {
            setStatus("no");
            setTasks([]);
            setSize(null);
        }
    }, [model_id, size_id, models_sizes_tasks]);
    
    return (
        <>
            {status !== "no" && (
                <div className="side-bar">
                    <h1 className="side-bar-title">{`${size?.name}'s tasks`}</h1>
                    <hr />
                    {status === "loading" && <img src={anim_spinner} alt="AI Processing" style={{ width: 32, height: 32 }} />}
                    {status === "done" && tasks.map((task) => (
                        <Link key={task.id} to={`/inference/${model_id}/${size_id}/${task.id}`}>
                            <div className="side-bar-item">{task.name}</div>
                        </Link>
                    ))}
                </div>
            )}
        </>
    );
}

export default SideBar;