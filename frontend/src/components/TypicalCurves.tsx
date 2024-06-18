import {
  Chart as ChartJS,
  LinearScale,
  CategoryScale,
  TimeScale,
  PointElement,
  LineElement,
  Title,
  Legend,
  Tooltip as ChartJSTooltip,
  ChartOptions,
} from 'chart.js';
import Zoom from 'chartjs-plugin-zoom';
import React, { useRef } from 'react';
import { Line } from 'react-chartjs-2';

type Props = {
  title: string;
  xAxis: string;
  yAxis: string;
  maxValue: number;
  xValues: string[];
  yValues: number[];
};

const TypicalCurves = (props: Props) => {
  const { title, maxValue, xValues, yValues, xAxis, yAxis } = props;

  const chartRef = useRef<any>(undefined);

  ChartJS.register(
    LinearScale,
    CategoryScale,
    TimeScale,
    PointElement,
    LineElement,
    Title,
    ChartJSTooltip,
    Legend,
    Zoom
  );

  const options: ChartOptions<'line'> = {
    responsive: true,
    animation: {
      duration: 0,
    },
    scales: {
      x: {
        title: {
          display: true,
          text: xAxis,
        },
      },
      y: {
        title: {
          display: true,
          text: yAxis,
        },
      },
    },
    plugins: {
      legend: {
        position: 'top' as const,
        onClick: (e: any) => {},
      },
      title: {
        display: true,
        text: title.toUpperCase(),
      },
    },
  };

  const data = {
    labels: xValues,
    datasets: [
      {
        label: title,
        data: yValues.map((v) => v * maxValue),
        borderColor: 'rgb(53, 162, 235)',
        backgroundColor: 'rgba(53, 162, 235, 0.5)',
      },
    ],
  };

  return (
    <Line id={`${title}-chart`} ref={chartRef} options={options} data={data} />
  );
};

export default TypicalCurves;
