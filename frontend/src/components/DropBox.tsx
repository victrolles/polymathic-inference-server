import DropList from "./DropList";
import type { DropBoxProps } from "../types/interfaces";
import { useEffect, useRef, useState } from "react";
import chevron_icon from "../assets/chevron.png";
function DropBox({ switchable_modalities, setCurrentModality }: DropBoxProps) {
    const [is_open, setIsOpen] = useState(false);
    const rootRef = useRef<HTMLDivElement | null>(null);

    useEffect(() => {
        if (!is_open) return;

        const onDocumentMouseDown = (e: MouseEvent) => {
            const root = rootRef.current;
            if (!root) return;
            if (!root.contains(e.target as Node)) setIsOpen(false);
        };

        document.addEventListener("mousedown", onDocumentMouseDown);
        return () => document.removeEventListener("mousedown", onDocumentMouseDown);
    }, [is_open]);

    return (
        <div
            ref={rootRef}
            className="drop-box"
            onMouseLeave={() => setIsOpen(false)}
        >
            <div className="drop-box-header" onClick={() => setIsOpen(!is_open)}>
                <img src={chevron_icon} alt="arrow-down" />
            </div>
            {is_open && <DropList switchable_modalities={switchable_modalities} setCurrentModality={setCurrentModality} />}
        </div>
    );
}

export default DropBox;