import { FC } from 'react';
import { FieldError, UseFormRegister } from 'react-hook-form';
import { ValidationMessage } from '../CommonPage/ValidationMessage';

export interface ForgotPasswordFormProps {
  register: UseFormRegister<{ email: string }>;
  sendEmail: () => void;
  backToLogin: () => void;
  errors: {
    email?: FieldError;
  };
}

export const ForgotPasswordForm: FC<ForgotPasswordFormProps> = ({
  register,
  sendEmail,
  backToLogin,
  errors,
}) => {
  return (
    <>
      <input
        type="text"
        className="w-full py-2 mb-4 border-0 border-b-2"
        placeholder="Email"
        tabIndex={1}
        {...register('email')}
      />
      <ValidationMessage message={errors.email?.message as string} />
      <div className="clear-both" />
      <div className="w-full mt-10 mb-2 lg:flex">
        <button
          tabIndex={3}
          className="transition-all border-2 w-full block border-sky-600 p-3 rounded-lg text-neutral-600 text-base font-semibold mr-0 mb-4 lg:my-0 mr-4"
          onClick={() => backToLogin()}
        >
          Back
        </button>
        <button
          type="button"
          tabIndex={2}
          className="transition-all border-2 w-full block border-sky-600 p-3 rounded-lg text-white text-base font-semibold ml-0 bg-sky-600 lg:my-0  hover:bg-sky-700"
          onClick={() => sendEmail()}
        >
          Send request
        </button>
      </div>
    </>
  );
};
