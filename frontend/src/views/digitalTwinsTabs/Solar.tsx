import { Container, Alert, Box, Grid } from '@mui/material';
import { useState } from 'react';
import SolarParams from '../../components/models/solar/SolarParams';
import {
  CUSTOM_SOLAR_PANEL,
  SOLAR_DIAGRAM_VARIABLES,
  SolarPanelParameters,
} from '../../types/models/solar';
import { setFormState } from '../../utils/setFormState';
import Iframe from 'react-iframe';
import Config from '../../config/config';
import TimeGraphs from '../../components/models/common/TimeGraphs';
import { GRAPH_TEST } from '../../types/graph';
import InputParams from '../../components/models/solar/InputParams';
import PlayerControls from '../../components/UI/PlayerControls';
import { useControlPlayer } from '../../hooks/useControlPlayer';
import Diagram from '../../components/UI/Diagram';
import solarDiagram from '../../assets/solarDiagram.svg';

type Props = {};

const Solar = (props: Props) => {
  const [solarModule, setSolarModule] =
    useState<SolarPanelParameters>(CUSTOM_SOLAR_PANEL);

  const [data, isPlaying, error, onPlay, onPause, onStop] = useControlPlayer<
    SolarPanelParameters,
    string
  >('solar', solarModule);

  const handleChange = (e: any, variableName?: string) => {
    const newState = setFormState<SolarPanelParameters>(
      e,
      solarModule,
      variableName
    );
    if (newState) {
      setSolarModule(newState);
    }
  };

  return (
    <Container maxWidth="xl">
      {error !== '' && isPlaying && (
        <Alert severity="error" variant="filled">
          {error}
        </Alert>
      )}
      {data !== undefined && isPlaying && (
        <Alert severity="info" variant="filled"></Alert>
      )}
      <Box display="flex" justifyContent="center" alignItems="center">
        <h2>Parámetros del sistema</h2>
      </Box>
      <Grid container spacing={2}>
        <Grid item xs={12} md={8} xl={8}>
          <SolarParams
            solarModule={solarModule}
            handleChange={handleChange}
          ></SolarParams>
        </Grid>
        <Grid item xs={12} md={4} xl={4}>
          <Iframe
            styles={{
              width: '100%',
              height: '100%',
            }}
            url={Config.getInstance().params.windyUrl}
          ></Iframe>
        </Grid>

        <Grid item xs={12} md={12} xl={12}>
          <Grid container spacing={2} margin={'normal'}>
            <Grid item xs={12} md={3} xl={3}>
              <InputParams
                solarModule={solarModule}
                handleChange={handleChange}
              ></InputParams>
            </Grid>
            <Grid item xs={12} md={9} xl={9}>
              <PlayerControls
                onPlay={onPlay}
                onPause={onPause}
                onStop={onStop}
              ></PlayerControls>
              <Diagram
                diagram={solarDiagram}
                variables={SOLAR_DIAGRAM_VARIABLES}
                width={800}
                height={400}
              ></Diagram>
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

export default Solar;
