import { FC, useState } from 'react';
import { useRouter } from 'next/router';
import { useQueryClient } from 'react-query';
import { useForm } from 'react-hook-form';
import * as Yup from 'yup';
import { yupResolver } from '@hookform/resolvers/yup';
import {
  CreateResourceMutationVariables,
  InputMaybe,
  ResourceResourceCategoryType,
  ResourcesQueryVariables,
  ResourceStatusType,
  ResourceUnitType,
  UpdateResourceMutation,
  useCreateResourceMutation,
  useResourcesQuery,
  useUpdateResourceMutation,
} from '@api/graphql';
import { ResourceList } from '@components/ui/Resources/ResourceList';
import { globalVariables, messages, status } from '@lib/common';
import graphQLClient from '@lib/useGQLQuery';
import { AddResource } from '@components/ui/Resources/AddResource';
import CustomizedSnackbars from 'ui/CommonPage/SnackBar/Snackbar';
import { ApiLoader } from '@components/ui/CommonPage/ApiLoader';
import { ErrorPage } from '@components/ui/CommonPage/ErrorPage/ErrorPage';
import { ConfirmationMessage } from '@components/ui/CommonPage/ConfirmationMessage';
import { useSession } from '@lib/useSession';
import TablePagination from '@components/ui/CommonPage/TablePagination';

export type resourceType = {
  id?: string;
  name: string;
  resourceCategory: string;
  capacity: number;
  unit: string;
};

interface ResourceProps {
  tenantId: string;
}

export const Resources: FC<ResourceProps> = ({ tenantId }) => {
  const tableTake = 10;
  const confirmationText = 'Do you want to change the status of the resource ?';
  const { state } = useSession();
  const { currentUser } = state;
  const route = useRouter();
  const [pageSelected, setPageSelected] = useState<number>(1);
  const [addResource, setAddResource] = useState<boolean>(false);
  const whereCondition = {
    tenant: {
      id: {
        equals: tenantId,
      },
    },
  };
  const [variables, setVariables] = useState<ResourcesQueryVariables>({
    where: whereCondition,
    resourcesCountWhere2: whereCondition,
    take: tableTake,
    skip: 0,
  });
  const [errorMessage, setErrorMessage] = useState<string>('');
  const [messageType, setMessageType] = useState<string>('');
  const [open, setOpen] = useState<boolean>(false);
  const [loader, setLoader] = useState<boolean>(false);
  const [editData, setEditData] = useState<resourceType>();
  const [confirmationFlag, setConfirmationFlag] = useState<boolean>(false);
  const [action, setAction] = useState<string>('');
  const [actionId, setActionId] = useState<string>('');

  const {
    data: resources,
    isLoading,
    isError,
  } = useResourcesQuery(graphQLClient(), variables);

  const createMutation =
    useCreateResourceMutation<CreateResourceMutationVariables>(graphQLClient());
  const updateMutation = useUpdateResourceMutation<UpdateResourceMutation>(
    graphQLClient(),
  );
  const queryClient = useQueryClient();
  const totaldata = resources?.resourcesCount;

  const defaultValue = {
    name: '',
    resourceCategory: globalVariables.categoryType,
    capacity: 0,
    unit: 'Select Unit',
  };

  const validationSchema = Yup.object().shape({
    name: Yup.string().required('Resource Name is required'),
    resourceCategory: Yup.string().required('Resource Category is required'),
    capacity: Yup.number().test('', 'Capacity is required', val => val !== 0),
    unit: Yup.string().test(
      '',
      'Unit is required',
      val => val !== 'Select Unit',
    ),
  });

  const formOptions = {
    defaultValues: defaultValue,
    resolver: yupResolver(validationSchema),
  };

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    control,
  } = useForm<resourceType>(formOptions);

  const actionConfirm = (action: string, deviceId: string) => {
    setConfirmationFlag(true);
    setAction(action);
    setActionId(deviceId);
  };

  const closeConfirmation = () => {
    setConfirmationFlag(false);
    setAction('');
    setActionId('');
  };

  const actionSubmit = async () => {
    try {
      setConfirmationFlag(false);
      setLoader(true);
      const variable = {
        where: {
          id: actionId,
        },
        data: {
          status:
            action === 'Deactivate'
              ? ResourceStatusType.Inactive
              : ResourceStatusType.Active,
        },
      };
      await updateMutation.mutateAsync(variable);
      queryClient.invalidateQueries();
      setErrorMessage(
        action === 'Deactivate'
          ? messages.sensorDeactivateMessage
          : messages.sensorActiveMessage,
      );
      setMessageType(status.success);
    } catch (e) {
      // eslint-disable-next-line no-console
      console.error(e);
      setErrorMessage(messages.commonError);
      setMessageType(status.error);
    } finally {
      setLoader(false);
      setOpen(true);
      setAction('');
      setActionId('');
    }
  };

  const submitForm = handleSubmit(async formValues => {
    try {
      setLoader(true);
      const resourceData = {
        name: formValues.name,
        resourceCategory:
          formValues.resourceCategory as ResourceResourceCategoryType,
        tenant: {
          connect: {
            id: tenantId,
          },
        },
        capacity: formValues.capacity,
        unit: formValues.unit as ResourceUnitType,
      };

      const createQueryVariables = {
        data: resourceData,
      };
      const updateQueryVariables = {
        where: {
          id: editData?.id,
        },
        data: resourceData,
      };

      if (editData) {
        await updateMutation.mutateAsync(updateQueryVariables);
        setErrorMessage('Resource updated successfully');
        setMessageType(status.success);
      } else {
        await createMutation.mutateAsync(createQueryVariables);
        setErrorMessage('Resource created successfully');
        setMessageType(status.success);
      }
    } catch (e) {
      // eslint-disable-next-line no-console
      console.error(e);
      setErrorMessage(messages.commonError);
      setMessageType(status.error);
    } finally {
      setLoader(false);
      queryClient.invalidateQueries();
      setOpen(true);
      setAddResource(false);
      reset(defaultValue);
      setEditData(undefined);
    }
  });

  const handleClose = () => {
    setAddResource(false);
    reset(defaultValue);
    setEditData(undefined);
    setLoader(false);
  };

  const pagination = async (pageKey: number) => {
    setPageSelected(pageKey + 1);
    const skipvalue = pageKey * tableTake;
    setVariables(prev => {
      return { ...prev, skip: skipvalue };
    });
  };

  const handleEdit = (editRow: resourceType) => {
    setEditData(editRow);
    setAddResource(true);
    reset({
      name: editRow.name,
      resourceCategory: editRow.resourceCategory,
      capacity: editRow.capacity,
      unit: editRow.unit,
    });
  };

  if (currentUser.role === undefined) route.push('/login');
  if (isLoading || loader) return <ApiLoader />;
  if (isError) return <ErrorPage />;

  return (
    <>
      <ResourceList
        resources={resources?.resources}
        {...{ setAddResource, handleEdit, actionConfirm }}
      />
      <CustomizedSnackbars
        {...{ open, setOpen }}
        message={errorMessage}
        type={messageType}
      />

      <TablePagination
        totaldata={totaldata ?? 0}
        {...{ pagination, tableTake, pageSelected }}
      />
      {addResource && (
        <AddResource
          {...{
            handleClose,
            register,
            errors,
            control,
            submitForm,
            editData,
          }}
        />
      )}
      {confirmationFlag && (
        <ConfirmationMessage
          {...{ closeConfirmation, confirmationText }}
          confirmedAction={actionSubmit}
        />
      )}
    </>
  );
};
