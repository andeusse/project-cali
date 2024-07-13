export type CommonChartType = {
  time: string[];
};

export type ChartType = {
  guid: string;
  chartValues: ChartValues;
};

export type ChartValues = {
  xValues: string[];
  variables: ChartValue[];
};

export type ChartValue = {
  variable: string;
  yValues: number[];
  color: string;
};
