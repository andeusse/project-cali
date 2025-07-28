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
  TimeSeriesScale,
} from 'chart.js';
import Zoom from 'chartjs-plugin-zoom';
import 'chartjs-adapter-moment';
import { saveAs } from 'file-saver';
import { Grid } from '@mui/material';
import ZoomOutMapIcon from '@mui/icons-material/ZoomOutMap';
import ImageIcon from '@mui/icons-material/Image';
import DeleteIcon from '@mui/icons-material/Delete';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import GridOnIcon from '@mui/icons-material/GridOn';
import { ChartType } from '../../../types/graph';
import { CustomIconButton } from '../../UI/CustomIconButton';
import { DiagramVariableType } from '../../../types/models/common';
import { DownloadCSV, DownloadExcel } from '../../../utils/saveFormats';
import { array2Array } from '../../../utils/array2CSV';

type Props = {
  chart: ChartType;
  variables: DiagramVariableType[];
  handleDeleteChart: (e: string) => void;
  isPlaying: boolean;
  maxPlayingValues?: number;
};

const TimeGraph = (props: Props) => {
  const {
    chart,
    variables,
    handleDeleteChart,
    isPlaying,
    maxPlayingValues = 20,
  } = props;

  const chartRef = useRef<any>(undefined);

  ChartJS.register(
    LinearScale,
    CategoryScale,
    TimeScale,
    TimeSeriesScale,
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
      y: {
        title: {
          display: true,
          text:
            variables.length === 1
              ? `${variables[0].name} (${variables[0].unit})`
              : '',
        },
      },
      x: {
        type: 'time',
        ticks: {
          autoSkip: true,
          maxTicksLimit: 10,
          maxRotation: 45,
          minRotation: 20,
        },
      },
    },
    interaction: {
      mode: 'index',
    },
    plugins: {
      legend: {
        position: 'top' as const,
        // onClick: (e: any) => {},
      },
      title: {
        display: true,
        text:
          variables.length === 1
            ? variables[0].name.toUpperCase()
            : 'Gráfica de tiempo',
      },
      zoom: !isPlaying
        ? {
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
          }
        : {},
    },
  };

  const data = {
    labels: isPlaying
      ? chart.chartValues.xValues.slice(-maxPlayingValues)
      : chart.chartValues.xValues,
    datasets: chart.chartValues.variables.map((c) => {
      const variable = variables.find((v) => v.variable === c.variable);
      return {
        label: variable
          ? `${variable.name} ${
              variable.unit !== '' ? `[${variable.unit}]` : ''
            }`
          : '',
        data: isPlaying ? c.yValues.slice(-maxPlayingValues) : c.yValues,
        borderColor: c.color,
        backgroundColor: c.color,
      };
    }),
  };

  const handleResetZoom = () => {
    chartRef.current.resetZoom();
  };

  const handleSaveCSV = () => {
    const data = [
      ['Time', ...chart.chartValues.variables.map((v) => v.variable)],
      ...array2Array([
        chart.chartValues.xValues,
        ...chart.chartValues.variables.map((v) => v.yValues),
      ]),
    ];
    DownloadCSV(data, 'Data');
  };

  const handleDownloadExcel = () => {
    const data = [
      ['Time', ...chart.chartValues.variables.map((v) => v.variable)],
      ...array2Array([
        chart.chartValues.xValues,
        ...chart.chartValues.variables.map((v) => v.yValues),
      ]),
    ];
    DownloadExcel(data, 'Data');
  };

  const handleSavePNG = () => {
    const canvas: any = document.getElementById(`${chart.guid}-chart`);
    canvas.toBlob((blob: any) => {
      saveAs(blob, `GraficaDeTiempo.png`);
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
          disabled={isPlaying}
        ></CustomIconButton>
        <CustomIconButton
          icon={<FileDownloadIcon fontSize="inherit" />}
          tooltip="Download CSV"
          handleClick={handleSaveCSV}
          disabled={isPlaying}
        ></CustomIconButton>
        <CustomIconButton
          icon={<GridOnIcon fontSize="inherit" />}
          tooltip="Download XLSX"
          handleClick={handleDownloadExcel}
          disabled={isPlaying}
        ></CustomIconButton>
        <CustomIconButton
          icon={<ImageIcon fontSize="inherit" />}
          tooltip="Download chart PNG"
          handleClick={handleSavePNG}
          disabled={isPlaying}
        ></CustomIconButton>
        <CustomIconButton
          icon={<DeleteIcon fontSize="inherit" />}
          color="error"
          tooltip="Remove chart"
          handleClick={() => handleDeleteChart(chart.guid)}
        ></CustomIconButton>
      </Grid>
      <Grid item xs={12} md={12} xl={12}>
        <Line
          id={`${chart.guid}-chart`}
          ref={chartRef}
          options={options}
          data={data}
        />
      </Grid>
    </Grid>
  );
};

export default TimeGraph;
