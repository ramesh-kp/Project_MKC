import { useState } from 'react';
import moment from 'moment';
import { TenantList } from '@components/pages/Tenants/Tenant';
import { DateRangePicker } from '../CommonPage/DateRangePicker';
import { ResourceConsumption } from '../CommonPage/ResourceConsumption';
import {
  ResourceResourceCategoryType,
  useResourcesDataByDateQuery,
  useTenantsByDateQuery,
} from '@api/graphql';
import graphQLClient from '@lib/useGQLQuery';
import { BarChart } from '../Charts/BarChart';
import { ApiLoader } from '../CommonPage/ApiLoader';
import { useSession } from '@lib/useSession';

export const WaterDashboard = () => {
  const { state } = useSession();
  const { dateRange } = state;
  const [fromDate, setFromDate] = useState<string>(
    moment(dateRange.from).format(),
  );
  const [toDate, setToDate] = useState<string>(moment(dateRange.to).format());

  const { data: resources, isLoading: resourceLoader } =
    useResourcesDataByDateQuery(graphQLClient(), {
      from: fromDate,
      to: toDate,
      where: {
        tenant: null,
        resourceCategory: {
          equals: ResourceResourceCategoryType.Water,
        },
      },
    });

  const differenceInTime =
    new Date(toDate).getTime() - new Date(fromDate).getTime();
  const differenceInDays = differenceInTime / (1000 * 3600 * 24);

  const { data: tenantData, isLoading: tenantLoader } = useTenantsByDateQuery(
    graphQLClient(),
    {
      where: {
        parent: null,
      },
      from: fromDate,
      to: toDate,
      deviceReadSumFrom2: fromDate,
      deviceReadSumTo2: toDate,
    },
  );
  const facilities: string[] = [];
  tenantData?.tenants?.forEach(tenant =>
    tenant.facilities?.forEach(facility =>
      facilities.push(facility.name as string),
    ),
  );
  const finalFacility = [...new Set(facilities)];

  const result =
    tenantData?.tenants &&
    tenantData?.tenants?.map(tenant => {
      const barChartData: { [key: string]: string | number } = {};

      tenant.facilities?.forEach(facility => {
        if (facility.name) {
          barChartData[facility.name] = facility.deviceReadSum as number;
        }
      });

      barChartData['tenant'] = tenant.name as string;

      finalFacility.forEach(i => (barChartData[i] = barChartData[i] ?? 0));

      return barChartData;
    });

  const barChartDetails = result
    ? (result as {
        [key: string]: string | number;
      }[])
    : [];

  const submitDates = () => {
    setFromDate(moment(dateRange.from).format());
    setToDate(moment(dateRange.to).format());
  };

  if (resourceLoader || tenantLoader) return <ApiLoader />;

  return (
    <>
      <div className="w-full mr-b-30">
        <div className="float-right bg-white rounded-md mb-5 single-datepicker-outer">
          <div className="float-left">
            <DateRangePicker {...{ submitDates }} />
          </div>
        </div>
        <div className="clear-both" />
      </div>
      <div className="clear-both" />
      <div className="grid-row">
        {resources?.resources?.map((resource, index) => (
          <div className="grid-outer" key={index}>
            <div className="w-full rounded-lg bg-white p-4">
              <h2 className="inline-block text-xl font-semibold mb-4 mt-0 float-left">
                {resource.name}
              </h2>

              <div className="clear-both" />
              <ResourceConsumption {...{ resource, differenceInDays }} />
              <div className="clear-both" />
            </div>
          </div>
        ))}
      </div>
      <div className="clear-both" />
      <div className="w-full rounded-lg bg-white p-6 mb-6 sm:mx-0">
        <h2 className="inline-block text-xl font-semibold mb-4 mt-1 float-left">
          Facilities
        </h2>
        <div className="pb-10 h-128">
          <BarChart
            barchartData={barChartDetails}
            barchartKeys={finalFacility}
            power={false}
          />
        </div>
      </div>
      <TenantList home />
      <div className="clear-both" />
    </>
  );
};
