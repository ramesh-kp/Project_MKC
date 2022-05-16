import { Dispatch, FC, SetStateAction } from 'react';
import Image from 'next/image';
import Dot from 'assets/dot.png';
import { DevicesQuery, DeviceStatusType, UserRoleType } from '@api/graphql';
import { DeviceType } from '@lib/common';

import { useSession } from '@lib/useSession';

interface SensorListProps {
  setAddSensor: Dispatch<SetStateAction<boolean>>;
  deviceData: DevicesQuery['devices'];
  handleEdit: (device: DeviceType) => void;
  actionConfirm?: (action: string, id: string) => void;
  tenantDetailView: boolean;
}

export const SensorList: FC<SensorListProps> = ({
  deviceData,
  handleEdit,
  actionConfirm,
}) => {
  const { state } = useSession();
  const { currentUser } = state;
  const headers = [
    'Name',
    'Sensor Device ID',
    'Sensor Type',
    'Edge Device Name',
    'Edge Device Port Number',
  ];

  const optionalHeader = [...headers, 'Action'];

  const coloumnHeaders =
    currentUser.role === UserRoleType.Admin ? optionalHeader : headers;

  const actionSubmit = (
    status: DeviceStatusType | null | undefined,
    deviceId: string,
  ) => {
    actionConfirm &&
      actionConfirm(
        status === DeviceStatusType.Active ? 'Deactivate' : 'Activate',
        deviceId,
      );
  };

  const tableRowStyle = (status: DeviceStatusType) => {
    let rowStyle: string = '';
    status === DeviceStatusType.Active
      ? (rowStyle = 'border-b border-gray-300')
      : (rowStyle = 'border-b border-gray-300 bg-stone-200');
    return rowStyle;
  };

  return (
    <>
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
            {deviceData?.map(device => (
              <tr
                className={tableRowStyle(device.status as DeviceStatusType)}
                key={device.id}
              >
                <td className="py-4 whitespace-nowrap ">
                  {device.name ?? '-'}
                </td>
                <td className="py-4 whitespace-nowrap ">
                  {device.deviceId ?? '-'}
                </td>
                <td className="py-4 whitespace-nowrap">
                  {device.deviceType?.name ?? '-'}
                </td>
                <td className="py-4 whitespace-nowrap">
                  {device.edgeDeviceId ?? '-'}
                </td>
                <td className="py-4 whitespace-nowrap">
                  {device.portNumber ?? '-'}
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
                            onClick={() => handleEdit(device as DeviceType)}
                          >
                            Edit
                          </label>
                        </li>
                        <li>
                          <label
                            htmlFor="my-modal"
                            className="py-1 rounded-none modal-button"
                            onClick={() =>
                              actionSubmit(device.status, device.id)
                            }
                          >
                            {device.status === DeviceStatusType.Active
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
