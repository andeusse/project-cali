import {
  Alert,
  Box,
  Container,
  FormControl,
  Grid,
  TextField,
} from '@mui/material';
import TurbineParams from '../../components/models/turbine/TurbineParams';
import { useEffect, useState } from 'react';
import {
  TURBINE,
  TURBINE_DIAGRAM_VARIABLES,
  TurbineOutput,
  TurbineParameters,
  TurbineType,
} from '../../types/models/turbine';
import ControllerParams from '../../components/models/turbine/ControllerParams';
import BatteryParams from '../../components/models/turbine/BatteryParams';
import InverterParams from '../../components/models/turbine/InverterParams';
import TimeGraphs from '../../components/models/common/TimeGraphs';
import InputParams from '../../components/models/turbine/InputParams';
import PlayerControls from '../../components/UI/PlayerControls';
import { setFormState } from '../../utils/setFormState';
import Diagram from '../../components/UI/Diagram';
import { useControlPlayer } from '../../hooks/useControlPlayer';
import peltonDiagram from '../../assets/peltonTurbineDiagram.svg';
import turgoDiagram from '../../assets/turgoTurbineDiagram.svg';

type Props = {};

const Turbine = (props: Props) => {
  const [turbine, setTurbine] = useState<TurbineParameters>(TURBINE);

  const [data, graphs, isPlaying, error, onPlay, onPause, onStop] =
    useControlPlayer<TurbineParameters, TurbineOutput>('turbine', turbine);

  useEffect(() => {
    if (data !== undefined) {
      setTurbine((o) => ({
        ...o,
        simulatedBatteryStateOfCharge: data.batteryStateOfCharge,
        simulatedDirectCurrentVoltage: data.directCurrentVoltage,
      }));
    } else {
      setTurbine((o) => ({
        ...o,
        simulatedBatteryStateOfCharge: undefined,
        simulatedDirectCurrentVoltage: undefined,
      }));
    }
  }, [data]);

  const handleChange = (e: any, variableName?: string) => {
    const newState = setFormState<TurbineParameters>(e, turbine, variableName);
    if (newState) {
      setTurbine(newState);
    }
  };

  return (
    <Container maxWidth="xl">
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
              value={turbine.name}
              name="name"
              onChange={handleChange}
            />
          </FormControl>
        </Grid>
        <Grid item xs={12} md={6} xl={3.5}>
          <TurbineParams
            selectedTurbine={turbine.turbineType}
            handleChange={handleChange}
          ></TurbineParams>
        </Grid>
        <Grid item xs={12} md={6} xl={3.5}>
          <ControllerParams
            turbine={turbine}
            handleChange={handleChange}
          ></ControllerParams>
        </Grid>
        <Grid item xs={12} md={6} xl={3.5}>
          <BatteryParams
            turbine={turbine}
            handleChange={handleChange}
          ></BatteryParams>
        </Grid>
        <Grid item xs={12} md={6} xl={1.5}>
          <InverterParams
            turbine={turbine}
            handleChange={handleChange}
          ></InverterParams>
        </Grid>
        <Grid item xs={12} md={12} xl={12}>
          <Grid container spacing={2} margin={'normal'}>
            <Grid item xs={12} md={3} xl={3}>
              <InputParams
                turbine={turbine}
                handleChange={handleChange}
              ></InputParams>
            </Grid>
            <Grid item xs={12} md={9} xl={9}>
              <PlayerControls
                onPlay={onPlay}
                onPause={onPause}
                onStop={onStop}
              ></PlayerControls>
              <Diagram<TurbineOutput>
                diagram={
                  turbine.turbineType === TurbineType.Pelton
                    ? peltonDiagram
                    : turgoDiagram
                }
                data={data}
                variables={TURBINE_DIAGRAM_VARIABLES}
                width={800}
                height={800}
              ></Diagram>
            </Grid>
          </Grid>
        </Grid>
        <Grid item xs={12} md={12} xl={12}>
          {graphs !== undefined && (
            <TimeGraphs
              graphs={graphs}
              variables={TURBINE_DIAGRAM_VARIABLES}
            ></TimeGraphs>
          )}
        </Grid>
      </Grid>
    </Container>
  );
};

export default Turbine;
