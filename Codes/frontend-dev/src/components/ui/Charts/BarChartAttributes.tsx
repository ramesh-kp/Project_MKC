import { BarLegendProps } from '@nivo/bar';

export const marginData = { top: 50, right: 130, bottom: 50, left: 60 };

export const defValues = [
  {
    id: 'dots',
    type: 'patternDots',
    background: 'inherit',
    color: '#38bcb2',
    size: 4,
    padding: 1,
    stagger: true,
  },
  {
    id: 'lines',
    type: 'patternLines',
    background: 'inherit',
    color: '#eed312',
    rotation: -45,
    lineWidth: 6,
    spacing: 10,
  },
];

export const fillValues = [
  {
    match: {
      id: 'fries',
    },
    id: 'dots',
  },
  {
    match: {
      id: 'sandwich',
    },
    id: 'lines',
  },
];

export const borderColors = {
  from: 'color',
  modifiers: [['darker', 1.6]],
};

export const legendData = [
  {
    dataFrom: 'keys',
    anchor: 'top',
    direction: 'row',
    justify: false,
    translateX: 250,
    translateY: -50,
    itemsSpacing: 2,
    itemWidth: 100,
    itemHeight: 20,
    itemDirection: 'left-to-right',
    itemOpacity: 0.85,
    symbolSize: 20,
    effects: [
      {
        on: 'hover',
        style: {
          itemOpacity: 1,
        },
      },
    ],
  },
] as BarLegendProps[];

export const valueScaleData = { type: 'linear' as 'band' };
export const paddingValue = 0.3;
export const innerPaddingData = 2;

export declare type ScaleBandSpec = {
  type: 'band';
  round?: boolean;
};

export const indexScaleData = { type: 'band', round: true } as ScaleBandSpec;
