import { useState } from 'react';
import moment from 'moment';
import graphQLClient from '@lib/useGQLQuery';
import { DateRangePicker } from '../CommonPage/DateRangePicker';
import { ResourceConsumption } from '../CommonPage/ResourceConsumption';
import { dateBeforeOneWeek, todayDate, waterQualityType } from '@lib/common';
import {
  ResourceResourceCategoryType,
  useResourcesDataByDateQuery,
  useWaterQualityDevicesDetailsQuery,
} from '@api/graphql';
import { ApiLoader } from '../CommonPage/ApiLoader';
import { useSession } from '@lib/useSession';

export const SewageDashboard = () => {
  const { state } = useSession();
  const { dateRange } = state;
  const [fromDate, setFromDate] = useState<string>(dateBeforeOneWeek);
  const [toDate, setToDate] = useState<string>(todayDate);
  let quality: string = '';
  const columnHeaders = ['Type', 'Value', 'Quality', ''];
  const pHValue = 'pH';
  const qualityTypes = ['Bad', 'Average', 'Good'];
  const pHQualityTypes = ['Acidic', 'Basic', 'Neutral'];
  const differenceInTime =
    new Date(toDate).getTime() - new Date(fromDate).getTime();
  const differenceInDays = differenceInTime / (1000 * 3600 * 24);

  const { data: resources, isLoading: resourceLoader } =
    useResourcesDataByDateQuery(graphQLClient(), {
      from: fromDate,
      to: toDate,
      where: {
        tenant: null,
        resourceCategory: {
          equals: ResourceResourceCategoryType.SewageTreatment,
        },
      },
    });

  const { data: devices, isLoading } = useWaterQualityDevicesDetailsQuery(
    graphQLClient(),
    {
      where: {
        resource: {
          resourceCategory: {
            equals: ResourceResourceCategoryType.SewageTreatment,
          },
        },
        deviceType: {
          name: {
            in: ['BOD', 'TDS', 'pH', 'TSS', 'COD'],
          },
        },
      },
    },
  );

  const submitDates = () => {
    setFromDate(moment(dateRange.from).format());
    setToDate(moment(dateRange.to).format());
  };

  const checkWaterQuality = (deviceData: waterQualityType) => {
    const deviceReadSum = deviceData.deviceReadSum as number;
    const deviceLowScale = deviceData?.deviceType?.scale?.low as number;
    const deviceHighScale = deviceData?.deviceType?.scale?.high as number;
    const deviceTypeName = deviceData?.deviceType?.name;

    const isValidDeviceData = Boolean(
      deviceReadSum && deviceLowScale && deviceHighScale,
    );
    const isBadQuality = Boolean(deviceReadSum < deviceLowScale);
    const isMediumQuality = Boolean(deviceReadSum < deviceHighScale);

    if (isValidDeviceData) {
      if (isBadQuality) {
        quality =
          deviceTypeName === pHValue ? pHQualityTypes[0] : qualityTypes[0];
      } else if (isMediumQuality) {
        quality =
          deviceTypeName === pHValue ? pHQualityTypes[1] : qualityTypes[1];
      } else {
        quality =
          deviceTypeName === pHValue ? pHQualityTypes[2] : qualityTypes[2];
      }
      return quality;
    }
  };

  const qualityColor = (deviceType: string) => {
    let color: string = '';
    const pHColor =
      quality === pHQualityTypes[0]
        ? (color = '#e13d23')
        : quality === pHQualityTypes[2]
        ? (color = '#66c71c')
        : (color = '#0284c7');

    const qualityColor =
      quality === qualityTypes[0]
        ? (color = '#e13d23')
        : quality === qualityTypes[1]
        ? (color = '#e5c02c')
        : (color = '#66c71c');

    deviceType === pHValue ? pHColor : qualityColor;
    return color;
  };

  if (isLoading && resourceLoader) return <ApiLoader />;
  return (
    <div className="lg:flex sm:block">
      <div className="w-full rounded-lg bg-white p-6 mb-6 lg:mr-6 lg:mb-0 sm:mx-0 lg:w-3/5">
        <h2 className="inline-block text-xl font-semibold mb-4 mt-1 float-left">
          Water Quality
        </h2>
        <div className="clear-both" />
        <div className="flex flex-col">
          <div className="-my-2 mt-4 sm:-mx-6 lg:-mx-8">
            <div className="py-2 align-middle inline-block min-w-full sm:px-6 lg:px-8">
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
                    {devices?.devices?.map(device => (
                      <tr key={device.id} className="border-b border-gray-300">
                        <td className="py-4 whitespace-nowrap hover:text-sky-500 cursor-pointer">
                          {device.deviceType?.name}
                        </td>
                        <td className="py-4 whitespace-nowrap">
                          {device.deviceReadSum}
                        </td>
                        <td className="py-4 whitespace-nowrap">
                          {checkWaterQuality(device as waterQualityType)}
                        </td>
                        <td className="py-4 whitespace-nowrap">
                          <div
                            className="w-6 inline-block	h-2.5"
                            style={{
                              backgroundColor: qualityColor(
                                device.deviceType?.name as string,
                              ),
                            }}
                          />
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>

        <div className="clear-both" />
      </div>

      <div className="w-full rounded-lg bg-white p-6 lg:w-2/5">
        <h2 className="inline-block text-xl font-semibold mb-4 mt-1 float-left">
          Sewage Tank
        </h2>
        <div className="float-right bg-white rounded-md mb-5 single-datepicker-outer">
          <DateRangePicker {...{ submitDates }} />
        </div>
        <div className="clear-both" />
        <div className="w-full px-8 py-8">
          {resources?.resources?.map((resource, index) => (
            <div key={index}>
              <ResourceConsumption {...{ resource, differenceInDays }} />
            </div>
          ))}
        </div>
        <div className="clear-both" />
      </div>
    </div>
  );
};
