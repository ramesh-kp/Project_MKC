import { FC, useState } from 'react';
import Image from 'next/image';
import { useRouter } from 'next/router';
import moment from 'moment';
import BackIcon from 'assets/back_icon.png';
import UserIcon from 'assets/user-icon.png';
import EditIcon from 'assets/edit-icon.png';
import {
  TenantDetailsQuery,
  UserRoleType,
  useTenantDetailsByDateQuery,
} from '@api/graphql';
import { useSession } from '@lib/useSession';
import { tenantType, dateBeforeOneWeek, todayDate } from '@lib/common';
import { BarChart } from '../Charts/BarChart';
import { DateRangePicker } from '../CommonPage/DateRangePicker';
import { ResourceConsumption } from '../CommonPage/ResourceConsumption';
import graphQLClient from '@lib/useGQLQuery';

interface TenantDetailProps {
  tenantDetails?: TenantDetailsQuery['tenant'];
  editData?: (tenantData: tenantType) => void;
}

export const TenantDetailsView: FC<TenantDetailProps> = ({
  tenantDetails,
  editData,
}) => {
  const router = useRouter();
  const { state } = useSession();
  const { currentUser, dateRange } = state;
  const [fromDate, setFromDate] = useState<string>(dateBeforeOneWeek);
  const [toDate, setToDate] = useState<string>(todayDate);
  const differenceInTime =
    new Date(toDate).getTime() - new Date(fromDate).getTime();
  const differenceInDays = differenceInTime / (1000 * 3600 * 24);

  const queryVariables = {
    where: {
      id: tenantDetails?.id,
    },
    from: fromDate,
    to: toDate,
    deviceReadSumFrom2: fromDate,
    deviceReadSumTo2: toDate,
  };

  const { data: tenantData } = useTenantDetailsByDateQuery(
    graphQLClient(),
    queryVariables,
  );

  const facilities: string[] = [];

  tenantData?.tenant?.facilities?.forEach(facility =>
    facilities.push(facility.name as string),
  );

  const finalFacility = [...new Set(facilities)];

  const barChartData: { [key: string]: string | number } = {};

  tenantData?.tenant?.facilities?.forEach(facility => {
    if (facility.name) {
      barChartData[facility.name] = facility.deviceReadSum as number;
    }
  });

  barChartData['tenant'] = tenantData?.tenant?.name as string;

  const submitDates = () => {
    setFromDate(moment(dateRange.from).format());
    setToDate(moment(dateRange.to).format());
  };

  return (
    <>
      <div className="p-6 bg-white rounded-lg mb-6">
        {currentUser.role === UserRoleType.Admin && (
          <button
            type="button"
            className="text-black hover:text-sky-500"
            onClick={() => router.back()}
          >
            <Image
              src={BackIcon}
              className="inline-block mr-2 w-4"
              alt="Back Icon"
            />{' '}
            Back
          </button>
        )}

        <div className="clear-both" />
        <div className="mt-5 lg:flex sm:block">
          <div className="flex w-full">
            <div className="rounded-full bg-zinc-200 w-16 h-16 text-center overflow-hidden">
              <Image
                src={UserIcon}
                alt="User icon"
                className="inline-block max-w-full"
              />
            </div>
            <div className="ml-5">
              <h2 className="mb-2 font-bold text-xl">
                {tenantDetails?.name}{' '}
                {currentUser.role === UserRoleType.Admin && (
                  <button
                    type="button"
                    onClick={() =>
                      editData && editData(tenantDetails as tenantType)
                    }
                  >
                    <Image
                      src={EditIcon}
                      alt="Edit"
                      className="inline-block ml-2"
                    />
                  </button>
                )}
              </h2>
              <p>
                {tenantDetails?.owners?.length === 0
                  ? 'Nil'
                  : tenantDetails?.owners?.[0].name}
                <br />
                {tenantDetails?.location}
              </p>
            </div>
          </div>

          <div className="flex bg-white rounded-md mb-5 single-datepicker-outer h-11">
            <div className="float-left">
              <DateRangePicker {...{ submitDates }} />
            </div>
          </div>
        </div>
      </div>

      <div className="grid-row">
        {tenantData?.tenant?.resources?.map((resource, index) => (
          <div className="grid-outer" key={index}>
            <div key={index} className="w-full rounded-lg bg-white p-4">
              <h2 className="inline-block text-l font-semibold mb-4 mt-0 float-left">
                {resource.name}
              </h2>
              <div className="clear-both" />
              <ResourceConsumption {...{ resource, differenceInDays }} />
              <div className="clear-both" />
            </div>
          </div>
        ))}
      </div>

      <div className="p-6 bg-white rounded-lg">
        <h2 className="inline-block text-xl font-semibold mb-4 mt-1 float-left">
          Facilities
        </h2>
        <div className="clear-both" />
        <div className="pb-4 h-128">
          <BarChart
            barchartData={[barChartData]}
            barchartKeys={finalFacility}
            power={false}
          />
        </div>
      </div>

      <div className="clear-both" />
    </>
  );
};
