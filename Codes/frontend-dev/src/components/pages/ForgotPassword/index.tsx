import { useState, FC } from 'react';
import { useRouter } from 'next/router';
import Image from 'next/image';
import { useForm } from 'react-hook-form';
import * as Yup from 'yup';
import { yupResolver } from '@hookform/resolvers/yup';
import graphQLClient from '@lib/useGQLQuery';
import { ForgotPasswordForm } from '../../ui/ForgotPassword/ForgotPasswordForm';
import { globalVariables, status } from '@lib/common';
import {
  SendUserPasswordResetLinkMutationVariables,
  useSendUserPasswordResetLinkMutation,
} from '@api/graphql';
import CustomizedSnackbars from '@components/ui/CommonPage/SnackBar/Snackbar';
import Logo from 'assets/logo.svg';
import Login from 'assets/login-img.jpg';
import { ApiLoader } from '@components/ui/CommonPage/ApiLoader';
const validationSchema = Yup.object().shape({
  email: Yup.string()
    .required(globalVariables.emailRequired)
    .email(globalVariables.emailValidation),
});

export const ForgotPasswordPage: FC = () => {
  const router = useRouter();
  const [open, setOpen] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string>('');
  const [messageType, setMessageType] = useState<string>(status.success);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const formOptions = {
    defaultValues: {
      email: '',
    },
    resolver: yupResolver(validationSchema),
  };
  const passwordResetSuccessMessage =
    'Please Check your inbox including spam folder for password reset link. Please ensure that you have provided the correct Email id. ';

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<{ email: string }>(formOptions);

  const sendUserPasswordResetLink =
    useSendUserPasswordResetLinkMutation<SendUserPasswordResetLinkMutationVariables>(
      graphQLClient(),
    );

  const sendEmail = handleSubmit(async formValues => {
    try {
      setIsLoading(true);
      await sendUserPasswordResetLink.mutateAsync(formValues);
      setErrorMessage(passwordResetSuccessMessage);
      setMessageType(status.success);
    } catch (e) {
      // eslint-disable-next-line no-console
      console.error(e);
      setErrorMessage('Email Id is not verified. Please contact admin.');
      setMessageType(status.error);
    } finally {
      setIsLoading(false);
      setOpen(true);
            setTimeout(() => {
              router.push('/login');
            }, 3000);
    }
  });

  const backToLogin = () => router.push('/login');

  if (isLoading) return <ApiLoader />;

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
        <div className="rounded-lg text-center bg-slate-100 p-5 sm:w-3/4 w-11/12 mx-auto mt-10 mb-10 lg:w-1/2 lg:bg-white lg:p-10 lg:mb-0">
          <div className="lg:w-4/6 mx-auto">
            <Image src={Logo} className="inline-block" alt="Logo" />
            <div className="clear-both" />
            <h1 className="my-8 text-xl ">Campus Monitoring Application</h1>
            <div className="clear-both" />

            <ForgotPasswordForm
              {...{ register, errors, sendEmail, backToLogin }}
            />
          </div>
        </div>
      </div>
    </>
  );
};
