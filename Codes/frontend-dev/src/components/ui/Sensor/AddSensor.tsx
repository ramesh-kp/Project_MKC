import { FC, useState } from 'react';
import {
  Control,
  Controller,
  FieldError,
  UseFormRegister,
} from 'react-hook-form';
import {
  DeviceTypesQuery,
  FacilitiesQuery,
  ResourceResourceCategoryType,
  useResourcesQuery,
} from '@api/graphql';
import { DeviceType, globalVariables, SensorFormType } from '@lib/common';

import { ValidationMessage } from '../CommonPage/ValidationMessage';
import graphQLClient from '@lib/useGQLQuery';

type errorType = {
  deviceName?: FieldError;
  deviceId?: FieldError;
  edgeDeviceId?: FieldError;
  portNumber?: FieldError;
  parent?: FieldError;
  description?: FieldError;
};
interface AddSensorProps {
  handleClose: () => void;
  register: UseFormRegister<SensorFormType>;
  errors: errorType;
  submitForm: () => void;
  facilities: FacilitiesQuery['facilities'];
  deviceTypes: DeviceTypesQuery['deviceTypes'];
  tenantDetailView: boolean;
  control: Control<SensorFormType, object>;
  editData?: DeviceType;
  tenantId?: string;
}

export const AddSensor: FC<AddSensorProps> = ({
  handleClose,
  register,
  errors,
  submitForm,
  facilities,
  deviceTypes,
  tenantDetailView,
  control,
  editData,
  tenantId,
}) => {
  const resourceTypes = [
    ResourceResourceCategoryType.Water,
    ResourceResourceCategoryType.Power,
    ResourceResourceCategoryType.SewageTreatment,
  ];

  const [resourceType, setResourcesType] =
    useState<ResourceResourceCategoryType>(
      editData
        ? (editData.resource?.resourceCategory as ResourceResourceCategoryType)
        : ResourceResourceCategoryType.Water,
    );

  const commonSensorCondition = {
    resourceCategory: {
      equals: resourceType,
    },
    tenant: null,
  };
  const sensorsForTenant = {
    resourceCategory: {
      equals: resourceType,
    },
    tenant: {
      id: {
        equals: tenantId,
      },
    },
  };
  const whereCondition = tenantId ? sensorsForTenant : commonSensorCondition;

  const { data: resources } = useResourcesQuery(graphQLClient(), {
    where: whereCondition,
    resourcesCountWhere2: whereCondition,
    take: null,
    skip: 0,
  });

  return (
    <>
      <div className="fixed left-0 top-0 z-40 w-full h-full overflow-y-auto overflow-hidden">
        <div
          className="max-w-3xl z-50 my-7 px-5 mx-auto relative flex items-center"
          style={{ minHeight: 'calc(100% - 3.5rem)' }}
        >
          <div className="p-7 bg-white rounded-md h-full w-full">
            <h2 className="inline-block text-2xl mb-4 font-semibold">
              Add Sensor
            </h2>

            <div className="sm:block md:flex">
              <div className="md:w-1/2 md:mr-4 sm:mr-0 sm:w-full">
                <input
                  type="text"
                  maxLength={15}
                  tabIndex={1}
                  className="w-full py-2 mb-4 border-0 border-b-2 focus-visible:outline-0 h-11"
                  placeholder="Sensor Name"
                  {...register('deviceName')}
                />
                <ValidationMessage
                  message={errors.deviceName?.message as string}
                />
              </div>
              <div className="md:w-1/2 md:mr-4 sm:mr-0 sm:w-full">
                <input
                  type="text"
                  maxLength={15}
                  tabIndex={1}
                  className="w-full py-2 mb-4 border-0 border-b-2 focus-visible:outline-0 h-11"
                  placeholder="Sensor Device ID"
                  {...register('deviceId')}
                />
                <ValidationMessage
                  message={errors.deviceId?.message as string}
                />
              </div>
            </div>

            <div className="sm:block md:flex">
              <div className="md:w-1/2 md:mr-4 sm:mr-0 sm:w-full">
                <input
                  type="text"
                  maxLength={15}
                  tabIndex={2}
                  className="w-full py-2 mb-4 border-0 border-b-2 focus-visible:outline-0 h-11"
                  placeholder="Edge Device Name or ID"
                  {...register('edgeDeviceId')}
                />
                <ValidationMessage
                  message={errors.edgeDeviceId?.message as string}
                />
              </div>
              <div className="md:w-1/2 md:mr-4 sm:mr-0 sm:w-full">
                <select
                  tabIndex={3}
                  className="w-full py-2 mb-4 border-0 border-b-2 bg-white focus-visible:outline-0 h-11"
                  {...register('sensorType')}
                >
                  <option>{globalVariables.sensorType}</option>
                  {deviceTypes?.map(deviceType => (
                    <option key={deviceType.id} value={deviceType.id}>
                      {deviceType.name}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <div className="sm:block md:flex">
              <div className="md:w-1/2 md:mr-4 sm:mr-0 sm:w-full">
                <input
                  type="text"
                  maxLength={20}
                  tabIndex={4}
                  className="w-full py-2 mb-4 border-0 border-b-2 focus-visible:outline-0 h-11"
                  placeholder="Edge Device Port Number"
                  {...register('portNumber')}
                />
                <ValidationMessage
                  message={errors.portNumber?.message as string}
                />
              </div>
              <div className="md:w-1/2 md:mr-4 sm:mr-0 sm:w-full">
                <Controller
                  name="resourceType"
                  control={control}
                  render={({ field }) => (
                    <select
                      tabIndex={5}
                      className="w-full py-2 mb-4 border-0 border-b-2 bg-white focus-visible:outline-0 h-11"
                      {...field}
                      onChange={e => {
                        setResourcesType(
                          e.target.value as ResourceResourceCategoryType,
                        );
                        field.onChange(e);
                      }}
                    >
                      <option>Resource Type</option>
                      {resourceTypes?.map(type => (
                        <option key={type} value={type}>
                          {type}
                        </option>
                      ))}
                    </select>
                  )}
                />
              </div>
            </div>

            <div className="sm:block md:flex">
              <div className="md:mr-4 sm:mr-0 sm:w-full">
                <select
                  tabIndex={6}
                  className="w-full py-2 mb-4 border-0 border-b-2 bg-white focus-visible:outline-0 h-11"
                  {...register('resource')}
                >
                  <option>{globalVariables.resource}</option>
                  {resources?.resources?.map(resource => (
                    <option key={resource.id} value={resource.id}>
                      {resource.name}
                    </option>
                  ))}
                </select>
              </div>
            </div>
            {tenantDetailView && (
              <div className="sm:block md:flex">
                <div className="md:w-1/2 md:mr-4 sm:mr-0 sm:w-full">
                  <select
                    tabIndex={7}
                    className="w-full py-2 mb-4 border-0 border-b-2 bg-white focus-visible:outline-0 h-11"
                    {...register('facility')}
                  >
                    <option>{globalVariables.tenantFacility}</option>
                    {facilities?.map(facility => (
                      <option key={facility.id} value={facility.id}>
                        {facility.name}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
            )}

            <textarea
              tabIndex={7}
              className="w-full py-2 mb-4 border-0 border-b-2 focus-visible:outline-0 h-24"
              placeholder="Description"
              {...register('description')}
            />
            <ValidationMessage
              message={errors.description?.message as string}
            />
            <div className="clear-both" />

            <div className="w-full mt-10 mb-2 text-right">
              <button
                type="button"
                tabIndex={9}
                className="transition-all border-2 w-auto inline-block border-sky-600 px-8 py-2 rounded-lg text-neutral-600 text-base font-semibold mr-0 mb-4 lg:my-0 mr-4 text-center"
                onClick={() => handleClose()}
              >
                Cancel
              </button>
              <button
                type="button"
                tabIndex={8}
                className="transition-all border-2 w-auto inline-block border-sky-600 px-8 py-2 rounded-lg text-white text-base font-semibold ml-0 bg-sky-600 lg:my-0  text-center hover:bg-sky-700"
                onClick={() => submitForm()}
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
