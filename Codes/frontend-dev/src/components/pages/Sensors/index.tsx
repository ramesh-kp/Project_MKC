import { FC, useState } from 'react';
import Image from 'next/image';
import { useQueryClient } from 'react-query';
import { useForm } from 'react-hook-form';
import { useRouter } from 'next/router';
import * as Yup from 'yup';
import { yupResolver } from '@hookform/resolvers/yup';
import { SensorList } from 'ui/Sensor/SensorList';
import { AddSensor } from '@components/ui/Sensor/AddSensor';
import {
  DeviceType,
  globalVariables,
  messages,
  SensorFormType,
  status,
  tenantOptionalFields,
} from '@lib/common';
import SensorIcon from 'assets/sensors-white.png';

import {
  CreateDeviceMutation,
  DevicesQuery,
  DevicesQueryVariables,
  DeviceStatusType,
  UpdateDeviceMutation,
  useCreateDeviceMutation,
  useDevicesQuery,
  useDeviceTypesQuery,
  useFacilitiesUnderTenantQuery,
  UserRoleType,
  useUpdateDeviceMutation,
} from '@api/graphql';
import graphQLClient from '@lib/useGQLQuery';
import CustomizedSnackbars from 'ui/CommonPage/SnackBar/Snackbar';
import TablePagination from '@components/ui/CommonPage/TablePagination';
import { ApiLoader } from '@components/ui/CommonPage/ApiLoader';
import { ErrorPage } from '@components/ui/CommonPage/ErrorPage/ErrorPage';
import { ConfirmationMessage } from '@components/ui/CommonPage/ConfirmationMessage';
import { useSession } from '@lib/useSession';
import { NoRecords } from '@components/ui/CommonPage/NoRecords/NoRecords';

const validationSchema = Yup.object().shape({
  deviceName: Yup.string().required(globalVariables.deviceNameRequired),
  deviceId: Yup.string().required(globalVariables.deviceIdRequired),
  edgeDeviceId: Yup.string().required(globalVariables.edgeDeviceIdRequired),
  portNumber: Yup.string().required(globalVariables.devicePortRequired),
  description: Yup.string().required(globalVariables.descriptionRequired),
});

interface SensorListProps {
  sensorList?: DevicesQuery['devices'];
  sensorCount?: number;
  tenantDetailView?: boolean;
  tenantId?: string;
}

export const SensorListPage: FC<SensorListProps> = ({
  sensorList,
  sensorCount,
  tenantDetailView,
  tenantId,
}) => {
  const tableTake = 10;
  const confirmationText = 'Do you want to change the status of the sensor ?';
  const { state } = useSession();
  const { currentUser } = state;
  const route = useRouter();
  const [pageSelected, setPageSelected] = useState<number>(1);
  const [addSensor, setAddSensor] = useState<boolean>(false);
  const [variables, setVariables] = useState<DevicesQueryVariables>({
    take: tableTake,
    skip: 0,
    where: {
      tenant: null,
    },
    devicesCountWhere2: {
      tenant: null,
    },
  });
  const [errorMessage, setErrorMessage] = useState<string>('');
  const [messageType, setMessageType] = useState<string>('');
  const [open, setOpen] = useState<boolean>(false);
  const [loader, setLoader] = useState<boolean>(false);
  const [editData, setEditData] = useState<DeviceType>();
  const [confirmationFlag, setConfirmationFlag] = useState<boolean>(false);
  const [action, setAction] = useState<string>('');
  const [actionId, setActionId] = useState<string>('');

  const {
    data: devices,
    isLoading,
    isError,
  } = useDevicesQuery(graphQLClient(), variables);
  const { data: facilities } = useFacilitiesUnderTenantQuery(graphQLClient(), {
    where: {
      tenants: {
        some: {
          id: {
            equals: tenantId,
          },
        },
      },
    },
  });
  const { data: deviceType } = useDeviceTypesQuery(graphQLClient(), {});
  const createMutation = useCreateDeviceMutation<CreateDeviceMutation>(
    graphQLClient(),
  );
  const updateMutation = useUpdateDeviceMutation<UpdateDeviceMutation>(
    graphQLClient(),
  );
  const queryClient = useQueryClient();
  const totaldata = tenantDetailView ? sensorCount : devices?.devicesCount;

  const sensorDefaultValues = {
    deviceName: '',
    deviceId: '',
    edgeDeviceId: '',
    portNumber: '',
    sensorType: globalVariables.sensorType,
    resourceType: globalVariables.resourceType,
    resource: globalVariables.resource,
    facility: globalVariables.tenantFacility,
    description: '',
  };

  const formOptions = {
    defaultValues: sensorDefaultValues,
    resolver: yupResolver(validationSchema),
  };

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    control,
  } = useForm<SensorFormType>(formOptions);

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
              ? DeviceStatusType.Inactive
              : DeviceStatusType.Active,
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
      const {
        deviceName: name,
        deviceId,
        edgeDeviceId,
        portNumber,
        description,
        facility,
        sensorType,
        resource,
      } = formValues;

      let optionalFields: tenantOptionalFields = {};

      if (sensorType !== globalVariables.sensorType) {
        optionalFields.deviceType = {
          connect: {
            id: sensorType,
          },
        };
      }
      if (facility !== 'Tenant Facility' && facility !== undefined) {
        optionalFields.tenant = {
          connect: {
            id: tenantId as string,
          },
        };
        optionalFields.facility = {
          connect: {
            id: facility as string,
          },
        };
      }

      if (resource !== globalVariables.resource)
        optionalFields.resource = {
          connect: {
            id: resource,
          },
        };

      const createQueryVariables = {
        data: {
          ...optionalFields,
          name,
          deviceId,
          edgeDeviceId,
          portNumber: portNumber,
          description,
        },
      };
      const updateQueryVariables = {
        where: {
          id: editData?.id,
        },
        data: {
          ...optionalFields,
          name,
          deviceId,
          edgeDeviceId,
          portNumber: portNumber,
          description,
        },
      };
      if (editData) {
        await updateMutation.mutateAsync(updateQueryVariables);
        setErrorMessage(messages.sensorUpdateMessage);
        setMessageType(status.success);
      } else {
        await createMutation.mutateAsync(createQueryVariables);
        setErrorMessage(messages.sensorCreateMessage);
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
      setAddSensor(false);
      reset(sensorDefaultValues);
      setEditData(undefined);
    }
  });

  const handleClose = () => {
    setAddSensor(false);
    reset(sensorDefaultValues);
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

  const handleEdit = (editRow: DeviceType) => {
    setEditData(editRow);
    setAddSensor(true);
    reset({
      deviceName: editRow?.name as string,
      deviceId: editRow?.deviceId as string,
      edgeDeviceId: editRow?.edgeDeviceId as string,
      portNumber: editRow?.portNumber as string,
      sensorType: editRow?.deviceType?.id as string,
      resourceType: editRow?.resource?.resourceCategory as string,
      resource: editRow?.resource?.id as string,
      facility: editRow?.facility?.id as string,
      description: editRow?.description as string,
    });
  };

  const sensorsData = tenantDetailView ? sensorList : devices?.devices;

  if (currentUser.role === undefined) route.push('/login');
  if (isLoading || loader) return <ApiLoader />;
  if (isError) return <ErrorPage />;

  return (
    <>
      <CustomizedSnackbars
        {...{ open, setOpen }}
        message={errorMessage}
        type={messageType}
      />
      <div className="p-6 bg-white rounded-lg mt-6 mb-10">
        <h1 className="inline-block text-2xl font-semibold">
          {tenantDetailView ? 'Sensors' : 'Common Sensors'}
        </h1>
        {currentUser.role === UserRoleType.Admin && (
          <button
            type="button"
            className="bg-sky-600 float-right text-white px-4 py-2 rounded-md text-lg font-semibold hover:bg-sky-700"
            onClick={() => setAddSensor(true)}
          >
            <Image
              src={SensorIcon}
              className="inline-block mr-1"
              alt="sensorWhite"
            />{' '}
            Add Sensor
          </button>
        )}
        <div className="clear-both" />
        {sensorsData?.length === 0 ? (
          <NoRecords />
        ) : (
          <div className="flex flex-col">
            <div className="-my-2 mt-4 sm:-mx-6 lg:-mx-8">
              <div className="py-2 align-middle inline-block min-w-full sm:px-6 lg:px-8">
                <SensorList
                  {...{ setAddSensor, handleEdit, actionConfirm }}
                  deviceData={sensorsData}
                  tenantDetailView={tenantDetailView as boolean}
                />
                <TablePagination
                  totaldata={totaldata ?? 0}
                  {...{ pagination, tableTake, pageSelected }}
                />
              </div>
            </div>
          </div>
        )}
      </div>
      {addSensor && (
        <AddSensor
          {...{
            handleClose,
            register,
            errors,
            control,
            submitForm,
            editData,
            tenantId,
          }}
          facilities={facilities?.facilities}
          deviceTypes={deviceType?.deviceTypes}
          tenantDetailView={tenantDetailView as boolean}
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
