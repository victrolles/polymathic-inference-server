import type { CardProps } from "../types/interfaces";
import { formatDate } from "../functions/functions";
import { Link } from "react-router-dom";

function Card({ model_information }: CardProps) {
    return (
        <div className="card">
            <div className="card-image">
                <img src={model_information.cover_image_path} alt={model_information.extended_name} />
            </div>
            <p className="card-title">{model_information.extended_name}</p>
            <p className="card-date">{formatDate(model_information.date)}</p>
            <p className="card-short-description">{model_information.short_description}</p>
            <Link to={`/inference/${model_information.model_id}/${model_information.size_id}/${model_information.task_id}`} className="card-link">
                <button className="card-button">Test model</button>
            </Link>
        </div>
    );
}

export default Card;