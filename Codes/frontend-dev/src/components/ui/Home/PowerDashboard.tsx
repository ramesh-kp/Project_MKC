import moment from 'moment';
import {
  ResourceResourceCategoryType,
  useTenantsDataByCategoryQuery,
} from '@api/graphql';
import { TenantList } from '@components/pages/Tenants/Tenant';
import graphQLClient from '@lib/useGQLQuery';
import { BarChart } from '../Charts/BarChart';
import { ApiLoader } from '../CommonPage/ApiLoader';
import { BarDatum } from '@nivo/bar';

const fromDate = moment().subtract(30, 'days').endOf('day').format();
const toDate = moment().format();

interface barchartType {
  tenant?: string;
  consumption?: number;
  capacity?: number;
}

export const PowerDashboard = () => {
  const queryVariables = {
    where: {
      resourceCategory: {
        equals: ResourceResourceCategoryType.Power,
      },
    },
    from: fromDate,
    to: toDate,
    tenantsWhere2: {
      parent: null,
    },
  };

  const { data: tenants, isLoading } = useTenantsDataByCategoryQuery(
    graphQLClient(),
    queryVariables,
  );

  const barChartKeys = ['consumption', 'capacity'];

  const barChartData = tenants?.tenants?.reduce(
    (acc, item) => [
      ...acc,
      {
        tenant: item.name,
        consumption: item?.resources && item.resources[0]?.deviceReadSum,
        capacity: item?.resources && item.resources[0]?.capacity,
      } as barchartType,
    ],
    [] as barchartType[],
  );

  const tenantBarChartData = barChartData ?? [];

  if (isLoading) return <ApiLoader />;

  return (
    <>
      <div className="lg:flex sm:block">
        <div className="w-full rounded-lg bg-white p-6 mb-6 sm:mx-0 ">
          <h2 className="inline-block text-xl font-semibold mb-4 mt-1 float-left">
            Power Consumption{' '}
          </h2>
          <div className="clear-both" />
          <div className="pb-4 h-128">
            <BarChart
              barchartData={tenantBarChartData as BarDatum[]}
              barchartKeys={barChartKeys}
              power
            />
          </div>
          <div className="clear-both" />
        </div>
      </div>
      <div className="clear-both" />
      <TenantList home />
      <div className="clear-both" />
    </>
  );
};
