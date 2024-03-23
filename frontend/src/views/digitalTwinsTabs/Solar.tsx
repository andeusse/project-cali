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
  SolarPanelParameters,
  SolarPanelModulesType,
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
    useState<SolarPanelParameters>(SOLAR_PANEL);

  const [, graphs, isPlaying, error, onPlay, onPause, onStop] =
    useControlPlayer<SolarPanelParameters, String>('solar', solarModule);

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
              onChange={handleChange}
            />
          </FormControl>
        </Grid>
        <Grid item xs={12} md={8} xl={8}>
          <Grid container spacing={2}>
            <Grid item xs={12} md={6} xl={6}>
              <FormControl fullWidth>
                <InputLabel id="solar-type">Tipo de módulo</InputLabel>
                <Select
                  labelId="solar-type"
                  label="Tipo de módulo"
                  value={solarModule.panelType}
                  name="panelType"
                  onChange={(e: any) => handleChange(e)}
                >
                  {Object.keys(SolarPanelModulesType).map((key) => (
                    <MenuItem key={key} value={key}>
                      {getValueByKey(SolarPanelModulesType, key)}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={6} md={3} xl={3}>
              <CustomNumberField
                variable={solarModule.moduleNumber}
                name="moduleNumber"
                handleChange={handleChange}
              ></CustomNumberField>
            </Grid>
            <Grid item xs={6} md={3} xl={3}>
              <CustomNumberField
                variable={solarModule.modulePeakPower}
                name="modulePeakPower"
                handleChange={handleChange}
              ></CustomNumberField>
            </Grid>
            <Grid item xs={6} md={3} xl={3}>
              <CustomNumberField
                variable={solarModule.moduleReductionPowerFactor}
                name="moduleReductionPowerFactor"
                handleChange={handleChange}
              ></CustomNumberField>
            </Grid>
            <Grid item xs={6} md={3} xl={3}>
              <CustomNumberField
                variable={solarModule.moduleEfficiency}
                name="moduleEfficiency"
                handleChange={handleChange}
              ></CustomNumberField>
            </Grid>
            <Grid item xs={6} md={3} xl={3}>
              <CustomNumberField
                variable={solarModule.moduleStandardTestIrradiation}
                name="moduleStandardTestIrradiation"
                handleChange={handleChange}
              ></CustomNumberField>
            </Grid>
            <Grid item xs={6} md={3} xl={3}>
              <CustomNumberField
                variable={solarModule.moduleStantardTestTemperature}
                name="moduleStantardTestTemperature"
                handleChange={handleChange}
              ></CustomNumberField>
            </Grid>
            <Grid item xs={6} md={3} xl={3}>
              <CustomNumberField
                variable={solarModule.moduleStandardIrradiation}
                name="moduleStandardIrradiation"
                handleChange={handleChange}
              ></CustomNumberField>
            </Grid>
            <Grid item xs={6} md={3} xl={3}>
              <CustomNumberField
                variable={solarModule.moduleStandardTemperature}
                name="moduleStandardTemperature"
                handleChange={handleChange}
              ></CustomNumberField>
            </Grid>
            <Grid item xs={6} md={3} xl={3}>
              <CustomNumberField
                variable={solarModule.moduleEnvironmentTemperature}
                name="moduleEnvironmentTemperature"
                handleChange={handleChange}
              ></CustomNumberField>
            </Grid>
            <Grid item xs={6} md={3} xl={3}>
              <CustomNumberField
                variable={solarModule.moduleCoefficientPowerVariation}
                name="moduleCoefficientPowerVariation"
                handleChange={handleChange}
              ></CustomNumberField>
            </Grid>
          </Grid>
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
          <Grid container spacing={2}>
            <Grid item xs={12} md={3} xl={3}>
              <Grid container spacing={2}>
                <Grid item xs={12} md={12} xl={12}>
                  <h2>Operación planta</h2>
                </Grid>
                <Grid item xs={12} md={12} xl={12}>
                  <FormControlLabel
                    control={
                      <Switch
                        checked={solarModule.inputOfflineOperation}
                        name="inputOfflineOperation"
                        onChange={(e: any) => handleChange(e)}
                        color="default"
                      />
                    }
                    label="Operación offline"
                  />
                </Grid>
                <Grid item xs={12} md={12} xl={12}>
                  <h3>Entradas</h3>
                </Grid>
                <Grid item xs={12} md={12} xl={12}>
                  <h3>Parámetros turbina</h3>
                </Grid>
                <Grid item xs={12} md={12} xl={12}>
                  <ToggleCustomNumberField
                    variable={solarModule.inputIrradiation}
                    name="inputIrradiation"
                    handleChange={handleChange}
                    offlineOperation={solarModule.inputOfflineOperation}
                  ></ToggleCustomNumberField>
                </Grid>
                <Grid item xs={12} md={12} xl={12}>
                  <ToggleCustomNumberField
                    variable={solarModule.inputTemperature}
                    name="inputTemperature"
                    handleChange={handleChange}
                    offlineOperation={solarModule.inputOfflineOperation}
                  ></ToggleCustomNumberField>
                </Grid>
              </Grid>
            </Grid>
            <Grid item xs={12} md={9} xl={9}>
              {playerControl}
              <Diagram<{}>
                diagram={solarDiagram}
                data={{}}
                variables={SOLAR_DIAGRAM_VARIABLES}
                width={800}
                height={400}
              ></Diagram>
            </Grid>
          </Grid>
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
        )}
      </Grid>
    </>
  );
};

export default Solar;
