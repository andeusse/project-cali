import { Box, Container, Grid } from '@mui/material';
import TurbineParams from '../../components/models/turbine/TurbineParams';
import { useState } from 'react';
import { TURBINE, turbine } from '../../types/models/turbine';
import ControllerParams from '../../components/models/turbine/ControllerParams';
import BatteryParams from '../../components/models/turbine/BatteryParams';
import InverterParams from '../../components/models/turbine/InverterParams';
import TimeGraphs from '../../components/models/common/TimeGraphs';
import { GRAPH_TEST } from '../../types/graph';

type Props = {};

const Turbine = (props: Props) => {
  const [userTurbine, setUserTurbine] = useState<turbine>(TURBINE);

  const handleChange = (e: any) => {
    if (
      e.target.type === 'checkbox' &&
      e.target.name === 'controllerCustomize'
    ) {
      setUserTurbine((oldState) => {
        let newState = { ...oldState };
        newState.controllerCustomize = e.target.checked;
        newState.controllerChargeVoltageBulk.disabled = !e.target.checked;
        newState.controllerChargeVoltageFloat.disabled = !e.target.checked;
        newState.controllerChargingMinimunVoltage.disabled = !e.target.checked;
        newState.controllerDissipatorOffVoltage.disabled = !e.target.checked;
        newState.controllerDissipatorOnVoltage.disabled = !e.target.checked;
        return newState;
      });
    } else if (
      typeof userTurbine[e.target.name as keyof turbine] === 'object'
    ) {
      setUserTurbine({
        ...userTurbine,
        [e.target.name]: {
          ...(userTurbine[e.target.name as keyof turbine] as object),
          value: e.target.value,
        },
      });
    } else {
      setUserTurbine({ ...userTurbine, [e.target.name]: e.target.value });
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
          <TimeGraphs graphs={GRAPH_TEST}></TimeGraphs>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Turbine;
