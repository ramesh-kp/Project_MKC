import { Dispatch, FC, SetStateAction } from 'react';
import { useRouter } from 'next/router';
import Image from 'next/image';
import Dot from 'assets/dot.png';
import { UsersQuery, UserStatusType } from '@api/graphql';
import { UsersType } from '@lib/common';

export interface listViewprops {
  tableData: UsersQuery['users'];
  setAddUserFlag: Dispatch<SetStateAction<boolean>>;
  setEditData: Dispatch<SetStateAction<UsersType>>;
  actionConfirm: (action: string, id: string) => void;
}

export const UserListView: FC<listViewprops> = ({
  tableData,
  setAddUserFlag,
  setEditData,
  actionConfirm,
}) => {
  const router = useRouter();
  const coloumnHeaders = [
    'User Name',
    'Tenant Name',
    'Email',
    'Phone',
    'Action',
  ];

  const actionSubmit = (
    status: UserStatusType | null | undefined,
    deviceId: string,
  ) => {
    actionConfirm(
      status === UserStatusType.Inactive
        ? UserStatusType.Active
        : UserStatusType.Inactive,
      deviceId,
    );
  };

  return (
    <div className="sm:rounded-lg">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-white">
          <tr className="border-b border-gray-300">
            {coloumnHeaders.map(coloumn => (
              <th
                key={coloumn}
                scope="col"
                className="py-3 text-left text-md font-semibold text-gray-700 tracking-wider w-1/10"
              >
                {coloumn}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {tableData?.map(user => {
            return (
              <tr
                className={
                  user.status === UserStatusType.Active
                    ? 'border-b border-gray-300'
                    : 'border-b border-gray-300 bg-stone-200'
                }
                key={user.id}
              >
                <td className="py-4 whitespace-nowrap">{user.name}</td>
                <td
                  className="py-4 whitespace-nowrap hover:text-sky-500 cursor-pointer"
                  onClick={() => router.push(`/tenant/${user?.tenant?.id}`)}
                >
                  {user.tenant?.name ?? '-'}
                </td>
                <td className="py-4 whitespace-nowrap">{user.email}</td>
                <td className="py-4 whitespace-nowrap">{user.phone ?? '-'}</td>

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
                          onClick={() => {
                            setEditData(user as UsersType);
                            setAddUserFlag(true);
                          }}
                        >
                          Edit
                        </label>
                      </li>
                      <li>
                        <label
                          htmlFor="my-modal"
                          className="py-1 rounded-none modal-button"
                          onClick={() => actionSubmit(user.status, user.id)}
                        >
                          {user.status === UserStatusType.Active
                            ? 'Deactivate'
                            : 'Activate'}
                        </label>
                      </li>
                    </ul>
                  </div>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};
