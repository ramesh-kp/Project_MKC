/* eslint-disable no-useless-escape */
import { FC, useState } from 'react';
import { useRouter } from 'next/router';
import Image from 'next/image';
import { useForm } from 'react-hook-form';
import * as Yup from 'yup';
import { yupResolver } from '@hookform/resolvers/yup';
import { FormInputs, globalVariables, messages, status } from '@lib/common';
import { ResetPasswordForm } from '@components/ui/ResetPassword/ResetPasswordForm';
import { ApiLoader } from '@components/ui/CommonPage/ApiLoader';
import {
  RedeemUserPasswordResetTokenMutationVariables,
  useRedeemUserPasswordResetTokenMutation,
} from '@api/graphql';
import graphQLClient from '@lib/useGQLQuery';
import CustomizedSnackbars from '@components/ui/CommonPage/SnackBar/Snackbar';
import Logo from 'assets/logo.svg';
import Login from 'assets/login-img.jpg';

const validationSchema = Yup.object().shape({
  email: Yup.string()
    .required(globalVariables.emailRequired)
    .email(globalVariables.emailValidation),
  password: Yup.string()
    .required(globalVariables.passwordRequired)
    .matches(
      /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})/,
      globalVariables.passwordValidation,
    ),
  confirmPassword: Yup.string()
    .required(globalVariables.confirmPasswordRequired)
    .oneOf([Yup.ref('password')], globalVariables.confirmPasswordValidation),
});

export const ResetPasswordPage: FC = () => {
  const router = useRouter();
  const { query } = useRouter();
  const [open, setOpen] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string>('');
  const [messageType, setMessageType] = useState<string>(status.success);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const formOptions = {
    defaultValues: {
      email: query.mail as string,
      password: '',
      confirmPassword: '',
    },
    resolver: yupResolver(validationSchema),
  };

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<FormInputs>(formOptions);
  const mutation =
    useRedeemUserPasswordResetTokenMutation<RedeemUserPasswordResetTokenMutationVariables>(
      graphQLClient(),
    );

  const resetPassword = handleSubmit(async formValues => {
    try {
      setIsLoading(true);
      const variable = {
        email: formValues.email,
        token: query.token as string,
        password: formValues.password,
      };
      const result = await mutation.mutateAsync(variable);
      if (
        result.redeemUserPasswordResetToken?.code === 'TOKEN_REDEEMED' ||
        result.redeemUserPasswordResetToken?.code === 'TOKEN_EXPIRED' ||
        result.redeemUserPasswordResetToken?.code === 'FAILURE'
      ) {
        setErrorMessage(result.redeemUserPasswordResetToken.message);
        setMessageType(status.error);
        setOpen(true);
      } else {
        setErrorMessage('Password Reset Successfully');
        setMessageType(status.success);
        setTimeout(() => {
          router.push('/login');
        }, 3000);
      }
    } catch (e) {
      setErrorMessage(messages.commonError);
      setMessageType(status.error);
    } finally {
      setIsLoading(false);
      setOpen(true);
    }
  });

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

            <ResetPasswordForm {...{ register, errors, resetPassword }} />
          </div>
        </div>
      </div>
    </>
  );
};
