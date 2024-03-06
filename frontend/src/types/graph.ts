import moment from 'moment';

export type GraphType = {
  variable: string;
  xValues: any[];
  yValues: number[];
};

const xValues = [
  moment().add(0, 's').format('LTS'),
  moment().add(1, 's').format('LTS'),
  moment().add(2, 's').format('LTS'),
  moment().add(3, 's').format('LTS'),
  moment().add(4, 's').format('LTS'),
];

export const GRAPH_TEST: GraphType[] = [
  {
    variable: 'Var 1',
    xValues: xValues,
    yValues: [1, 2, 3, 4, 5],
  },
  {
    variable: 'Var 2',
    xValues: xValues,
    yValues: [5, 4, 3, 2, 1],
  },
  {
    variable: 'Var 3',
    xValues: xValues,
    yValues: [10, 15, 20, 15, 0],
  },
  {
    variable: 'Var 4',
    xValues: xValues,
    yValues: [-5, -10, -15, -20, 10],
  },
];
