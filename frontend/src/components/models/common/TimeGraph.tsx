import React from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { GraphType } from '../../../types/graph';

type Props = {
  graph: GraphType;
  title: string | undefined;
};

const TimeGraph = (props: Props) => {
  const { graph, title } = props;

  ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
  );

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
        onClick: (e: any) => {},
      },
      title: {
        display: true,
        text: title ? title : graph.variable,
      },
    },
    animation: {
      duration: 0,
    },
  };

  const data = {
    labels: graph.xValues,
    datasets: [
      {
        label: graph.variable,
        data: graph.yValues,
        borderColor: 'rgb(53, 162, 235)',
        backgroundColor: 'rgba(53, 162, 235, 0.5)',
      },
    ],
  };

  return <Line options={options} data={data} />;
};

export default TimeGraph;
