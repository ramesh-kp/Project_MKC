import { FC, useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import Image from 'next/image';
import { useForm } from 'react-hook-form';
import { CurrentUser, useSession } from '@lib/useSession';
import { LoginFormInputs, messages } from '@lib/common';
import Logo from 'assets/logo.svg';
import Login from 'assets/login-img.jpg';
import { LoginForm } from 'ui/Login/LoginForm';
import {
  AuthenticateUserWithPasswordMutation,
  useAuthenticateUserWithPasswordMutation,
} from '../../../domain/api/graphql';
import graphQLClient from '@lib/useGQLQuery';
import CustomizedSnackbars from 'ui/CommonPage/SnackBar/Snackbar';
import { ApiLoader } from '@components/ui/CommonPage/ApiLoader';

export const LoginPage: FC = () => {
  const router = useRouter();
  const { state, dispatch } = useSession(true);
  const { currentUser } = state;
  const [errorMessage, setErrorMessage] = useState<string>('');
  const [messageType, setMessageType] = useState<string>('');
  const [open, setOpen] = useState<boolean>(false);
  const [passwordVisible, setPasswordVisible] = useState<boolean>(false);
  const [rememberMe, setRememberMe] = useState<boolean>(false);
  const [loader, setLoader] = useState<boolean>(false);

  const formOptions = {
    defaultValues: {
      username: '',
      password: '',
    },
  };
  const { register, handleSubmit, setValue } =
    useForm<LoginFormInputs>(formOptions);

  const mutation =
    useAuthenticateUserWithPasswordMutation<AuthenticateUserWithPasswordMutation>(
      graphQLClient(),
    );
  const userDetails = 'userdetails';

  useEffect(() => {
    const savedCredentials: string | null = localStorage.getItem(userDetails);
    if (savedCredentials) {
      const userData = JSON.parse(savedCredentials?.toString());
      if (userData) {
        setValue('username', userData.username);
        setValue('password', userData.password);
      }
    }
  });

  const handleLogin = handleSubmit(async formValues => {
    try {
      setLoader(true);
      if (rememberMe)
        localStorage.setItem(userDetails, JSON.stringify(formValues));
      const variable = {
        email: formValues.username,
        password: formValues.password,
      };

      const data = await mutation.mutateAsync(variable);
      const authenticatedData = data?.authenticateUserWithPassword;
      if (authenticatedData && 'sessionToken' in authenticatedData) {
        const user = authenticatedData.item;
        dispatch({ type: 'saveUserLogin', user: user as CurrentUser });
        router.push('/home');
      } else {
        setOpen(true);
        setErrorMessage(authenticatedData?.message as string);
        setMessageType('error');
      }
    } catch (e) {
      // eslint-disable-next-line no-console
      console.error(e);
      setOpen(true);
      setErrorMessage(messages.commonError);
    } finally {
      setLoader(false);
    }
  });

  const forgotPassword = () => router.push('/forgot-password');

  if (currentUser.role) router.push('/home');

  if (loader) return <ApiLoader />;

  return (
    <>
      <CustomizedSnackbars
        open={open}
        setOpen={setOpen}
        message={errorMessage}
        type={messageType}
      />
      <div className="lg:flex">
        <div className="hidden lg:w-1/2 overflow-hidden h-screen relative lg:block">
          <Image
            src={Login}
            className="w-full h-screen absolute"
            alt="login-img"
          />
        </div>
        <div className="text-center bg-slate-100 p-5 sm:w-3/4 w-11/12 mx-auto lg:w-1/2 lg:bg-white lg:p-10 lg:mb-0">
          <div className="lg:w-4/6 mx-auto">
            <Image src={Logo} className="inline-block" alt="Logo" />
            <div className="clear-both" />
            <h1 className="my-8  text-xl ">Campus Monitoring Application</h1>
            <div className="clear-both" />

            <LoginForm
              {...{
                register,
                handleLogin,
                forgotPassword,
                rememberMe,
                setRememberMe,
                passwordVisible,
                setPasswordVisible,
              }}
            />
          </div>
        </div>
      </div>
    </>
  );
};
