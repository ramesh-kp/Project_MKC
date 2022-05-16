import { FC } from 'react';
import Image from 'next/image';
import { useRouter } from 'next/router';
import Dot from 'assets/dot.png';
import {
  ResourceResourceCategoryType,
  TenantsQuery,
  TenantStatusType,
  UserRoleType,
} from '@api/graphql';
import { tenantType } from '@lib/common';
import { useSession } from '@lib/useSession';

const headersForParentTenant = [
  'Tenant Name',
  'Tenant User Name',
  'Location',
  'Water Source',
  'Consumed Power',
];

const headersForSubTenant = ['Tenant Name', 'Tenant User Name', 'Location'];

export interface TenantListProps {
  tenantList?: TenantsQuery['tenants'];
  editData?: (data: tenantType) => void;
  actionConfirm?: (action: string, tenantId: string) => void;
  tenantDetailView: boolean;
}

export const TenantListView: FC<TenantListProps> = ({
  tenantList,
  editData,
  actionConfirm,
  tenantDetailView,
}) => {
  const router = useRouter();
  const { state } = useSession();
  const { currentUser } = state;

  const optionalHeader = tenantDetailView
    ? [...headersForSubTenant, 'Action']
    : [...headersForParentTenant, 'Action'];

  const tenantDashboardHeaders = tenantDetailView
    ? headersForSubTenant
    : headersForParentTenant;

  const columnHeaders =
    currentUser.role === UserRoleType.Admin
      ? optionalHeader
      : tenantDashboardHeaders;

  const actionSubmit = (
    status: TenantStatusType | null | undefined,
    deviceId: string,
  ) => {
    actionConfirm &&
      actionConfirm(
        status === TenantStatusType.Active ? 'Deactivate' : 'Activate',
        deviceId,
      );
  };

  const powerConsumption = (tenantData: tenantType) => {
    let consumption: number | undefined = 0;
    consumption = tenantData?.resources?.find(
      resource =>
        resource.resourceCategory === ResourceResourceCategoryType.Power,
    )?.deviceReadSum;
    return consumption ?? '-';
  };

  const waterSources = (tenantData: tenantType) => {
    let sources: string = '';
    const waterResources = tenantData?.resources?.filter(
      resource =>
        resource.resourceCategory === ResourceResourceCategoryType.Water,
    );
    sources = waterResources.map(resource => resource.name).join(',');
    return sources;
  };

  const tableRowStyle = (status: TenantStatusType) => {
    let rowStyle: string = '';
    status === TenantStatusType.Active
      ? (rowStyle = 'border-b border-gray-300')
      : (rowStyle = 'border-b border-gray-300 bg-stone-200');
    return rowStyle;
  };

  return (
    <>
      <div className="border-b border-gray-300">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-white">
            <tr className="border-b border-gray-300">
              {columnHeaders.map((column: string) => (
                <th
                  key={column}
                  scope="col"
                  className="py-3 text-left text-md font-semibold text-gray-700 tracking-wider"
                >
                  {column}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200 ">
            {tenantList?.map(tenant => (
              <tr
                key={tenant.id}
                className={tableRowStyle(tenant.status as TenantStatusType)}
              >
                <td
                  className="py-4 whitespace-nowrap hover:text-sky-500 cursor-pointer"
                  onClick={() => router.push(`/tenant/${tenant.id}`)}
                >
                  {tenant.name}
                </td>
                <td className="py-4 whitespace-nowrap">
                  {tenant.owners && tenant.owners[0]?.name}
                </td>
                <td className="py-4 whitespace-nowrap">{tenant.location}</td>
                {!tenantDetailView && (
                  <>
                    <td className="py-4 whitespace-nowrap">
                      {waterSources(tenant as tenantType)}
                    </td>
                    <td className="py-4 whitespace-nowrap">
                      {powerConsumption(tenant as tenantType)}
                    </td>
                  </>
                )}
                {currentUser.role === UserRoleType.Admin && (
                  <td className="py-2 whitespace-nowrap">
                    <div className="dropdown dropdown-end">
                      <label
                        tabIndex={0}
                        className="mx-1 min-h-0 h-10 btn bg-white border-0 hover:bg-slate-100"
                      >
                        <Image src={Dot} alt="dot" />
                      </label>
                      <ul
                        tabIndex={0}
                        className="p-2 shadow menu dropdown-content bg-base-100 rounded-lg w-34"
                      >
                        <li>
                          <label
                            className="py-1 rounded-none"
                            onClick={() =>
                              editData && editData(tenant as tenantType)
                            }
                          >
                            Edit
                          </label>
                        </li>
                        <li>
                          <label
                            htmlFor="my-modal"
                            className="py-1 rounded-none modal-button"
                            onClick={() =>
                              actionSubmit(tenant.status, tenant.id)
                            }
                          >
                            {tenant.status === TenantStatusType.Active
                              ? 'Deactivate'
                              : 'Activate'}
                          </label>
                        </li>
                      </ul>
                    </div>
                  </td>
                )}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="clear-both" />
    </>
  );
};
