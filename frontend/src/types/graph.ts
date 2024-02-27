export type GraphType = {
  variable: string;
  xValues: number[];
  yValues: number[];
};

export const GRAPH_TEST: GraphType[] = [
  {
    variable: 'Var 1',
    xValues: [1, 2, 3, 4, 5],
    yValues: [1, 2, 3, 4, 5],
  },
  {
    variable: 'Var 2',
    xValues: [1, 2, 3, 4, 5],
    yValues: [5, 4, 3, 2, 1],
  },
  {
    variable: 'Var 3',
    xValues: [1, 2, 3, 4, 5],
    yValues: [10, 15, 20, 15, 0],
  },
  {
    variable: 'Var 4',
    xValues: [1, 2, 3, 4, 5],
    yValues: [-5, -10, -15, -20, 10],
  },
];
