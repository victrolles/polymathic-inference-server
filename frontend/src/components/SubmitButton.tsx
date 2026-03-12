import type { SubmitButtonProps } from "../types/interfaces";

function SubmitButton({ submitAction, submitText }: SubmitButtonProps) {
    return (
        <div className="submit-button">
            <button className="submit-button-text" onClick={submitAction}>{submitText}</button>
        </div>
    );
}

export default SubmitButton;