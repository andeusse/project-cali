import React, { useEffect, useState } from 'react';
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
  Slider,
  Typography,
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import { ChartType, ChartValue, ChartValues } from '../../../types/graph';
import TimeGraph from './TimeGraph';
import { DiagramVariableType } from '../../../types/models/common';
import CustomNumberField from '../../UI/CustomNumberField';
import { InputType } from '../../../types/inputType';
import { compareStrings } from '../../../utils/compareStrings';
import { v4 as uuidv4 } from 'uuid';

type Props = {
  timeMultiplier: InputType;
  timeMultiplierAdditionalCondition?: boolean;
  handleChange: (e: any) => void;
  charts: ChartValues;
  variables: DiagramVariableType[];
  playerControl: React.ReactNode;
  isPlaying: boolean;
};

const TimeGraphs = (props: Props) => {
  const {
    timeMultiplier,
    handleChange,
    charts,
    variables,
    playerControl,
    isPlaying,
    timeMultiplierAdditionalCondition = false,
  } = props;

  const [availableGraphs, setAvailableGraphs] = useState([...charts.variables]);

  const marks = [
    {
      value: timeMultiplier.min ? timeMultiplier.min : 1,
      label: timeMultiplier.min ? timeMultiplier.min.toString() : 'Min',
    },
    {
      value: timeMultiplier.max ? timeMultiplier.max : 10,
      label: timeMultiplier.max ? timeMultiplier.max.toString() : 'Max',
    },
  ];

  useEffect(() => {
    setAvailableGraphs([...charts.variables]);
  }, [charts]);

  const [selectedVariables, setSelectedVariables] = useState<string[]>([]);

  const [currentGraphs, setCurrentGraphs] = useState<ChartType[]>([]);

  const handleAddGraph = () => {
    const variables: ChartValue[] = [];
    selectedVariables.forEach((s) => {
      var newChart = availableGraphs.find((g) => g.variable === s);
      if (newChart) {
        variables.push(newChart);
      }
    });
    const chart: ChartType = {
      guid: uuidv4(),
      chartValues: {
        xValues: charts.xValues,
        variables: variables,
      },
    };
    setCurrentGraphs([...currentGraphs, chart]);
    setSelectedVariables([]);
  };

  const handleVariableSelectedChange = (event: SelectChangeEvent<string[]>) => {
    const {
      target: { value },
    } = event;
    setSelectedVariables(typeof value === 'string' ? value.split(',') : value);
  };

  const handleRemoveGraph = (e: string) => {
    setCurrentGraphs(currentGraphs.filter((f) => f.guid !== e));
  };

  return (
    <>
      <Grid container spacing={2}>
        <Grid item xs={12} md={2} xl={2}>
          <h2>Gráficas de tiempo</h2>
          <Typography id="input-slider" gutterBottom>
            Multiplicador de velocidad:
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} md={12} xl={7}>
              <Slider
                aria-label="TimeMultiplier"
                value={timeMultiplier.value}
                name="timeMultiplier"
                valueLabelDisplay="auto"
                step={timeMultiplier.step}
                marks={marks}
                min={timeMultiplier.min}
                max={timeMultiplier.max}
                disabled={
                  timeMultiplier.disabled || timeMultiplierAdditionalCondition
                }
                onChange={handleChange}
              />
            </Grid>
            <Grid item xs={12} md={12} xl={5}>
              <CustomNumberField
                variable={timeMultiplier}
                name="timeMultiplier"
                handleChange={handleChange}
                disabled={timeMultiplierAdditionalCondition}
              ></CustomNumberField>
            </Grid>
          </Grid>
          <FormControl
            fullWidth
            sx={{ marginBottom: '10px', marginTop: '10px' }}
          >
            <InputLabel id="variable-select-label">Variable</InputLabel>
            <Select
              labelId="variable-select-label"
              label="Variable"
              multiple
              value={selectedVariables}
              onChange={(e) => handleVariableSelectedChange(e)}
              renderValue={(selected) => selected.join(', ')}
            >
              {variables
                .sort((a, b) => compareStrings(a.name, b.name))
                .map((v, index) => {
                  if (v.isShown) {
                    return (
                      <MenuItem key={`${index}${v.name}`} value={v.variable}>
                        <Checkbox
                          checked={selectedVariables.indexOf(v.variable) > -1}
                        />
                        <ListItemText
                          primary={`${v.name} ${
                            v.unit !== '' ? `[${v.unit}]` : ''
                          }`}
                        />
                      </MenuItem>
                    );
                  }
                  return null;
                })}
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
        <Grid item xs={12} md={10} xl={10}>
          {playerControl}
          <Grid container spacing={2}>
            {currentGraphs.map((g, index) => {
              return (
                <Grid key={`${index}_${g}`} item xs={12} md={6} xl={6}>
                  <TimeGraph
                    chart={g}
                    variables={variables}
                    handleDeleteChart={handleRemoveGraph}
                    isPlaying={isPlaying}
                  ></TimeGraph>
                </Grid>
              );
            })}
          </Grid>
        </Grid>
      </Grid>
    </>
  );
};

export default TimeGraphs;
