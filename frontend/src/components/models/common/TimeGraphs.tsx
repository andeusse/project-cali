import React, { useEffect, useState } from 'react';
import {
  Button,
  FormControl,
  Grid,
  InputLabel,
  MenuItem,
  Select,
  Slider,
  Typography,
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import { GraphType } from '../../../types/graph';
import TimeGraph from './TimeGraph';
import { DiagramVariableType, InputType } from '../../../types/models/common';
import CustomNumberField from '../../UI/CustomNumberField';

type Props = {
  timeMultiplier: InputType;
  handleChange: (e: any) => void;
  graphs: GraphType[];
  variables: DiagramVariableType[];
  playerControl: React.ReactNode;
  isPlaying: boolean;
};

const TimeGraphs = (props: Props) => {
  const {
    timeMultiplier,
    handleChange,
    graphs,
    variables,
    playerControl,
    isPlaying,
  } = props;

  const [availableGraphs, setAvailableGraphs] = useState([...graphs]);

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
    setAvailableGraphs([...graphs]);
  }, [graphs]);

  const [selectedVariable, setSelectedVariable] = useState<string>('');

  const [currentGraphs, setCurrentGraphs] = useState<GraphType[]>([]);

  const handleAddGraph = () => {
    const newGraph = availableGraphs.find(
      (g) => g.variable === selectedVariable
    );
    if (newGraph) {
      setCurrentGraphs([...currentGraphs, newGraph]);
      setSelectedVariable('');
    }
  };

  const handleRemoveGrahp = (e: string) => {
    setCurrentGraphs(currentGraphs.filter((f) => f.variable !== e));
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
                disabled={timeMultiplier.disabled}
                onChange={handleChange}
              />
            </Grid>
            <Grid item xs={12} md={12} xl={5}>
              <CustomNumberField
                variable={timeMultiplier}
                name="timeMultiplier"
                handleChange={handleChange}
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
              value={selectedVariable}
              onChange={(e) => setSelectedVariable(e.target.value)}
            >
              {availableGraphs.map((g, index) => (
                <MenuItem key={`${index}${g.variable}`} value={g.variable}>
                  {variables.find((v) => g.variable === v.variable)?.name}
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
        <Grid item xs={12} md={10} xl={10}>
          {playerControl}
          <Grid container spacing={2}>
            {currentGraphs.map((g, index) => {
              const variable = variables.find((v) => g.variable === v.variable);
              return (
                <Grid key={`${index}_${g}`} item xs={12} md={6} xl={6}>
                  <TimeGraph
                    graph={g}
                    variable={variable}
                    handleDeleteChart={handleRemoveGrahp}
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
