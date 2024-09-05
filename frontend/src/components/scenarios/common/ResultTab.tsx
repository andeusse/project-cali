import {
  Button,
  Checkbox,
  FormControl,
  Grid,
  InputLabel,
  ListItemText,
  MenuItem,
  Select,
  SelectChangeEvent,
} from '@mui/material';
import React, { useCallback, useEffect, useRef, useState } from 'react';
import { SmartSystemOutput } from '../../../types/scenarios/common';
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
import { Bar } from 'react-chartjs-2';
import { randomColorGenerator } from '../../../utils/randomColorGenerator';
import AddIcon from '@mui/icons-material/Add';
import BarGraph from './BarGraph';
import saveAs from 'file-saver';
import { CustomIconButton } from '../../UI/CustomIconButton';
import ImageIcon from '@mui/icons-material/Image';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import { array2CSV } from '../../../utils/array2CSV';

type Props = {
  data: SmartSystemOutput;
};

const ResultTab = (props: Props) => {
  const { data } = props;

  const [currentGraphs, setCurrentGraphs] = useState<string[]>([]);

  const [allSeries, setAllSeries] = useState<any>([]);

  const [mainChartSeries, setMainChartSeries] = useState<any>();

  const [labels, setLabels] = useState<string[]>([]);

  const [selectedVariables, setSelectedVariables] = useState<string[]>([]);

  const getSeriesFromData = useCallback(() => {
    const series: any[] = [];
    data.columns.forEach((d, i) => {
      const serie: number[] = [];
      data.data.forEach((d) => {
        serie.push(d[i]);
      });
      series.push({
        id: d,
        label: data.columns[i],
        data: serie,
        backgroundColor: [randomColorGenerator()],
        borderColor: ['rgba(0,0,0,0.5)'],
        borderWidth: 1,
      });
    });
    setLabels(data.index.map((i) => `P ${i + 1}`));
    setAllSeries(series);
    let chartSeries = {
      labels: data.index.map((i) => `P ${i + 1}`),
      datasets: series.filter(
        (f: { id: string | string[] }) =>
          !f.id.includes('_SOC') && !f.id.includes('_Energia')
      ),
    };
    setMainChartSeries(chartSeries);
  }, [data.columns, data.data, data.index]);

  useEffect(() => {
    getSeriesFromData();
  }, [getSeriesFromData]);

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
          text: `Potencia [kW]`.toUpperCase(),
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
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Sistema'.toUpperCase(),
      },
    },
  };

  const handleSelectedVariableChange = (event: SelectChangeEvent<string[]>) => {
    const {
      target: { value },
    } = event;
    setSelectedVariables(typeof value === 'string' ? value.split(',') : value);
  };

  const handleAddGraph = () => {
    setCurrentGraphs([...currentGraphs, ...selectedVariables]);
    setSelectedVariables([]);
  };

  const handleDeleteGraph = (e: string) => {
    setCurrentGraphs(currentGraphs.filter((f) => f !== e));
  };

  const handleSaveCSV = () => {
    var blob = new Blob(
      [array2CSV([data.columns, ...data.data], ['Sistema', ...labels])],
      {
        type: 'text/csv;charset=utf-8',
      }
    );
    saveAs(blob, `Sistema-data.csv`);
  };

  const handleSavePNG = () => {
    const canvas: any = document.getElementById(`main-chart`);
    canvas.toBlob((blob: any) => {
      saveAs(blob, `Sistema.png`);
    });
  };

  let series = {
    labels: labels,
    datasets: allSeries.filter(
      (f: { id: string | string[] }) => !f.id.includes('SOC')
    ),
  };

  return (
    <Grid container spacing={2}>
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
      </Grid>
      <Grid item xs={12} md={12} xl={12}>
        <Bar
          id={`main-chart`}
          ref={chartRef}
          data={mainChartSeries ? mainChartSeries : series}
          options={options}
        />
      </Grid>
      <Grid item xs={12} md={12} xl={12}>
        <Grid container spacing={2}>
          <Grid item xs={12} md={12} xl={3}>
            <h2>Gráficas individuales</h2>
            <FormControl
              fullWidth
              sx={{ marginBottom: '10px', marginTop: '10px' }}
            >
              <InputLabel id="variable-select-label">Variable</InputLabel>
              <Select
                labelId="variable-select-label"
                label="Variable"
                multiple
                renderValue={(selected) => selected.join(', ')}
                value={selectedVariables}
                onChange={(e) => handleSelectedVariableChange(e)}
              >
                {data.columns.map((v, index) => (
                  <MenuItem key={`${index}${v}`} value={v}>
                    <Checkbox checked={selectedVariables.indexOf(v) > -1} />
                    <ListItemText primary={`${v}`} />
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            <Button
              fullWidth
              variant="outlined"
              startIcon={<AddIcon />}
              onClick={handleAddGraph}
              disabled={selectedVariables.length === 0}
            >
              Add
            </Button>
          </Grid>
          <Grid item xs={12} md={12} xl={9}>
            <Grid container spacing={2}>
              {currentGraphs.map((g, index) => {
                return (
                  <Grid key={`${index}-${g}`} item xs={12} md={12} xl={6}>
                    <BarGraph
                      handleDeleteChart={handleDeleteGraph}
                      labels={labels}
                      title={g}
                      serie={allSeries.find((f: any) => f.id === g)}
                    ></BarGraph>
                  </Grid>
                );
              })}
            </Grid>
          </Grid>
        </Grid>
      </Grid>
    </Grid>
  );
};

export default ResultTab;
