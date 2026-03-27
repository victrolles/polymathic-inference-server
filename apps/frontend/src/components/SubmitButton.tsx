import type { SubmitButtonProps } from "../types/interfaces";

function SubmitButton({ submitAction, submit_text }: SubmitButtonProps) {
    return (
        <div className="submit-button">
            <button className="submit-button-text" onClick={submitAction}>{submit_text}</button>
        </div>
    );
}

export default SubmitButton;