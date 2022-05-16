import { Dispatch, FC, SetStateAction } from 'react';
import Image from 'next/image';
import Dot from 'assets/dot.png';
import { ResourcesQuery, ResourceStatusType, UserRoleType } from '@api/graphql';
import { NoRecords } from '../CommonPage/NoRecords/NoRecords';
import { useSession } from '@lib/useSession';
import { resourceType } from '@components/pages/Resources';

interface ResourceListProps {
  setAddResource: Dispatch<SetStateAction<boolean>>;
  resources: ResourcesQuery['resources'];
  handleEdit: (resource: resourceType) => void;
  actionConfirm?: (action: string, id: string) => void;
}

export const ResourceList: FC<ResourceListProps> = ({
  resources,
  setAddResource,
  handleEdit,
  actionConfirm,
}) => {
  const { state } = useSession();
  const { currentUser } = state;
  const headers = ['Name', 'Category', 'Capacity', 'Unit'];
  const optionalHeader = [...headers, 'Action'];
  const coloumnHeaders =
    currentUser.role === UserRoleType.Admin ? optionalHeader : headers;

  const actionSubmit = (
    status: ResourceStatusType | null | undefined,
    resourceId: string,
  ) => {
    actionConfirm &&
      actionConfirm(
        status === ResourceStatusType.Active ? 'Deactivate' : 'Activate',
        resourceId,
      );
  };
  return (
    <>
      <div className="p-6 bg-white rounded-lg mt-6 mb-10">
        <h1 className="inline-block text-2xl font-semibold">Resources</h1>
        {currentUser.role === UserRoleType.Admin && (
          <button
            type="button"
            className="bg-sky-600 float-right text-white px-4 py-2 rounded-md text-lg font-semibold hover:bg-sky-700"
            onClick={() => setAddResource(true)}
          >
            Add Resource
          </button>
        )}
        <div className="clear-both" />
        {resources?.length === 0 ? (
          <NoRecords />
        ) : (
          <div className="flex flex-col">
            <div className="-my-2 mt-4 sm:-mx-6 lg:-mx-8">
              <div className="py-2 align-middle inline-block min-w-full sm:px-6 lg:px-8">
                <div className="sm:rounded-lg">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-white">
                      <tr className="border-b border-gray-300">
                        {coloumnHeaders.map(coloumn => (
                          <th
                            key={coloumn}
                            scope="col"
                            className="py-3 text-left text-md font-semibold text-gray-700 tracking-wider"
                          >
                            {coloumn}
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {resources?.map(resource => (
                        <tr
                          className={
                            resource.status === ResourceStatusType.Active
                              ? 'border-b border-gray-300'
                              : 'border-b border-gray-300 bg-stone-200'
                          }
                          key={resource.id}
                        >
                          <td className="py-4 whitespace-nowrap ">
                            {resource.name ?? '-'}
                          </td>
                          <td className="py-4 whitespace-nowrap">
                            {resource.resourceCategory ?? '-'}
                          </td>
                          <td className="py-4 whitespace-nowrap ">
                            {resource.capacity ?? '-'}
                          </td>
                          <td className="py-4 whitespace-nowrap ">
                            {resource.unit ?? '-'}
                          </td>
                          {currentUser.role === UserRoleType.Admin && (
                            <td className="py-4 whitespace-nowrap">
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
                                        handleEdit(resource as resourceType)
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
                                        actionSubmit(
                                          resource.status,
                                          resource.id,
                                        )
                                      }
                                    >
                                      {resource.status ===
                                      ResourceStatusType.Active
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
              </div>
            </div>
          </div>
        )}
      </div>
      <div className="clear-both" />
    </>
  );
};
