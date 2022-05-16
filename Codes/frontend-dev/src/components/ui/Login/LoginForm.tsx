import { FC, useState } from 'react';
import Image from 'next/image';
import { UseFormRegister } from 'react-hook-form';
import { LoginFormInputs } from '@lib/common';
import EyeIcon from 'assets/eye-icon.png';
import DisableEyeIcon from 'assets/disable_eye.png';

export interface LoginFormprops {
  register: UseFormRegister<LoginFormInputs>;
  handleLogin: () => void;
  forgotPassword: () => void;
  rememberMe: boolean;
  setRememberMe: (value: boolean) => void;
  passwordVisible: boolean;
  setPasswordVisible: (value: boolean) => void;
}

export const LoginForm: FC<LoginFormprops> = ({
  register,
  handleLogin,
  forgotPassword,
  rememberMe,
  setRememberMe,
}) => {
  const [passwordVisible, setPasswordVisible] = useState<boolean>(false);
  const visibleIcon = passwordVisible ? DisableEyeIcon : EyeIcon;
  const textVisible = passwordVisible ? 'text' : 'password';
  return (
    <>
      <input
        type="text"
        className="w-full py-2 mb-4 border-0 border-b-2 focus-visible:outline-0"
        placeholder="Username"
        tabIndex={1}
        {...register('username')}
      />
      <input
        className="w-full py-2 mb-4 border-0 border-b-2"
        placeholder="Password"
        type={textVisible}
        tabIndex={2}
        {...register('password')}
      />
      <div
        className="eyeIcon_password"
        onClick={() => setPasswordVisible(!passwordVisible)}
      >
        <Image src={visibleIcon} alt="view Password" />
      </div>
      <div className="clear-both" />
      <div className="float-left">
        <label className="text-slate-500">
          <input
            type="checkbox"
            className="default:ring-2 mr-2 "
            checked={rememberMe}
            tabIndex={3}
            onChange={() => setRememberMe(!rememberMe)}
          />{' '}
          Remember me
        </label>
      </div>
      <label
        className="lg:float-right md:float-right float-left width mt-2 text-slate-500 hover:text-indigo-800 float-sm-left cursor-pointer"
        onClick={() => forgotPassword()}
      >
        Forgot Password
      </label>
      <div className="clear-both" />
      <div className="w-full mt-10 mb-2 lg:flex">
        <button
          type="button"
          tabIndex={4}
          className="transition-all border-2 w-full block border-sky-600 p-3 rounded-lg text-white text-base font-semibold ml-0 bg-sky-600 lg:my-0  hover:bg-sky-700"
          onClick={() => handleLogin()}
        >
          Login
        </button>
      </div>
    </>
  );
};
