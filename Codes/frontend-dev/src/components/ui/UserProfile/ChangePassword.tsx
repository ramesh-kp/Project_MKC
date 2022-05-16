import { Dispatch, FC, SetStateAction, useState } from 'react';
import Image from 'next/image';
import { FieldError, UseFormRegister, UseFormReset } from 'react-hook-form';
import { FormFields } from '@components/pages/Profile';
import { ValidationMessage } from '../CommonPage/ValidationMessage';
import EyeIcon from 'assets/eye-icon.png';
import DisableEyeIcon from 'assets/disable_eye.png';

type fieldType = {
  password?: FieldError;
  confirmPassword?: FieldError;
};
export interface ChangePasswordSectionProps {
  setChangePassword: Dispatch<SetStateAction<boolean>>;
  submitPassword: () => void;
  register: UseFormRegister<FormFields>;
  errors: fieldType;
  reset: UseFormReset<FormFields>;
}

export const ChangePasswordSection: FC<ChangePasswordSectionProps> = ({
  setChangePassword,
  submitPassword,
  register,
  errors,
  reset,
}) => {
  const [passwordVisible, setPasswordVisible] = useState<boolean>(false);
  const visibleIcon = passwordVisible ? DisableEyeIcon : EyeIcon;
  const textVisible = passwordVisible ? 'text' : 'password';
  return (
    <div className="w-full">
      <h2 className="text-2xl font-semibold py-3">Change Password</h2>
      <input
        type="password"
        tabIndex={1}
        maxLength={16}
        className="w-full py-2 mb-4 border-0 border-b-2 focus-visible:outline-0"
        placeholder="New Password"
        {...register('password')}
      />
      <ValidationMessage message={errors.password?.message as string} />
      <input
        className="w-full py-2 mb-4 border-0 border-b-2 focus-visible:outline-0"
        placeholder="Confirm Password"
        maxLength={16}
        tabIndex={2}
        type={textVisible}
        {...register('confirmPassword')}
      />
      <div
        className="eyeIcon_password"
        onClick={() => setPasswordVisible(!passwordVisible)}
      >
        <Image src={visibleIcon} alt="view Password" />
      </div>
      <ValidationMessage message={errors.confirmPassword?.message as string} />
      <div className="flex text-center mt-5">
        <button
          type="button"
          tabIndex={4}
          className="transition-all border-2 w-full block border-sky-600 p-2 rounded-lg text-neutral-600 text-base font-semibold mr-0 lg:my-0 mr-4"
          onClick={() => {
            setChangePassword(false);
            reset({ password: '', confirmPassword: '' });
          }}
        >
          Cancel
        </button>
        <button
          type="button"
          tabIndex={3}
          className="transition-all border-2 w-full block border-sky-600 p-2 rounded-lg text-white text-base font-semibold ml-0 bg-sky-600 lg:my-0  hover:bg-sky-700"
          onClick={() => submitPassword()}
        >
          Submit
        </button>
      </div>
    </div>
  );
};
