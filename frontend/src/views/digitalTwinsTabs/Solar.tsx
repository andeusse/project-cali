import {
  Alert,
  Box,
  Grid,
  FormControl,
  TextField,
  FormControlLabel,
  Switch,
  InputLabel,
  MenuItem,
  Select,
} from '@mui/material';
import { useState } from 'react';
import {
  SOLAR_PANEL,
  SOLAR_DIAGRAM_VARIABLES,
  SolarWindParameters,
} from '../../types/models/solar';
import { setFormState } from '../../utils/setFormState';
import Iframe from 'react-iframe';
import Config from '../../config/config';
import TimeGraphs from '../../components/models/common/TimeGraphs';
import PlayerControls from '../../components/UI/PlayerControls';
import { useControlPlayer } from '../../hooks/useControlPlayer';
import Diagram from '../../components/UI/Diagram';
import solarDiagram from '../../assets/solarDiagram.svg';
import ToggleCustomNumberField from '../../components/UI/ToggleCustomNumberField';
import CustomNumberField from '../../components/UI/CustomNumberField';
import { getValueByKey } from '../../utils/getValueByKey';

type Props = {};

const Solar = (props: Props) => {
  const [solarModule, setSolarModule] =
    useState<SolarWindParameters>(SOLAR_PANEL);

  const [, graphs, isPlaying, error, onPlay, onPause, onStop] =
    useControlPlayer<SolarWindParameters, String>('solar', solarModule);

  const handleChange = (e: any, variableName?: string) => {
    const newState = setFormState<SolarWindParameters>(
      e,
      solarModule,
      variableName
    );
    if (newState) {
      setSolarModule(newState as SolarWindParameters);
    }
  };

  const playerControl = (
    <PlayerControls
      isPlaying={isPlaying}
      onPlay={onPlay}
      onPause={onPause}
      onStop={onStop}
    ></PlayerControls>
  );

  return (
    <>
      {error !== '' && isPlaying && (
        <Alert severity="error" variant="filled">
          {error}
        </Alert>
      )}
      <Box display="flex" justifyContent="center" alignItems="center">
        <h2>Parámetros del sistema</h2>
      </Box>
      <Grid container spacing={2}>
        <Grid item xs={12} md={12} xl={12}>
          <FormControl fullWidth>
            <TextField
              label="Nombre"
              value={solarModule.name}
              name="name"
              autoComplete="off"
              onChange={handleChange}
            />
          </FormControl>
        </Grid>

        {/* <Grid item xs={12} md={4} xl={4}>
          <Iframe
            styles={{
              width: '100%',
              height: '100%',
            }}
            url={Config.getInstance().params.windyUrl}
          ></Iframe>
        </Grid> */}
        {/* <Grid item xs={12} md={9} xl={9}>
          {playerControl}
          <Diagram<{}>
            diagram={solarDiagram}
            data={{}}
            variables={SOLAR_DIAGRAM_VARIABLES}
            width={800}
            height={400}
          ></Diagram>
        </Grid>
        {graphs !== undefined && solarModule.timeMultiplier && (
          <>
            <Grid item xs={12} md={12} xl={12}>
              <TimeGraphs
                timeMultiplier={solarModule.timeMultiplier}
                handleChange={handleChange}
                graphs={graphs}
                variables={SOLAR_DIAGRAM_VARIABLES}
                playerControl={playerControl}
                isPlaying={isPlaying}
              ></TimeGraphs>
            </Grid>
          </>
        )} */}
      </Grid>
    </>
  );
};

export default Solar;
