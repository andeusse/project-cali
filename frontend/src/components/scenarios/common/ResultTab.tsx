import {
  Button,
  FormControl,
  Grid,
  InputLabel,
  MenuItem,
  Select,
} from '@mui/material';
import React, { useRef, useState } from 'react';
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

type Props = {
  data: SmartSystemOutput;
};

const ResultTab = (props: Props) => {
  const { data } = props;

  const getDataFromSerie = (index: number) => {
    const serie: number[] = [];
    data.data.forEach((d) => {
      serie.push(d[index]);
    });
    return serie;
  };

  const getSeriesFromData = () => {
    const series: any[] = [];
    data.columns.forEach((d, i) => {
      series.push({
        id: d,
        label: data.columns[i],
        data: getDataFromSerie(i),
        backgroundColor: [randomColorGenerator()],
        borderColor: ['rgba(0,0,0,0.5)'],
        borderWidth: 1,
      });
    });
    return series;
  };

  const [currentGraphs, setCurrentGraphs] = useState<string[]>([]);

  const [allSeries] = useState(getSeriesFromData());

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
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Sistema'.toUpperCase(),
      },
    },
  };

  const [selectedVariable, setSelectedVariable] = useState<string>('');

  const handleAddGraph = () => {
    currentGraphs.push(selectedVariable);
    setSelectedVariable('');
  };

  const handleDeleteGraph = (e: string) => {
    setCurrentGraphs(currentGraphs.filter((f) => f !== e));
  };

  const labels: string[] = data.index.map((i) => `P ${i + 1}`);

  let series = {
    labels: labels,
    datasets: allSeries.filter((f) => !f.id.includes('SOC')),
  };

  return (
    <Grid container spacing={2}>
      <Grid item xs={12} md={12} xl={12}>
        <Bar id={`main-chart`} ref={chartRef} data={series} options={options} />
      </Grid>
      <Grid item xs={12} md={12} xl={12}>
        <Grid container spacing={2}>
          <Grid item xs={12} md={12} xl={3}>
            <h2>Gráficas de tiempo</h2>
            <FormControl
              fullWidth
              sx={{ marginBottom: '10px', marginTop: '10px' }}
            >
              <InputLabel id="variable-select-label">Variable</InputLabel>
              <Select
                labelId="variable-select-label"
                label="Variable"
                value={selectedVariable}
                onChange={(e) => setSelectedVariable(e.target.value)}
              >
                {data.columns.map((v, index) => (
                  <MenuItem key={`${index}${v}`} value={v}>
                    {v}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            <Button
              fullWidth
              variant="outlined"
              startIcon={<AddIcon />}
              onClick={handleAddGraph}
              disabled={selectedVariable === ''}
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
                      serie={allSeries.find((f) => f.id === g)}
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
