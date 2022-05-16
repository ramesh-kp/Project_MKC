import { FC, useState } from 'react';
import { useRouter } from 'next/router';
import { useForm } from 'react-hook-form';
import { useQueryClient } from 'react-query';
import * as Yup from 'yup';
import { yupResolver } from '@hookform/resolvers/yup';
import Image from 'next/image';
import SearchIcon from 'assets/search_icon.png';
import TenantIcon from 'assets/tenants_white.png';
import TablePagination from '@components/ui/CommonPage/TablePagination';
import { TenantListView } from '@components/ui/TenantTable/TenantListView';
import {
  CreateTenantMutation,
  Exact,
  InputMaybe,
  QueryMode,
  TenantDetailsQuery,
  TenantsQueryVariables,
  TenantStatusType,
  TenantUpdateInput,
  TenantWhereUniqueInput,
  UpdateTenantMutation,
  useCreateTenantMutation,
  useFacilitiesQuery,
  UserRoleType,
  useTenantsQuery,
  useUpdateTenantMutation,
} from '@api/graphql';
import graphQLClient from '@lib/useGQLQuery';
import { AddTenantForm } from '@components/ui/TenantTable/AddTenant';
import CustomizedSnackbars from 'ui/CommonPage/SnackBar/Snackbar';
import {
  globalVariables,
  messages,
  orderAsc,
  status,
  tenantData,
  TenantFormInputs,
  tenantType,
} from '@lib/common';
import { ApiLoader } from '@components/ui/CommonPage/ApiLoader';
import { ErrorPage } from '@components/ui/CommonPage/ErrorPage/ErrorPage';
import { ConfirmationMessage } from '@components/ui/CommonPage/ConfirmationMessage';
import { useSession } from '@lib/useSession';
import { NoRecords } from '@components/ui/CommonPage/NoRecords/NoRecords';

const mandatoryValidationFields = {
  name: Yup.string().required(globalVariables.tenantName),
  location: Yup.string().required(globalVariables.location),
  description: Yup.string().required(globalVariables.description),
  facilities: Yup.array().test(
    '',
    globalVariables.facilities,
    val => val?.length !== 0,
  ),
};

const optionalValidationFields = {
  owner: Yup.string().test(
    '',
    globalVariables.owner,
    val => val !== globalVariables.user,
  ),
};

export interface TenantListProps {
  tenantDetailView?: boolean;
  tenantList?: TenantDetailsQuery['tenant'];
  home?: boolean;
}

export interface FacilityType {
  value: string;
  label: string;
}

export const TenantList: FC<TenantListProps> = ({
  tenantDetailView,
  tenantList,
  home,
}) => {
  const tableTake = 10;
  const initialValues = {
    name: '',
    location: '',
    owner: globalVariables.user,
    description: '',
    facilities: [],
  };
  const validationFields = {
    ...mandatoryValidationFields,
    ...optionalValidationFields,
  };

  const validationSchema = Yup.object().shape(
    tenantDetailView ? mandatoryValidationFields : validationFields,
  );
  const { state } = useSession();
  const { currentUser } = state;
  const route = useRouter();
  const confirmationText = 'Do you want to change the status of the tenant ?';
  const [pageSelected, setPageSelected] = useState<number>(1);
  const [searchItem, setSearchItem] = useState<string>('');
  const [addTenantFlag, setAddTenantFlag] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string>('');
  const [messageType, setMessageType] = useState<string>('');
  const [open, setOpen] = useState<boolean>(false);
  const [loader, setLoader] = useState<boolean>(false);
  const [editRowId, setEditRowId] = useState<string>('');
  const [facilityArray, setFacilityArray] = useState<FacilityType[]>([]);
  const [confirmationFlag, setConfirmationFlag] = useState<boolean>(false);
  const [action, setAction] = useState<string>('');
  const [actionId, setActionId] = useState<string>('');
  const queryClient = useQueryClient();
  const createMutation = useCreateTenantMutation<CreateTenantMutation>(
    graphQLClient(),
  );
  const updateMutation = useUpdateTenantMutation<UpdateTenantMutation>(
    graphQLClient(),
  );

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

  const searchDefault = {
    contains: '',
    mode: 'insensitive' as InputMaybe<QueryMode> | undefined,
  };

  const whereCondition = {
    OR: [
      {
        name: searchDefault,
      },
      {
        location: searchDefault,
      },
      {
        owners: {
          some: {
            name: searchDefault,
          },
        },
      },
    ],
    parent: null,
  };

  const queryVariables = {
    where: whereCondition,
    orderBy: orderAsc,
    take: tableTake,
    skip: 0,
    tenantsCountWhere2: whereCondition,
  };
  const [variables, setVaribles] =
    useState<TenantsQueryVariables>(queryVariables);

  const { data, isLoading, isError } = useTenantsQuery(
    graphQLClient(),
    variables,
  );

  const { data: facilityData } = useFacilitiesQuery(graphQLClient(), {});

  const totaldata = tenantDetailView
    ? tenantList?.childrenCount
    : data?.tenantsCount;

  const resetData = () => {
    setLoader(false);
    setAddTenantFlag(false);
    queryClient.invalidateQueries();
    reset();
    setEditRowId('');
    setFacilityArray([]);
    setOpen(true);
    setPageSelected(1);
    setVaribles(prev => {
      return {
        ...prev,
        skip: 0,
      };
    });
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

  const createTenant = async (
    queryData: Exact<{
      data: TenantUpdateInput;
    }>,
  ) => {
    try {
      await createMutation.mutateAsync(queryData);
      setErrorMessage(messages.tenantCreateMessage);
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

    const alreadyConnectedOwners = data?.tenants?.find(
      tenant => tenant.id === editRowId,
    )?.owners;

    const ownersToConnect = [
      {
        id: owner,
      },
    ];

    const ownersToDisconnect = alreadyConnectedOwners?.map(owner => {
      return { id: owner.id };
    });

    const ownersData =
      owner !== globalVariables.user
        ? {
            connect: ownersToConnect,
            disconnect: ownersToDisconnect,
          }
        : null;

    let formData: tenantData = {
      name,
      location,
      description,

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

    if (tenantDetailView) {
      formData.parent = {
        connect: {
          id: tenantList?.id as string,
        },
      };
    } else {
      formData.owners = ownersData;
    }

    if (editRowId !== '') {
      const queryData = {
        where: {
          id: editRowId,
        } as TenantWhereUniqueInput,
        data: formData as unknown as TenantUpdateInput,
      };

      updateTenant(queryData);
    } else {
      const queryData = {
        data: formData as unknown as TenantUpdateInput,
      };
      createTenant(queryData);
    }
  });

  const actionConfirm = (action: string, tenantId: string) => {
    setConfirmationFlag(true);
    setAction(action);
    setActionId(tenantId);
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
              ? TenantStatusType.Inactive
              : TenantStatusType.Active,
        },
      };
      await updateMutation.mutateAsync(variable);
      queryClient.invalidateQueries();
      setErrorMessage(
        action === 'Deactivate'
          ? messages.tenantDeactivateMessage
          : messages.tenantActiveMessage,
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

  const showPopup = () => {
    reset(initialValues);
    setAddTenantFlag(true);
  };

  const cancelPopup = () => {
    setAddTenantFlag(false);
    reset();
    setFacilityArray([]);
    setEditRowId('');
  };

  const searchItems = () => {
    setSearchItem(searchItem);

    const convertedSearchItem = {
      contains: searchItem,
      mode: 'insensitive' as InputMaybe<QueryMode> | undefined,
    };

    const condition = {
      OR: [
        {
          name: convertedSearchItem,
        },
        {
          location: convertedSearchItem,
        },
        {
          owners: {
            some: {
              name: convertedSearchItem,
            },
          },
        },
      ],
      parent: null,
    };

    setVaribles(prev => {
      return {
        ...prev,
        where: condition,
        tenantsCountWhere2: condition,
        skip: 0,
      };
    });
    setPageSelected(1);
  };

  const pagination = async (pageKey: number) => {
    setPageSelected(pageKey + 1);
    const skipvalue = pageKey * tableTake;
    setVaribles(prev => {
      return { ...prev, skip: skipvalue };
    });
  };

  const tenantsData = tenantDetailView ? tenantList?.children : data?.tenants;

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
      <div className="p-6 bg-white rounded-lg mb-10">
        <h1 className="inline-block text-2xl font-semibold">
          {tenantDetailView ? 'Sub-Tenants' : 'Tenants'}
        </h1>
        <div className="float-right flex">
          <div className="relative mr-4 h-10 overflow-hidden rounded-md">
            <input
              value={searchItem}
              type="text"
              className="mr-5 px-3 py-2 bg-slate-200 focus-visible:outline-0 text-md font-medium text-gray-700"
              placeholder="Search here..."
              onChange={e => setSearchItem && setSearchItem(e.target.value)}
              onKeyDown={e => {
                if (e.key === 'Enter') searchItems && searchItems();
              }}
            />
            <button
              type="button"
              className="bg-sky-600 px-3 pt-1 h-10 absolute top-0 right-0 hover:bg-sky-700"
              onClick={() => searchItems && searchItems()}
            >
              <Image
                src={SearchIcon}
                className="inline-block search_icon"
                alt=""
              />
            </button>
          </div>
          {currentUser.role === UserRoleType.Admin && Boolean(home) === false && (
            <button
              type="button"
              className="bg-sky-600 float-right text-white px-4 py-2 rounded-md text-lg font-semibold hover:bg-sky-700"
              onClick={() => showPopup && showPopup()}
            >
              <Image
                src={TenantIcon}
                className="inline-block mr-1"
                alt="userWhite"
              />{' '}
              {tenantDetailView ? 'Add Sub-Tenant' : 'Add Tenant'}
            </button>
          )}
        </div>
        <div className="clear-both" />
        {tenantsData?.length === 0 ? (
          <NoRecords />
        ) : (
          <div className="flex flex-col">
            <div className="-my-2 mt-4 sm:-mx-6 lg:-mx-8">
              <div className="py-2 align-middle inline-block min-w-full sm:px-6 lg:px-8">
                <TenantListView
                  tenantList={tenantsData}
                  tenantDetailView={tenantDetailView as boolean}
                  {...{
                    editData,
                    actionConfirm,
                  }}
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
      {addTenantFlag && (
        <AddTenantForm
          facilityData={facilityData?.facilities}
          tenantDetailView={tenantDetailView as boolean}
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
      {confirmationFlag && (
        <ConfirmationMessage
          {...{ closeConfirmation, confirmationText }}
          confirmedAction={actionSubmit}
        />
      )}
    </>
  );
};
