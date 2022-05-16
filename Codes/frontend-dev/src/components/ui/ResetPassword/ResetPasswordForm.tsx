import { FC, useState } from 'react';
import Image from 'next/image';
import { FieldError, UseFormRegister } from 'react-hook-form';
import { FormInputs } from '@lib/common';
import { ValidationMessage } from '../CommonPage/ValidationMessage';
import EyeIcon from 'assets/eye-icon.png';
import DisableEyeIcon from 'assets/disable_eye.png';

export interface ResetPasswordFormProps {
  register: UseFormRegister<FormInputs>;
  errors: {
    email?: FieldError;
    password?: FieldError;
    name?: FieldError;
    confirmPassword?: FieldError;
  };
  resetPassword: () => void;
}

export const ResetPasswordForm: FC<ResetPasswordFormProps> = ({
  register,
  errors,
  resetPassword,
}) => {
  const [passwordVisible, setPasswordVisible] = useState<boolean>(false);
  const visibleIcon = passwordVisible ? DisableEyeIcon : EyeIcon;
  const textVisible = passwordVisible ? 'text' : 'password';
  return (
    <>
      <input
        type="text"
        className="w-full py-2 mb-4 border-0 border-b-2"
        placeholder="Email"
        disabled
        {...register('email')}
      />
      <ValidationMessage message={errors.email?.message as string} />
      <input
        type="password"
        maxLength={16}
        className="w-full py-2 mb-4 border-0 border-b-2"
        {...register('password')}
        placeholder="Password"
      />
      <ValidationMessage message={errors.password?.message as string} />
      <input
        className="w-full py-2 mb-4 border-0 border-b-2"
        maxLength={16}
        placeholder="Confirm Password"
        type={textVisible}
        {...register('confirmPassword')}
      />
      <ValidationMessage message={errors.confirmPassword?.message as string} />
      <div
        className="eyeIcon_password"
        onClick={() => setPasswordVisible(!passwordVisible)}
      >
        <Image src={visibleIcon} alt="view Password" />
      </div>
      <div className="clear-both" />
      <div className="w-full mt-10 mb-2 lg:flex">
        <button
          type="button"
          className="transition-all border-2 w-full block border-sky-600 p-3 rounded-lg text-white text-base font-semibold ml-0 bg-sky-600 lg:my-0  hover:bg-sky-700"
          onClick={() => resetPassword()}
        >
          Submit
        </button>
      </div>
    </>
  );
};
