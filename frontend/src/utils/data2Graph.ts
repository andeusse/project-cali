import { CommonChartType, ChartValue, ChartValues } from '../types/graph';
import { randomColorGenerator } from './randomColorGenerator';

export const data2Graph = <T extends CommonChartType>(data: T): ChartValues => {
  const graphValues: ChartValues = {
    xValues: data['time'],
    variables: [],
  };
  for (const key in data) {
    if (key !== 'time') {
      const graphValue: ChartValue = {
        variable: key,
        yValues: data[key] as number[],
        color: randomColorGenerator(),
      };
      graphValues.variables.push(graphValue);
    }
  }
  return graphValues;
};
