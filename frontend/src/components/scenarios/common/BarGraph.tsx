import { Grid } from '@mui/material';
import React, { useRef } from 'react';
import { Bar } from 'react-chartjs-2';
import { CustomIconButton } from '../../UI/CustomIconButton';
import {
  Chart as ChartJS,
  LinearScale,
  CategoryScale,
  TimeScale,
  PointElement,
  Title,
  Legend,
  Tooltip as ChartJSTooltip,
  BarElement,
  ChartOptions,
} from 'chart.js';

import ImageIcon from '@mui/icons-material/Image';
import DeleteIcon from '@mui/icons-material/Delete';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import { saveAs } from 'file-saver';

import { array2CSV } from '../../../utils/array2CSV';

type Props = {
  title: string;
  labels: string[];
  serie: any;
  handleDeleteChart: (e: string) => void;
};

const BarGraph = (props: Props) => {
  const { title, labels, serie, handleDeleteChart } = props;

  const chartRef = useRef<any>(undefined);

  ChartJS.register(
    LinearScale,
    CategoryScale,
    TimeScale,
    PointElement,
    BarElement,
    Title,
    ChartJSTooltip,
    Legend
  );

  const options: ChartOptions<'bar'> = {
    responsive: true,
    scales: {
      y: {
        title: {
          display: true,
          text: `Potencia [W]`.toUpperCase(),
        },
        stacked: true,
      },
      x: {
        title: {
          display: true,
          text: `Periodo`.toUpperCase(),
        },
        stacked: true,
      },
    },
    plugins: {
      legend: {
        onClick: () => {},
        position: 'top' as const,
      },
      title: {
        display: true,
        text: title.toUpperCase(),
      },
    },
  };

  let series = {
    labels: labels,
    datasets: [serie],
  };

  const handleSaveCSV = () => {
    var blob = new Blob([array2CSV([labels, serie.data], ['Time', title])], {
      type: 'text/csv;charset=utf-8',
    });
    saveAs(blob, `${title}-data.csv`);
  };

  const handleSavePNG = () => {
    const canvas: any = document.getElementById(`${title}-chart`);
    canvas.toBlob((blob: any) => {
      saveAs(blob, `${title}.png`);
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
          handleClick={() => handleDeleteChart(title)}
        ></CustomIconButton>
      </Grid>
      <Grid item xs={12} md={12} xl={12}>
        <Bar
          id={`${title}-chart`}
          ref={chartRef}
          data={series}
          options={options}
        />
      </Grid>
    </Grid>
  );
};

export default BarGraph;
