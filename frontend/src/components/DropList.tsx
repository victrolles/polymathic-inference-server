import type { DropListProps } from "../types/interfaces";

function DropList({ switchable_modalities, setCurrentModality }: DropListProps) {
    if (!switchable_modalities) return null;
    return (
        <div className="drop-list">
            {switchable_modalities.map((modality) => (
                <div
                className="drop-list-item"
                onClick={() => setCurrentModality(modality)}
                key={modality.id}>{modality.name}</div>
            ))}
        </div>
    );
}

export default DropList;