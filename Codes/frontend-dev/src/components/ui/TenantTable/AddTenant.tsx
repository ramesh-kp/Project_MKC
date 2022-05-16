/* eslint-disable no-console */
import { FC, useState } from 'react';
import Image from 'next/image';
import { FieldError, UseFormRegister, UseFormSetValue } from 'react-hook-form';
import Select from 'react-select';
import { useQueryClient } from 'react-query';
import AddIcon from 'assets/add-icon.png';
import CheckIcon from 'assets/tick.png';
import CloseIcon from 'assets/remove.png';
import { ValidationMessage } from '../CommonPage/ValidationMessage';
import {
  CreateFacilityMutation,
  FacilitiesQuery,
  useCreateFacilityMutation,
  UserRoleType,
  UserStatusType,
  useUsersQuery,
} from '@api/graphql';
import graphQLClient from '@lib/useGQLQuery';
import { globalVariables, orderAsc, TenantFormInputs } from '@lib/common';
import { ApiLoader } from '../CommonPage/ApiLoader';
import { ErrorPage } from '../CommonPage/ErrorPage/ErrorPage';
import { FacilityType } from '@components/pages/Tenants/Tenant';

type errorType = {
  name?: FieldError;
  location?: FieldError;
  owner?: FieldError;
  parent?: FieldError;
  description?: FieldError;
  facilities?: FieldError;
};

export interface AddUserProps {
  register: UseFormRegister<TenantFormInputs>;
  errors: errorType;
  submitTenant: () => void;
  setValue: UseFormSetValue<TenantFormInputs>;
  facilityData: FacilitiesQuery['facilities'];
  facilityArray: FacilityType[];
  cancelPopup: () => void;
  editRowId: string;
  tenantDetailView: boolean;
}

export const AddTenantForm: FC<AddUserProps> = ({
  register,
  errors,
  submitTenant,
  setValue,
  facilityData,
  facilityArray,
  cancelPopup,
  editRowId,
  tenantDetailView,
}) => {
  const [loader, setLoader] = useState<boolean>(false);
  const [addFacility, setAddFacility] = useState<boolean>(false);
  const [newFacility, setNewFacility] = useState<string>('');
  const [facilityValidationMessage, setFacilityValidationMessage] =
    useState<string>('');
  const queryClient = useQueryClient();

  const createFacility = useCreateFacilityMutation<CreateFacilityMutation>(
    graphQLClient(),
  );

  const conditionForEdit = {
    OR: [
      {
        tenant: null,
      },
      {
        tenant: {
          id: {
            equals: editRowId,
          },
        },
      },
    ],
    status: {
      equals: UserStatusType.Active,
    },
    role: {
      equals: UserRoleType.Tenant,
    },
  };
  const conditionForAdd = {
    tenant: null,
    role: {
      equals: UserRoleType.Tenant,
    },
    status: {
      equals: UserStatusType.Active,
    },
  };

  const whereConditionForUser =
    editRowId === '' ? conditionForAdd : conditionForEdit;

  const userVariables = {
    skip: 0,
    usersCountWhere2: whereConditionForUser,
    where: whereConditionForUser,
    orderBy: orderAsc,
  };

  const {
    data: users,
    isLoading,
    isError,
  } = useUsersQuery(graphQLClient(), userVariables);

  const options = facilityData?.map(facility => {
    return {
      value: facility.id,
      label: facility.name,
    };
  });
  const defaultValueForFacility = options?.filter(option =>
    facilityArray.find(({ value }) => option.value === value),
  );
  const isButtonDisabled =
    newFacility === '' || facilityValidationMessage !== '';

  const handleFacilityName = (facilityName: string) => {
    setNewFacility(facilityName);
    const nameArray = options?.map(option => option.label?.toLowerCase());
    const isValidName = nameArray?.includes(facilityName.toLocaleLowerCase());
    const message = isValidName ? 'Facility name is already taken' : '';
    setFacilityValidationMessage(message);
  };

  const submitData = async () => {
    try {
      setLoader(true);
      const variable = {
        data: {
          name: newFacility,
        },
      };
      await createFacility.mutateAsync(variable);
      queryClient.invalidateQueries();

      setNewFacility('');
      setAddFacility(false);
    } catch (e) {
      console.error(e);
    } finally {
      setLoader(false);
    }
  };

  if (isLoading || loader) return <ApiLoader />;
  if (isError) return <ErrorPage />;
  return (
    <>
      <div className="fixed left-0 top-0 z-40 w-full h-full overflow-y-auto overflow-hidden">
        <div
          className="max-w-3xl z-50 my-7 px-5 mx-auto relative flex items-center"
          style={{ minHeight: 'calc(100% - 3.5rem)' }}
        >
          <div className="p-7 bg-white rounded-md h-full w-full">
            <h2 className="inline-block text-2xl mb-4 font-semibold">
              {tenantDetailView ? 'Add Sub-Tenant' : 'Add Tenant'}
            </h2>
            <input
              type="text"
              className="w-full py-2 mb-4 border-0 border-b-2 focus-visible:outline-0"
              placeholder="Tenant Name"
              maxLength={30}
              {...register('name')}
              tabIndex={1}
            />
            <ValidationMessage message={errors.name?.message as string} />
            <div className="sm:block md:flex">
              <div className="md:w-1/2 md:mr-4 sm:mr-0 sm:w-full">
                <input
                  type="text"
                  className="w-full py-2 mb-4 border-0 border-b-2 focus-visible:outline-0 h-11"
                  placeholder="Tenant Location"
                  maxLength={30}
                  {...register('location')}
                  tabIndex={2}
                />
                <ValidationMessage
                  message={errors.location?.message as string}
                />
              </div>
              <div className="md:w-1/2 md:ml-4 sm:ml-0 sm:w-full">
                <select
                  className="w-full py-2 mb-4 border-0 border-b-2 bg-white focus-visible:outline-0 h-11"
                  {...register('owner')}
                  tabIndex={3}
                >
                  <option>{globalVariables.user}</option>

                  {users?.users?.map(user => (
                    <option key={user.id} id={user.id} value={user.id}>
                      {user.name}
                    </option>
                  ))}
                </select>
                <ValidationMessage message={errors.owner?.message as string} />
              </div>
            </div>
            <textarea
              className="w-full py-2 mb-4 border-0 border-b-2 focus-visible:outline-0 "
              placeholder="Description"
              maxLength={200}
              tabIndex={4}
              {...register('description')}
            />
            <ValidationMessage
              message={errors.description?.message as string}
            />
            <div className="clear-both" />

            <h2 className="inline-block text-2xl mb-4 font-semibold">
              Facilities
            </h2>
            <div className="sm:block md:flex">
              <div className="md:w-1/2 md:mr-4 sm:mr-0 sm:w-full">
                <Select
                  placeholder="Select Facilities..."
                  isMulti
                  name="facilities"
                  options={options}
                  className="basic-multi-select"
                  classNamePrefix="select"
                  onChange={e => setValue('facilities', e)}
                  defaultValue={defaultValueForFacility}
                  tabIndex={5}
                />
                <ValidationMessage
                  message={errors.facilities?.message as string}
                />
              </div>
              <div className="md:w-1/2 md:ml-4 sm:ml-0 sm:w-full">
                <button
                  type="button"
                  className={
                    addFacility
                      ? 'mb-5 transition-all border-2 w-auto inline-block border-slate-400 px-3 py-2 rounded-md text-black text-base font-semibold ml-0 bg-slate-200 lg:my-0  hover:bg-grey-700'
                      : 'mb-5 transition-all border-2 w-auto inline-block border-sky-600 px-3 py-2 rounded-md text-white text-base font-semibold ml-0 bg-sky-600 lg:my-0  hover:bg-sky-700'
                  }
                  onClick={() => setAddFacility(true)}
                  disabled={addFacility}
                  tabIndex={6}
                >
                  Add New Facilities{' '}
                  <Image
                    src={AddIcon}
                    className="inline-block ml-3"
                    alt="Add"
                  />
                </button>
              </div>
            </div>
            {addFacility && (
              <div className="relative">
                <input
                  type="text"
                  className="w-full py-2 mb-4 border-0 border-b-2 focus-visible:outline-0"
                  placeholder="Type new facility"
                  required
                  maxLength={60}
                  onChange={e => handleFacilityName(e.target.value)}
                />
                <ValidationMessage message={facilityValidationMessage} />
                <div className="absolute right-0 bottom-5 flex">
                  <button
                    type="button"
                    className="mr-2 w-10 h-10 p-3 pt-2 rounded-full text-center"
                    onClick={() => submitData()}
                    disabled={isButtonDisabled}
                  >
                    <div className="w-9 hover:bg-sky-200">
                      <Image
                        src={CheckIcon}
                        alt="Close"
                        className="inline-block"
                      />
                    </div>
                  </button>
                  <button
                    type="button"
                    className="mr-2 w-10 h-10 p-3 pt-2 rounded-full text-center"
                    onClick={() => setAddFacility(false)}
                  >
                    <div className="w-9 hover:bg-sky-200">
                      <Image
                        src={CloseIcon}
                        alt="check"
                        className="inline-block "
                      />
                    </div>
                  </button>
                </div>
              </div>
            )}
            <div className="w-full mt-10 mb-2 text-right">
              <button
                type="button"
                className="transition-all border-2 w-auto inline-block border-sky-600 px-8 py-2 rounded-lg text-neutral-600 text-base font-semibold mr-0 mb-4 lg:my-0 mr-4 text-center"
                onClick={() => cancelPopup()}
                tabIndex={8}
              >
                Cancel
              </button>
              <button
                type="button"
                className="transition-all border-2 w-auto inline-block border-sky-600 px-8 py-2 rounded-lg text-white text-base font-semibold ml-0 bg-sky-600 lg:my-0 text-center hover:bg-sky-700"
                onClick={() => submitTenant()}
                tabIndex={7}
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
