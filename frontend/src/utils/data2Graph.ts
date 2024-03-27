import { CommonGraphType, GraphType } from '../types/graph';

export const data2Graph = <T extends CommonGraphType>(data: T): GraphType[] => {
  const graphs: GraphType[] = [];

  for (const key in data) {
    if (key !== 'time' && key !== 'timeMoment') {
      const graph: GraphType = {
        variable: key,
        xValues: data['time'],
        yValues: data[key] as number[],
      };
      graphs.push(graph);
    }
  }
  return graphs;
};
