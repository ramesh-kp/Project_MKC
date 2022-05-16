import { Dispatch, FC, SetStateAction, useState } from 'react';
import Image from 'next/image';
import { useRouter } from 'next/router';
import { useForm } from 'react-hook-form';
import { useQueryClient } from 'react-query';
import * as Yup from 'yup';
import { yupResolver } from '@hookform/resolvers/yup';
import { useSession } from '@lib/useSession';
import graphQLClient from '@lib/useGQLQuery';
import Logout from 'assets/logout-icon.png';
import { globalVariables, messages, status } from '@lib/common';
import { UpdateUserMutation, useUpdateUserMutation } from '@api/graphql';
import { ChangePasswordSection } from '@components/ui/UserProfile/ChangePassword';
import { ProfileSection } from '@components/ui/UserProfile/UserProfile';
import CustomizedSnackbars from 'ui/CommonPage/SnackBar/Snackbar';
import { ApiLoader } from '@components/ui/CommonPage/ApiLoader';

export type FormFields = {
  password: string;
  confirmPassword: string;
};

const validationSchema = Yup.object().shape({
  password: Yup.string()
    .required(globalVariables.passwordRequired)
    .matches(
      // eslint-disable-next-line no-useless-escape
      /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})/,
      globalVariables.passwordValidation,
    ),
  confirmPassword: Yup.string()
    .required(globalVariables.confirmPasswordRequired)
    .oneOf([Yup.ref('password')], globalVariables.confirmPasswordValidation),
});

export interface ProfilePageProps {
  setProfileFlag: Dispatch<SetStateAction<boolean>>;
}
export const ProfilePage: FC<ProfilePageProps> = ({ setProfileFlag }) => {
  const router = useRouter();
  const { state, dispatch } = useSession();
  const [changePassword, setChangePassword] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string>('');
  const [messageType, setMessageType] = useState<string>('');
  const [open, setOpen] = useState<boolean>(false);
  const [loader, setLoader] = useState<boolean>(false);
  const { currentUser } = state;

  const formOptions = {
    defaultValues: { password: '', confirmPassword: '' },
    resolver: yupResolver(validationSchema),
  };

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<FormFields>(formOptions);

  const logout = () => {
    dispatch({ type: 'logout' });
    router.push('/login');
  };

  const updateMutation = useUpdateUserMutation<UpdateUserMutation>(
    graphQLClient(),
  );
  const queryClient = useQueryClient();

  const submitPassword = handleSubmit(async formValues => {
    try {
      setLoader(true);
      const variable = {
        where: {
          id: currentUser.id,
        },
        data: {
          password: formValues.password,
        },
      };
      await updateMutation.mutateAsync(variable);
      queryClient.invalidateQueries();
      setErrorMessage('Password changed successfully');
      setMessageType(status.success);
    } catch (e) {
      // eslint-disable-next-line no-console
      console.error(e);
      setErrorMessage(messages.commonError);
      setMessageType(status.error);
    } finally {
      setChangePassword(false);
      setOpen(true);
      reset();
      setLoader(false);
    }
  });

  if (loader) return <ApiLoader />;

  return (
    <>
      <CustomizedSnackbars
        open={open}
        setOpen={setOpen}
        message={errorMessage}
        type={messageType}
      />
      <div className="w-1/4 h-full fixed right-0 top-0 bg-white z-50">
        <div className="w-full mt-20 p-8">
          <div className="rounded-full bg-green-200 w-20 h-20 text-center text-white uppercase text-4xl font-semibold leading-relaxed pt-2">
            {currentUser.name?.charAt(0)}
          </div>
          {changePassword ? (
            <ChangePasswordSection
              {...{
                setChangePassword,
                submitPassword,
                register,
                errors,
                reset,
              }}
            />
          ) : (
            <ProfileSection {...{ setChangePassword }} />
          )}
        </div>

        <label
          onClick={() => logout()}
          className="absolute pr-8 right-0 bottom-5 text-sky-600 font-semibold uppercase text-sm hover:text-black cursor-pointer"
        >
          Log Out{' '}
          <Image src={Logout} className="float-right ml-2" alt="logout" />
        </label>
      </div>
      <div
        className="fixed bg-current left-0 top-0 opacity-40 z-40 w-full h-full"
        onClick={() => setProfileFlag(false)}
      />
    </>
  );
};
