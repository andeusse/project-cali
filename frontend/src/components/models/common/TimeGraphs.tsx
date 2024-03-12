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
import { DiagramVariableType } from '../../../types/models/common';

type Props = {
  graphs: GraphType[];
  variables: DiagramVariableType[];
};

const marks = [
  {
    value: 1,
    label: '1',
  },
  {
    value: 10,
    label: '10',
  },
];

const TimeGraphs = (props: Props) => {
  const { graphs, variables } = props;

  const [availableGraphs, setAvailableGraphs] = useState([...graphs]);

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
    <div>
      <h2>Gráficas de tiempo</h2>
      <Grid container spacing={2}>
        <Grid item xs={12} md={2} xl={2}>
          <Typography id="input-slider" gutterBottom>
            Multiplicador de velocidad:
          </Typography>
          <Slider
            aria-label="TimeMultiplier"
            defaultValue={1}
            valueLabelDisplay="auto"
            step={1}
            marks={marks}
            min={1}
            max={10}
          />
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
          <Grid container spacing={2}>
            {currentGraphs.map((g, index) => {
              return (
                <Grid key={`${index}_${g}`} item xs={12} md={6} xl={6}>
                  <TimeGraph
                    graph={g}
                    title={
                      variables.find((v) => g.variable === v.variable)?.name
                    }
                    handleDeleteChart={handleRemoveGrahp}
                  ></TimeGraph>
                </Grid>
              );
            })}
          </Grid>
        </Grid>
      </Grid>
    </div>
  );
};

export default TimeGraphs;
