import { FC, useState } from 'react';
import Image from 'next/image';
import { FieldError, UseFormRegister } from 'react-hook-form';
import { FormInputs, UsersType } from '@lib/common';
import { ValidationMessage } from '@components/ui/CommonPage/ValidationMessage';
import EyeIcon from 'assets/eye-icon.png';
import DisableEyeIcon from 'assets/disable_eye.png';

export interface AddUserProps {
  register: UseFormRegister<FormInputs>;
  errors: {
    fullName?: FieldError;
    email?: FieldError;
    phone?: FieldError;
    password?: FieldError;
    confirmPassword?: FieldError;
  };
  handleClose: () => void;
  addUser: () => void;
  editData: UsersType;
}

export const AddUserForm: FC<AddUserProps> = ({
  handleClose,
  register,
  errors,
  addUser,
  editData,
}) => {
  const [email, setEmail] = useState<string>('');
  const [passwordVisible, setPasswordVisible] = useState<boolean>(false);
  const visibleIcon = passwordVisible ? DisableEyeIcon : EyeIcon;
  const textVisible = passwordVisible ? 'text' : 'password';

  return (
    <>
      <div className="fixed left-0 top-0 z-40 w-full h-full overflow-y-auto overflow-hidden">
        <div
          className="max-w-3xl z-50 my-7 px-5 mx-auto relative flex items-center"
          style={{ minHeight: 'calc(100% - 3.5rem)' }}
        >
          <div className="p-7 bg-white rounded-md h-full w-full">
            <h2 className="inline-block text-2xl mb-4 font-semibold">
              {editData ? 'Edit User' : 'Add User'}
            </h2>
            <input
              type="text"
              tabIndex={1}
              className="w-full py-2 mb-4 border-0 border-b-2 focus-visible:outline-0"
              placeholder="Full Name"
              maxLength={40}
              {...register('fullName')}
            />
            <ValidationMessage message={errors.fullName?.message as string} />
            <div className="sm:block md:flex">
              <div className="md:w-1/2 md:mr-4 sm:mr-0 sm:w-full">
                <input
                  type="text"
                  tabIndex={2}
                  className="w-full py-2 mb-4 border-0 border-b-2 focus-visible:outline-0 h-11"
                  placeholder="Email"
                  {...register('email')}
                  value={email.toLowerCase()}
                  maxLength={40}
                  onChange={e => setEmail(e.target.value)}
                />
                <ValidationMessage message={errors.email?.message as string} />
              </div>
              <div className="md:w-1/2 md:ml-4 sm:ml-0 sm:w-full">
                <input
                  type="text"
                  tabIndex={3}
                  className="w-full py-2 mb-4 border-0 border-b-2 focus-visible:outline-0 h-11"
                  placeholder="Phone"
                  {...register('phone')}
                  minLength={10}
                  maxLength={16}
                />
                <ValidationMessage message={errors.phone?.message as string} />
              </div>
            </div>
            {!editData ? (
              <div className="sm:block md:flex">
                <div className="md:w-1/2 md:mr-4 sm:mr-0 sm:w-full">
                  <input
                    tabIndex={4}
                    type="password"
                    maxLength={16}
                    className="w-full py-2 mb-4 border-0 border-b-2 focus-visible:outline-0 h-11"
                    placeholder="Password"
                    {...register('password')}
                  />
                  <ValidationMessage
                    message={errors.password?.message as string}
                  />
                </div>
                <div className="md:w-1/2 md:ml-4 sm:ml-0 sm:w-full">
                  <input
                    type={textVisible}
                    tabIndex={5}
                    maxLength={16}
                    className="w-full py-2 mb-4 border-0 border-b-2 focus-visible:outline-0 h-11"
                    placeholder="Confirm Password"
                    {...register('confirmPassword')}
                  />
                  <div
                    className="eyeIcon_password"
                    onClick={() => setPasswordVisible(!passwordVisible)}
                  >
                    <Image src={visibleIcon} alt="view Password" />
                  </div>
                  <ValidationMessage
                    message={errors.confirmPassword?.message as string}
                  />
                </div>
              </div>
            ) : (
              ''
            )}

            <div className="clear-both" />

            <div className="w-full mt-10 mb-2 text-right">
              <button
                tabIndex={7}
                className="transition-all border-2 w-auto inline-block border-sky-600 px-8 py-2 rounded-lg text-neutral-600 text-base font-semibold mr-0 mb-4 lg:my-0 mr-4 text-center"
                onClick={() => handleClose()}
              >
                Cancel
              </button>
              <button
                tabIndex={6}
                className="transition-all border-2 w-auto inline-block border-sky-600 px-8 py-2 rounded-lg text-white text-base font-semibold ml-0 bg-sky-600 lg:my-0  text-center hover:bg-sky-700"
                onClick={() => addUser()}
              >
                Submit
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="fixed bg-current left-0 top-0 opacity-40 z-30 w-full h-full" />
    </>
  );
};
