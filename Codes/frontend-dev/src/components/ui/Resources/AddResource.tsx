import { FC } from 'react';
import { FieldError, UseFormRegister } from 'react-hook-form';
import { ResourceResourceCategoryType, ResourceUnitType } from '@api/graphql';
import { ValidationMessage } from '../CommonPage/ValidationMessage';
import { resourceType } from '@components/pages/Resources';
import { globalVariables } from '@lib/common';

type errorType = {
  name?: FieldError;
  resourceCategory?: FieldError;
  capacity?: FieldError;
  unit?: FieldError;
};

interface AddSensorProps {
  handleClose: () => void;
  register: UseFormRegister<resourceType>;
  errors: errorType;
  submitForm: () => void;
}

export const AddResource: FC<AddSensorProps> = ({
  handleClose,
  register,
  errors,
  submitForm,
}) => {
  const resourceTypes = [
    ResourceResourceCategoryType.Water,
    ResourceResourceCategoryType.Power,
    ResourceResourceCategoryType.SewageTreatment,
  ];

  const units = [ResourceUnitType.Kw, ResourceUnitType.Ltr];

  return (
    <>
      <div className="fixed left-0 top-0 z-40 w-full h-full overflow-y-auto overflow-hidden">
        <div
          className="max-w-3xl z-50 my-7 px-5 mx-auto relative flex items-center"
          style={{ minHeight: 'calc(100% - 3.5rem)' }}
        >
          <div className="p-7 bg-white rounded-md h-full w-full">
            <h2 className="inline-block text-2xl mb-4 font-semibold">
              Add Resource
            </h2>

            <div className="sm:block md:flex">
              <div className="md:w-1/2 md:mr-4 sm:mr-0 sm:w-full">
                <input
                  type="text"
                  maxLength={15}
                  tabIndex={1}
                  className="w-full py-2 mb-4 border-0 border-b-2 focus-visible:outline-0 h-11"
                  placeholder="Resource Name"
                  {...register('name')}
                />
                <ValidationMessage message={errors.name?.message as string} />
              </div>

              <div className="md:w-1/2 md:mr-4 sm:mr-0 sm:w-full">
                <select
                  tabIndex={3}
                  className="w-full py-2 mb-4 border-0 border-b-2 bg-white focus-visible:outline-0 h-11"
                  {...register('resourceCategory')}
                >
                  <option>{globalVariables.categoryType}</option>
                  {resourceTypes?.map(resourceType => (
                    <option key={resourceType} value={resourceType}>
                      {resourceType}
                    </option>
                  ))}
                </select>
              </div>
              <ValidationMessage
                message={errors.resourceCategory?.message as string}
              />
            </div>

            <div className="sm:block md:flex">
              <div className="md:w-1/2 md:mr-4 sm:mr-0 sm:w-full">
                <input
                  type="text"
                  maxLength={15}
                  tabIndex={1}
                  className="w-full py-2 mb-4 border-0 border-b-2 focus-visible:outline-0 h-11"
                  placeholder="Capacity"
                  {...register('capacity')}
                />
                <ValidationMessage
                  message={errors.capacity?.message as string}
                />
              </div>

              <div className="md:w-1/2 md:mr-4 sm:mr-0 sm:w-full">
                <select
                  tabIndex={3}
                  className="w-full py-2 mb-4 border-0 border-b-2 bg-white focus-visible:outline-0 h-11"
                  {...register('unit')}
                >
                  <option>{'Select Unit'}</option>
                  {units?.map(unit => (
                    <option key={unit} value={unit}>
                      {unit}
                    </option>
                  ))}
                </select>
                <ValidationMessage message={errors.unit?.message as string} />
              </div>
            </div>
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
