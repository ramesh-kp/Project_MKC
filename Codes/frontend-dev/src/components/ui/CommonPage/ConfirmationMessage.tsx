import { FC } from 'react';

interface ConfirmationMessageProps {
  closeConfirmation: () => void;
  confirmedAction: () => void;
  confirmationText: string;
}
export const ConfirmationMessage: FC<ConfirmationMessageProps> = ({
  closeConfirmation,
  confirmedAction,
  confirmationText,
}) => {
  return (
    <>
      <input type="checkbox" id="my-modal" className="modal-toggle" />
      <div className="modal">
        <div className="modal-box">
          <p className="py-4">{confirmationText}</p>
          <div className="modal-action">
            <label
              htmlFor="my-modal"
              className="btn bg-sky-600 hover:bg-sky-700"
              onClick={() => closeConfirmation()}
            >
              No
            </label>
            <label
              className="btn bg-sky-600 hover:bg-sky-700"
              onClick={() => confirmedAction()}
            >
              Yes
            </label>
          </div>
        </div>
      </div>
    </>
  );
};
