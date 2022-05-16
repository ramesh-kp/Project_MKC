import { FC } from 'react';
import { MyCustomCSS, resourceDataType } from '@lib/common';

interface ResourcesProps {
  resource: resourceDataType;
  differenceInDays: number;
}

export const ResourceConsumption: FC<ResourcesProps> = ({
  resource,
  differenceInDays,
}) => {
  const deviceReadSum = resource?.deviceReadSum as number;
  const capacity = resource?.capacity as number;
  const deviceReadAvg = resource?.deviceReadAvg as number;
  const deviceReadCurrent = resource?.deviceReadCurrent as number;

  const isValidDeviceData = Boolean(
    deviceReadSum && capacity && deviceReadAvg && deviceReadCurrent,
  );

  let consumptionRate: number = 0;
  let consumptionPerDay: number = 0;
  let projectedWaterAvailability: number = 0;
  let waterLevel: number = 0;

  if (isValidDeviceData) {
    consumptionRate =
      deviceReadAvg === 0 ? deviceReadAvg : (deviceReadAvg / capacity) * 100;

    consumptionPerDay = Math.round(deviceReadSum / differenceInDays);
    projectedWaterAvailability = Math.round(
      deviceReadCurrent / consumptionPerDay,
    );
    waterLevel = (deviceReadCurrent / capacity) * 100;
  }

  return (
    <div className="flex flex-col w-full lg:flex-row">
      <div className="grid flex-grow h-32 card rounded-box place-items-center">
        <div className="w-full mr-2">
          <div
            className="radial-progress"
            style={
              {
                '--value': consumptionRate === NaN ? 0 : consumptionRate,
                color: '#009fd1',
              } as MyCustomCSS
            }
          >
            {consumptionRate === NaN ? 0 : consumptionRate.toFixed(2)}%
          </div>
        </div>
      </div>
      <div className="flex">
        <div className="grid flex-grow h-32 card rounded-box leading-8">
          Water Level
          <br />
          Projected Water Availability
          <br />
          Consumption Per Day
        </div>
        <div className="grid flex-grow h-32 card rounded-box place-items-center font-semibold ml-2 leading-8 -mt-4">
          {`${waterLevel.toFixed(2)} %`}
          <br />
          {`${projectedWaterAvailability} Days`}
          <br />
          {`${consumptionPerDay} L`}
        </div>
      </div>
    </div>
  );
};
