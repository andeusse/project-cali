import { Alert, Box, Container, Grid } from '@mui/material';
import TurbineParams from '../../components/models/turbine/TurbineParams';
import { useCallback, useEffect, useState } from 'react';
import { TURBINE, TurbineParameters } from '../../types/models/turbine';
import ControllerParams from '../../components/models/turbine/ControllerParams';
import BatteryParams from '../../components/models/turbine/BatteryParams';
import InverterParams from '../../components/models/turbine/InverterParams';
import TimeGraphs from '../../components/models/common/TimeGraphs';
import { GRAPH_TEST } from '../../types/graph';
import InputParams from '../../components/models/turbine/InputParams';
import PlayerControls from '../../components/UI/PlayerControls';
import { setFormState } from '../../utils/setFormState';
import Diagram from '../../components/UI/Diagram';
import { updateModel } from '../../api/digitalTwinsModels';
import { AxiosError } from 'axios';

type Props = {};

const Turbine = (props: Props) => {
  const [turbine, setUserTurbine] = useState<TurbineParameters>(TURBINE);

  const [isPlaying, setIsPlaying] = useState(false);

  const [error, setError] = useState('');

  const queryApi = useCallback(() => {
    updateModel<TurbineParameters, string>('turbine', turbine)
      .then((resp) => {
        setError('');
      })
      .catch((err: AxiosError) => {
        setError(`Error al realizar la consulta con el mesaje: ${err.message}`);
      })
      .finally(() => {});
  }, [turbine]);

  useEffect(() => {
    const interval: NodeJS.Timer = setInterval(() => {
      if (isPlaying) {
        queryApi();
      }
    }, 5000);
    return () => {
      clearInterval(interval);
    };
  }, [isPlaying, queryApi, turbine]);

  const onPlay = () => {
    queryApi();
    setIsPlaying(true);
  };

  const onPause = () => {
    setIsPlaying(false);
    setError('');
  };

  const onStop = () => {
    setIsPlaying(false);
    setError('');
  };

  const handleChange = (e: any, variableName?: string) => {
    const newState = setFormState<TurbineParameters>(e, turbine, variableName);
    if (newState) {
      setUserTurbine(newState);
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
              <Diagram turbineType={turbine.turbineType}></Diagram>
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
