import { Dispatch, FC, SetStateAction, useState } from 'react';
import { useForm } from 'react-hook-form';
import { useQueryClient } from 'react-query';
import * as Yup from 'yup';
import { yupResolver } from '@hookform/resolvers/yup';
import {
  FormInputs,
  globalVariables,
  messages,
  status,
  UsersType,
} from '@lib/common';
import CustomizedSnackbars from 'ui/CommonPage/SnackBar/Snackbar';
import { AddUserForm } from '@components/ui/UsersTable/AddUser/AddUser';
import {
  CreateUserMutation,
  UpdateUserMutation,
  useCreateUserMutation,
  UserRoleType,
  useUpdateUserMutation,
} from '@api/graphql';
import graphQLClient from '@lib/useGQLQuery';
import { ApiLoader } from '@components/ui/CommonPage/ApiLoader';

export interface AddUserPageProps {
  setAddUserFlag: Dispatch<SetStateAction<boolean>>;
  editData: UsersType;
  setEditData: Dispatch<SetStateAction<UsersType>>;
  setOpen: Dispatch<SetStateAction<boolean>>;
  setErrorMessage: Dispatch<SetStateAction<string>>;
  setMessageType: Dispatch<SetStateAction<string>>;
}

export const AddUserPage: FC<AddUserPageProps> = ({
  setAddUserFlag,
  editData,
  setEditData,
  setOpen,
  setErrorMessage,
  setMessageType,
}) => {
  const [loader, setLoader] = useState<boolean>(false);
  const createMutation = useCreateUserMutation<CreateUserMutation>(
    graphQLClient(),
  );
  const updateMutation = useUpdateUserMutation<UpdateUserMutation>(
    graphQLClient(),
  );
  const queryClient = useQueryClient();

  const validationSchema = Yup.object().shape({
    fullName: Yup.string()
      .required(globalVariables.nameRequired)
      .matches(/^[aA-zZ\s]+$/, globalVariables.nameValidation),
    email: Yup.string()
      .required(globalVariables.emailRequired)
      .email(globalVariables.emailValidation)
      .lowercase(),
    phone: Yup.string()
      .required(globalVariables.phoneRequired)
      .matches(
        /^[+]?[(]?[0-9]{3}[)]?[-\s.]?[0-9]{3}[-\s.]?[0-9]{4,6}$/im,
        globalVariables.phoneValidation,
      ),
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

  const validationSchemaForEdit = Yup.object().shape({
    fullName: Yup.string()
      .required(globalVariables.nameRequired)
      .matches(/^[aA-zZ\s]+$/, globalVariables.nameValidation),
    email: Yup.string()
      .required(globalVariables.emailRequired)
      .email(globalVariables.emailValidation),
    phone: Yup.string()
      .required(globalVariables.phoneRequired)
      .matches(
        /^[+]?[(]?[0-9]{3}[)]?[-\s.]?[0-9]{3}[-\s.]?[0-9]{4,6}$/im,
        globalVariables.phoneValidation,
      ),
  });

  let userFormValues: object;

  if (editData) {
    userFormValues = {
      fullName: editData.name,
      email: editData.email,
      phone: editData.phone,
    };
  } else {
    userFormValues = {
      fullName: '',
      email: '',
      phone: '',
      password: '',
      confirmPassword: '',
    };
  }
  const formOptions = {
    defaultValues: userFormValues,
    resolver: yupResolver(
      editData ? validationSchemaForEdit : validationSchema,
    ),
  };

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<FormInputs>(formOptions);

  const addUser = handleSubmit(async formValues => {
    try {
      setLoader(true);
      const { fullName, email, phone, password } = formValues;
      if (editData) {
        const variable = {
          where: {
            id: editData.id,
          },
          data: {
            name: fullName,
            email,
            phone,
          },
        };
        await updateMutation.mutateAsync(variable);
        queryClient.invalidateQueries();
        setErrorMessage('User updated successfully');
      } else {
        const variable = {
          data: {
            name: fullName,
            email,
            password,
            phone,
            role: UserRoleType.Tenant,
          },
        };
        await createMutation.mutateAsync(variable);
        queryClient.invalidateQueries();
        setErrorMessage(messages.usercreatedMessage);
      }
      setMessageType(status.success);
    } catch (e) {
      // eslint-disable-next-line no-console
      console.error(e);
      setErrorMessage(messages.commonError);
      setMessageType(status.error);
    } finally {
      setLoader(false);
      setOpen(true);
      setEditData(null);
      setAddUserFlag(false);
    }
  });

  const handleClose = () => {
    setEditData(null);
    setAddUserFlag(false);
  };

  if (loader) return <ApiLoader />;
  return (
    <AddUserForm {...{ register, errors, handleClose, addUser, editData }} />
  );
};

export default AddUserPage;
