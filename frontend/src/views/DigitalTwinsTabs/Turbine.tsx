import { Box, Container, Grid } from '@mui/material';
import TurbineParams from '../../components/models/turbine/TurbineParams';
import { useState } from 'react';
import { TURBINE, TurbineParameters } from '../../types/models/turbine';
import ControllerParams from '../../components/models/turbine/ControllerParams';
import BatteryParams from '../../components/models/turbine/BatteryParams';
import InverterParams from '../../components/models/turbine/InverterParams';
import TimeGraphs from '../../components/models/common/TimeGraphs';
import { GRAPH_TEST } from '../../types/graph';
import InputParams from '../../components/models/turbine/InputParams';
import PlayerControls from '../../components/UI/PlayerControls';
import { setFormState } from '../../utils/setFormState';

type Props = {};

const Turbine = (props: Props) => {
  const [userTurbine, setUserTurbine] = useState<TurbineParameters>(TURBINE);

  const onPlay = () => {};

  const onPause = () => {};

  const onStop = () => {};

  const handleChange = (e: any, variableName?: string) => {
    const newState = setFormState<TurbineParameters>(
      e,
      userTurbine,
      variableName
    );
    console.log(newState);

    if (newState) {
      setUserTurbine(newState);
    }
  };

  return (
    <Container maxWidth="xl">
      <Box display="flex" justifyContent="center" alignItems="center">
        <h2>Parámetros del sistema</h2>
      </Box>
      <Grid container spacing={2}>
        <Grid item xs={12} md={6} xl={3.5}>
          <TurbineParams
            selectedTurbine={userTurbine.turbineType}
            handleChange={handleChange}
          ></TurbineParams>
        </Grid>
        <Grid item xs={12} md={6} xl={3.5}>
          <ControllerParams
            turbine={userTurbine}
            handleChange={handleChange}
          ></ControllerParams>
        </Grid>
        <Grid item xs={12} md={6} xl={3.5}>
          <BatteryParams
            turbine={userTurbine}
            handleChange={handleChange}
          ></BatteryParams>
        </Grid>
        <Grid item xs={12} md={6} xl={1.5}>
          <InverterParams
            turbine={userTurbine}
            handleChange={handleChange}
          ></InverterParams>
        </Grid>
        <Grid item xs={12} md={12} xl={12}>
          <Grid container spacing={2} margin={'normal'}>
            <Grid item xs={12} md={2} xl={2}>
              <InputParams
                turbine={userTurbine}
                handleChange={handleChange}
              ></InputParams>
            </Grid>
            <Grid item xs={12} md={10} xl={10}>
              <PlayerControls
                onPlay={onPlay}
                onPause={onPause}
                onStop={onStop}
              ></PlayerControls>
            </Grid>
          </Grid>
        </Grid>
        <Grid item xs={12} md={12} xl={12}>
          <TimeGraphs graphs={GRAPH_TEST}></TimeGraphs>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Turbine;
