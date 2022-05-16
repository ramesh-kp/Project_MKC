import { useState } from 'react';
import { useRouter } from 'next/router';
import { useDevicesQuery, useTenantDetailsQuery } from '@api/graphql';
import { TenantDetailsView } from '@components/ui/TenantTable/TenantDetails';
import graphQLClient from '@lib/useGQLQuery';
import { ApiLoader } from '@components/ui/CommonPage/ApiLoader';
import { ErrorPage } from '@components/ui/CommonPage/ErrorPage/ErrorPage';
import { TenantList } from '../Tenant';
import { useSession } from '@lib/useSession';
import { globalVariables, selectType } from '@lib/common';
import { SensorListPage } from '@components/pages/Sensors';
import { Resources } from '@components/pages/Resources';

export const TenantDashboard = () => {
  const router = useRouter();
  const { state } = useSession();
  const { currentUser } = state;
  const [tab, setTab] = useState<string>(globalVariables.tenant);
  const tabs = [
    { value: 'tenant', label: 'Sub-Tenants' },
    { value: 'sensor', label: 'Sensors' },
    { value: 'resource', label: 'Resources' },
  ];

  const variables = {
    where: {
      id: currentUser.tenant?.id,
    },
  };

  const whereCondition = {
    tenant: {
      id: {
        equals: currentUser.tenant?.id,
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

  const tabStyle = (tabLabel: selectType) => {
    let classStyle: string = '';
    tab === tabLabel.value
      ? (classStyle = 'tab tab-lifted text-xl font-medium tab-active')
      : (classStyle = 'tab tab-lifted text-sky-600 text-xl font-medium');

    return classStyle;
  };

  if (currentUser.role === undefined) router.push('/login');
  if (isLoading) return <ApiLoader />;
  if (isError) return <ErrorPage />;

  return (
    <>
      <TenantDetailsView tenantDetails={tenantDetails?.tenant} />
      <div className="p-6 bg-white rounded-lg mt-6 mb-10">
        <div className="tabs h-12 border-b-2 border-sky-600 tab-outer">
          {tabs.map(tabOption => (
            <label
              key={tabOption.value}
              className={tabStyle(tabOption)}
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
          <Resources tenantId={currentUser.tenant?.id as string} />
        )}
      </div>
    </>
  );
};
