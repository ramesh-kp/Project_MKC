import { useState } from 'react';
import { useRouter } from 'next/router';
import { useQueryClient } from 'react-query';
import { useForm } from 'react-hook-form';
import * as Yup from 'yup';
import { yupResolver } from '@hookform/resolvers/yup';
import {
  Exact,
  TenantUpdateInput,
  TenantWhereUniqueInput,
  UpdateTenantMutation,
  useDevicesQuery,
  useFacilitiesQuery,
  useTenantDetailsQuery,
  useUpdateTenantMutation,
} from '@api/graphql';
import { TenantDetailsView } from '@components/ui/TenantTable/TenantDetails';
import graphQLClient from '@lib/useGQLQuery';
import { ApiLoader } from '@components/ui/CommonPage/ApiLoader';
import { ErrorPage } from '@components/ui/CommonPage/ErrorPage/ErrorPage';
import { FacilityType, TenantList } from '../Tenant';
import { useSession } from '@lib/useSession';
import {
  globalVariables,
  messages,
  status,
  tenantData,
  TenantFormInputs,
  tenantType,
} from '@lib/common';
import { AddTenantForm } from '@components/ui/TenantTable/AddTenant';
import CustomizedSnackbars from 'ui/CommonPage/SnackBar/Snackbar';
import { SensorListPage } from '@components/pages/Sensors';
import { Resources } from '@components/pages/Resources';

const validationSchema = Yup.object().shape({
  name: Yup.string().required(globalVariables.tenantName),
  location: Yup.string().required(globalVariables.location),
  owner: Yup.string().test(
    '',
    globalVariables.owner,
    val => val !== globalVariables.user,
  ),
  description: Yup.string().required(globalVariables.description),
  facilities: Yup.array().test(
    '',
    globalVariables.facilities,
    val => val?.length !== 0,
  ),
});

export const TenantDetailsPage = () => {
  const router = useRouter();
  const { state } = useSession();
  const { currentUser } = state;
  const { id } = router.query;
  const [tab, setTab] = useState<string>(globalVariables.tenant);
  const [addTenantFlag, setAddTenantFlag] = useState<boolean>(false);
  const [editRowId, setEditRowId] = useState<string>('');
  const [facilityArray, setFacilityArray] = useState<[]>([]);
  const [loader, setLoader] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string>('');
  const [messageType, setMessageType] = useState<string>('');
  const [open, setOpen] = useState<boolean>(false);

  const tabs = [
    { value: 'tenant', label: 'Sub-Tenants' },
    { value: 'sensor', label: 'Sensors' },
    { value: 'resource', label: 'Resources' },
  ];

  const initialValues = {
    name: '',
    location: '',
    owner: globalVariables.user,
    description: '',
    facilities: [],
  };

  const formOptions = {
    defaultValues: initialValues,
    resolver: yupResolver(validationSchema),
  };
  const {
    register,
    handleSubmit,
    formState: { errors },
    setValue,
    reset,
  } = useForm<TenantFormInputs>(formOptions);

  const variables = {
    where: {
      id: id as string,
    },
  };

  const whereCondition = {
    tenant: {
      id: {
        equals: id as string,
      },
    },
  };

  const deviceVariables = {
    take: null,
    skip: 0,
    where: whereCondition,
    devicesCountWhere2: whereCondition,
  };

  const {
    data: tenantDetails,
    isLoading,
    isError,
  } = useTenantDetailsQuery(graphQLClient(), variables);

  const { data: devices } = useDevicesQuery(graphQLClient(), deviceVariables);
  const { data: facilityData } = useFacilitiesQuery(graphQLClient(), {});
  const updateMutation = useUpdateTenantMutation<UpdateTenantMutation>(
    graphQLClient(),
  );
  const queryClient = useQueryClient();

  if (currentUser.role === undefined) router.push('/login');
  if (isLoading) return <ApiLoader />;
  if (isError) return <ErrorPage />;

  const editData = (data: tenantType) => {
    const { id, name, location, owners, description, facilities } = data;
    type FacilityType = { id: string; name: string };
    const facility = facilities.map((facility: FacilityType) => {
      return {
        value: facility.id,
        label: facility.name,
      };
    });
    const ownersData =
      owners.length !== 0 ? owners[0].id : globalVariables.user;
    setEditRowId(id);
    setFacilityArray(facility as []);
    setAddTenantFlag(true);
    reset({
      name,
      location,
      owner: ownersData,
      description,
      facilities: facility,
    });
  };

  const resetData = () => {
    setLoader(false);
    setAddTenantFlag(false);
    queryClient.invalidateQueries();
    reset();
    setEditRowId('');
    setFacilityArray([]);
    setOpen(true);
  };

  const updateTenant = async (
    queryData: Exact<{
      where: TenantWhereUniqueInput;
      data: TenantUpdateInput;
    }>,
  ) => {
    try {
      await updateMutation.mutateAsync(queryData);
      setErrorMessage(messages.tenantUpdateMessage);
      setMessageType(status.success);
    } catch (e) {
      // eslint-disable-next-line no-console
      console.error(e);
      setErrorMessage(messages.commonError);
      setMessageType(status.error);
    } finally {
      resetData();
    }
  };

  const submitTenant = handleSubmit(async formValues => {
    setLoader(true);
    const { name, location, owner, description, facilities } = formValues;
    type facilityType = { id: string };

    const facilitiesToConnect = facilities.reduce(
      (acc: facilityType[], facility: FacilityType) => [
        ...acc,
        {
          id: facility.value,
        },
      ],
      [] as facilityType[],
    );

    const filteredFacilities = facilityArray.filter(
      (facility: FacilityType) =>
        !facilitiesToConnect.some(
          (facilityData: facilityType) => facilityData.id === facility.value,
        ),
    );

    const facilitiesToDisconnect = filteredFacilities.reduce(
      (acc, facilityValues: FacilityType) => [
        ...acc,
        {
          id: facilityValues.value,
        },
      ],
      [] as facilityType[],
    );

    const ownersData =
      owner !== globalVariables.user
        ? {
            connect: [
              {
                id: owner,
              },
            ],
          }
        : null;

    let formData: tenantData = {
      name,
      location,
      description,
      owners: ownersData,
      facilities:
        editRowId !== ''
          ? {
              connect: facilitiesToConnect,
              disconnect: facilitiesToDisconnect,
            }
          : {
              connect: facilitiesToConnect,
            },
    };
    const queryData = {
      where: {
        id: editRowId,
      } as TenantWhereUniqueInput,
      data: formData as unknown as TenantUpdateInput,
    };
    updateTenant(queryData);
  });

  const cancelPopup = () => {
    setAddTenantFlag(false);
    reset();
    setFacilityArray([]);
    setEditRowId('');
  };

  if (isLoading || loader) return <ApiLoader />;
  if (isError) return <ErrorPage />;

  return (
    <>
      <CustomizedSnackbars
        {...{ open, setOpen }}
        message={errorMessage}
        type={messageType}
      />
      <TenantDetailsView
        tenantDetails={tenantDetails?.tenant}
        {...{ editData }}
      />
      <div className="p-6 bg-white rounded-lg mt-6 mb-10">
        <div className="tabs h-12 border-b-2 border-sky-600 tab-outer">
          {tabs.map(tabOption => (
            <label
              key={tabOption.value}
              className={
                tab === tabOption.value
                  ? 'tab tab-lifted text-xl font-medium tab-active'
                  : 'tab tab-lifted text-sky-600 text-xl font-medium'
              }
              onClick={() => setTab(tabOption.value)}
            >
              {tabOption.label}
            </label>
          ))}
        </div>
        {tab === tabs[0].value ? (
          <TenantList tenantList={tenantDetails?.tenant} tenantDetailView />
        ) : tab === tabs[1].value ? (
          <SensorListPage
            sensorList={devices?.devices}
            sensorCount={devices?.devicesCount as number | undefined}
            tenantDetailView
            tenantId={tenantDetails?.tenant?.id as string}
          />
        ) : (
          <Resources tenantId={id as string} />
        )}
      </div>
      {addTenantFlag && (
        <AddTenantForm
          facilityData={facilityData?.facilities}
          tenantDetailView={false}
          {...{
            setAddTenantFlag,
            register,
            errors,
            submitTenant,
            setValue,
            reset,
            facilityArray,
            cancelPopup,
            editRowId,
          }}
        />
      )}
    </>
  );
};
