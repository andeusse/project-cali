import React from 'react';
import { GraphType } from '../../../types/graph';
import { LineChart } from '@mui/x-charts';

type Props = {
  graph: GraphType | undefined;
};

const TimeGraph = (props: Props) => {
  const { graph } = props;
  return (
    <LineChart
      xAxis={[
        {
          data: graph?.xValues,
          label: 'Time [s]',
          scaleType: 'band',
        },
      ]}
      series={[
        {
          data: graph?.yValues,
          label: graph?.variable,
        },
      ]}
      height={350}
    />
  );
};

export default TimeGraph;
