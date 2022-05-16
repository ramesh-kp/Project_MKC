import { FC } from 'react';
import { BarDatum, ResponsiveBar } from '@nivo/bar';
import {
  defValues,
  fillValues,
  indexScaleData,
  innerPaddingData,
  legendData,
  marginData,
  paddingValue,
  valueScaleData,
} from './BarChartAttributes';

interface BarChartProps {
  barchartData: BarDatum[];
  barchartKeys: string[];
  power: boolean;
}
export const BarChart: FC<BarChartProps> = ({
  barchartData,
  barchartKeys,
  power,
}) => {
  const legendLabel = power ? 'Watts' : 'Consumption';
  return (
    <ResponsiveBar
      data={barchartData}
      keys={barchartKeys}
      indexBy="tenant"
      margin={marginData}
      padding={paddingValue}
      innerPadding={innerPaddingData}
      isInteractive
      groupMode="grouped"
      valueScale={valueScaleData}
      indexScale={indexScaleData}
      colors={{ scheme: 'paired' }}
      defs={defValues}
      fill={fillValues}
      borderColor={{
        from: 'color',
        modifiers: [['darker', 1.6]],
      }}
      axisTop={null}
      axisRight={null}
      axisBottom={{
        tickSize: 0,
        tickPadding: 2,
        tickRotation: 0,
        legend: 'Tenant',
        legendPosition: 'middle',
        legendOffset: 32,
      }}
      axisLeft={{
        tickSize: 5,
        tickPadding: 5,
        tickRotation: 0,
        legend: legendLabel,
        legendPosition: 'middle',
        legendOffset: -40,
      }}
      labelSkipWidth={100}
      labelSkipHeight={12}
      labelTextColor={{
        from: 'color',
        modifiers: [['darker', 1.6]],
      }}
      legends={legendData}
      role="application"
      ariaLabel="Nivo bar chart demo"
      barAriaLabel={e =>
        `${e.id} : ${e.formattedValue} in tenant ${e.indexValue}`
      }
    />
  );
};
