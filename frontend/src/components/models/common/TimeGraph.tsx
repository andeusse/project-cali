import React, { useRef } from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  LinearScale,
  CategoryScale,
  TimeScale,
  PointElement,
  LineElement,
  Title,
  Tooltip as ChartJSTooltip,
  Legend,
  ChartOptions,
} from 'chart.js';
import Zoom from 'chartjs-plugin-zoom';
import { saveAs } from 'file-saver';
import { Grid } from '@mui/material';
import ZoomOutMapIcon from '@mui/icons-material/ZoomOutMap';
import ImageIcon from '@mui/icons-material/Image';
import DeleteIcon from '@mui/icons-material/Delete';
import FileDownloadIcon from '@mui/icons-material/FileDownload';

import { GraphType } from '../../../types/graph';
import { CustomIconButton } from '../../UI/CustomIconButton';
import { array2CSV } from '../../../utils/array2CSV';

type Props = {
  graph: GraphType;
  title: string | undefined;
  handleDeleteChart: (e: string) => void;
};

const TimeGraph = (props: Props) => {
  const { graph, title, handleDeleteChart } = props;

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
      duration: 200,
    },
    plugins: {
      legend: {
        position: 'top' as const,
        onClick: (e: any) => {},
      },
      title: {
        display: true,
        text: title ? title.toUpperCase() : graph.variable,
      },
      zoom: {
        pan: {
          enabled: true,
          mode: 'x' as const,
          modifierKey: 'ctrl' as const,
        },
        zoom: {
          drag: {
            enabled: true,
          },
          pinch: {
            enabled: true,
          },
          mode: 'x' as const,
        },
      },
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

  const handleResetZoom = () => {
    chartRef.current.resetZoom();
  };

  const handleSaveCSV = () => {
    var blob = new Blob(
      [array2CSV([graph.xValues, graph.yValues], ['Time', title ? title : ''])],
      {
        type: 'text/csv;charset=utf-8',
      }
    );
    saveAs(blob, `${graph.variable}-data.csv`);
  };

  const handleSavePNG = () => {
    const canvas: any = document.getElementById(`${graph.variable}-chart`);
    canvas.toBlob((blob: any) => {
      saveAs(blob, `${graph.variable}.png`);
    });
  };

  return (
    <Grid container>
      <Grid
        item
        xs={12}
        md={12}
        xl={12}
        sx={{
          textAlign: 'center',
        }}
      >
        <CustomIconButton
          icon={<ZoomOutMapIcon fontSize="inherit" />}
          tooltip="Reset Zoom"
          handleClick={handleResetZoom}
        ></CustomIconButton>
        <CustomIconButton
          icon={<FileDownloadIcon fontSize="inherit" />}
          tooltip="Download CSV"
          handleClick={handleSaveCSV}
        ></CustomIconButton>
        <CustomIconButton
          icon={<ImageIcon fontSize="inherit" />}
          tooltip="Download chart PNG"
          handleClick={handleSavePNG}
        ></CustomIconButton>
        <CustomIconButton
          icon={<DeleteIcon fontSize="inherit" />}
          color="error"
          tooltip="Remove chart"
          handleClick={() => handleDeleteChart(graph.variable)}
        ></CustomIconButton>
      </Grid>
      <Grid item xs={12} md={12} xl={12}>
        <Line
          id={`${graph.variable}-chart`}
          ref={chartRef}
          options={options}
          data={data}
        />
      </Grid>
    </Grid>
  );
};

export default TimeGraph;
