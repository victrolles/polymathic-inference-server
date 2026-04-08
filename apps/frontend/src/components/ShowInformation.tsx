import type { Dict } from "../types/types";
import type { ShowInformationProps } from "../types/interfaces";
import { formatDate } from "../functions/functions";

function Link({ link }: { link: Dict }) {
    return (
        <li className="show-information-link">
            <span className="show-information-link-label">{link.name} :</span>
            <a href={link.url} target="_blank" rel="noopener noreferrer">{link.alt}</a>
        </li>
    );
}

function ShowInformation({ model_information }: ShowInformationProps) {
    if (model_information === null) {
        return null;
    }
    return (
        <div className="show-information">
            <p className="show-information-title">{model_information.extended_name}</p>
            <p className="show-information-date">{formatDate(model_information.date)}</p>
            <div className="show-information-image">
                <img src={model_information.cover_image_path} alt={model_information.extended_name} />
            </div>
            <p className="show-information-description">{model_information.description}</p>
            {model_information.links.length > 0 && (
                <div className="show-information-links">
                    <p>Links :</p>
                    <ul className="show-information-link-list">
                        {model_information.links.map((link: Dict) => (
                            <Link key={link.name} link={link} />
                        ))}
                    </ul>
                </div>
            )}
            {model_information.authors !== "" && (
                <div className="show-information-authors">
                    <p>Authors :</p>
                    <span>{model_information.authors}</span>
                </div>
            )}
        </div>
    );
}

export default ShowInformation;