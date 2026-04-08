import { useEffect, useState } from "react";
import { requestAllModelsInformation } from "../requests/fast_api_requests";
import type { Dict } from "../types/types";
import Card from "./Card";


function CardContainer() {
    const [models_information, setModelsInformation] = useState<Dict[]>([]);
    useEffect(() => {
        requestAllModelsInformation().then((data: Dict[]) => {
            setModelsInformation(data);
            console.log("models_information", data);
        }).catch((error) => {
            console.error(error);
        });
    }, []);

    return (
        <div className="cards-container">
            {models_information.map((model_information: Dict) => (
                <Card
                    key={model_information.extended_name}
                    model_information={model_information}
                />
            ))}
        </div>
    );
}

export default CardContainer;