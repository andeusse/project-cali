import {
  Alert,
  Box,
  Container,
  FormControl,
  FormControlLabel,
  Grid,
  InputLabel,
  MenuItem,
  Select,
  Switch,
  TextField,
} from '@mui/material';
import { useEffect, useState } from 'react';
import {
  ControllerStateType,
  PELTON_TURBINE,
  TURBINE,
  TURBINE_DIAGRAM_VARIABLES,
  TURGO_TURBINE,
  TurbineOutput,
  TurbineParameters,
  TurbineType,
} from '../../types/models/turbine';
import TimeGraphs from '../../components/models/common/TimeGraphs';
import PlayerControls from '../../components/UI/PlayerControls';
import { setFormState } from '../../utils/setFormState';
import Diagram from '../../components/UI/Diagram';
import { useControlPlayer } from '../../hooks/useControlPlayer';
import peltonDiagram from '../../assets/peltonTurbineDiagram.svg';
import turgoDiagram from '../../assets/turgoTurbineDiagram.svg';
import turgoDiagramNoCharge from '../../assets/turgoNoChargeDiagram.svg';
import CustomNumberField from '../../components/UI/CustomNumberField';
import ToggleCustomNumberField from '../../components/UI/ToggleCustomNumberField';

type Props = {};

const Turbine = (props: Props) => {
  const [turbine, setTurbine] = useState<TurbineParameters>(TURBINE);

  const [data, graphs, isPlaying, error, onPlay, onPause, onStop] =
    useControlPlayer<TurbineParameters, TurbineOutput>('turbine', turbine);

  useEffect(() => {
    if (data !== undefined) {
      setTurbine((o) => ({
        ...o,
        inputPressure: {
          ...o.inputPressure,
          value: data.inputPressure
            ? data.inputPressure
            : o.inputPressure.value,
        },
        inputFlow: {
          ...o.inputFlow,
          value: data.inputFlow ? data.inputFlow : o.inputFlow.value,
        },
        inputActivePower: {
          ...o.inputActivePower,
          value: data.inputActivePower
            ? data.inputActivePower
            : o.inputActivePower.value,
        },
        inputPowerFactor: {
          ...o.inputPowerFactor,
          value: data.inputPowerFactor
            ? data.inputPowerFactor
            : o.inputPowerFactor.value,
        },
        simulatedBatteryStateOfCharge: data.batteryStateOfCharge,
        simulatedDirectCurrentVoltage: data.directCurrentVoltage,
        simulatedInverterState: data.inverterState,
        simulatedSinkLoadState: data.sinkLoadState,
      }));
    } else {
      setTurbine((o) => ({
        ...o,
        simulatedBatteryStateOfCharge: undefined,
        simulatedDirectCurrentVoltage: undefined,
        simulatedInverterState: undefined,
        simulatedSinkLoadState: undefined,
      }));
    }
  }, [data]);

  const handleChange = (e: any, variableName?: string) => {
    const newState = setFormState<TurbineParameters>(e, turbine, variableName);
    if (newState) {
      setTurbine(newState);
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
              value={turbine.name}
              name="name"
              onChange={handleChange}
            />
          </FormControl>
        </Grid>
        <Grid item xs={12} md={6} xl={3.5}>
          <h3>Turbinas</h3>
          <Grid container spacing={2}>
            <Grid item xs={12} md={12} xl={12}>
              <FormControl fullWidth>
                <InputLabel id="turbine-type">Tipo de turbina</InputLabel>
                <Select
                  labelId="turbine-type"
                  label="Tipo de turbina"
                  value={turbine.turbineType}
                  name="turbineType"
                  onChange={(e: any) => handleChange(e)}
                >
                  {Object.keys(TurbineType).map((key) => (
                    <MenuItem key={key} value={key}>
                      {key}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            {turbine.turbineType === TurbineType.Pelton &&
              PELTON_TURBINE.map((variable) => (
                <Grid
                  key={variable.variableString + variable.variableSubString}
                  item
                  xs={6}
                  md={6}
                  xl={6}
                >
                  <CustomNumberField variable={variable}></CustomNumberField>
                </Grid>
              ))}
            {turbine.turbineType === TurbineType.Turgo &&
              TURGO_TURBINE.map((variable) => (
                <Grid
                  key={variable.variableString + variable.variableSubString}
                  item
                  xs={6}
                  md={6}
                  xl={6}
                >
                  <CustomNumberField variable={variable}></CustomNumberField>
                </Grid>
              ))}
          </Grid>
        </Grid>
        <Grid item xs={12} md={6} xl={3.5}>
          <h3>Controlador de carga</h3>
          <Grid container spacing={2}>
            <Grid item xs={6} md={6} xl={6}>
              <FormControl fullWidth>
                <InputLabel>Estado inicial disipación</InputLabel>
                <Select
                  label="Estado inicial disipación"
                  value={turbine.sinkLoadInitialState}
                  name="sinkLoadInitialState"
                  onChange={(e: any) => handleChange(e)}
                >
                  {Object.keys(ControllerStateType).map((key) => (
                    <MenuItem key={key} value={key}>
                      {key}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={6} md={6} xl={6} sx={{ alignContent: 'center' }}>
              <FormControlLabel
                control={
                  <Switch
                    checked={turbine.controllerCustomize}
                    name="controllerCustomize"
                    onChange={(e: any) => handleChange(e)}
                    color="default"
                  />
                }
                label={turbine.controllerCustomize ? 'Manual' : 'Auto'}
              />
            </Grid>
            <Grid item xs={6} md={6} xl={6}>
              <CustomNumberField
                variable={turbine.controllerEfficiency}
                name="controllerEfficiency"
              ></CustomNumberField>
            </Grid>
            <Grid item xs={6} md={6} xl={6}>
              <CustomNumberField
                variable={turbine.controllerChargeVoltageBulk}
                name="controllerChargeVoltageBulk"
                handleChange={handleChange}
              ></CustomNumberField>
            </Grid>
            <Grid item xs={6} md={6} xl={6}>
              <CustomNumberField
                variable={turbine.controllerChargeVoltageFloat}
                name="controllerChargeVoltageFloat"
                handleChange={handleChange}
              ></CustomNumberField>
            </Grid>
            <Grid item xs={6} md={6} xl={6}>
              <CustomNumberField
                variable={turbine.controllerChargingMinimunVoltage}
                name="controllerChargingMinimunVoltage"
                handleChange={handleChange}
              ></CustomNumberField>
            </Grid>
            <Grid item xs={6} md={6} xl={6}>
              <CustomNumberField
                variable={turbine.controllerSinkOffVoltage}
                name="controllerSinkOffVoltage"
                handleChange={handleChange}
              ></CustomNumberField>
            </Grid>
            <Grid item xs={6} md={6} xl={6}>
              <CustomNumberField
                variable={turbine.controllerSinkOnVoltage}
                name="controllerSinkOnVoltage"
                handleChange={handleChange}
              ></CustomNumberField>
            </Grid>
          </Grid>
        </Grid>
        <Grid item xs={12} md={6} xl={3.5}>
          <h3>Baterías</h3>
          <Grid container spacing={2}>
            <Grid item xs={6} md={6} xl={6}>
              <CustomNumberField
                variable={turbine.batteryStateOfCharge}
                name="batteryStateOfCharge"
                handleChange={handleChange}
              ></CustomNumberField>
            </Grid>
            <Grid item xs={6} md={6} xl={6}>
              <CustomNumberField
                variable={turbine.batteryTemperatureCoefficient}
                name="batteryTemperatureCoefficient"
              ></CustomNumberField>
            </Grid>
            <Grid item xs={6} md={6} xl={6}>
              <CustomNumberField
                variable={turbine.batteryCapacity}
                name="batteryCapacity"
              ></CustomNumberField>
            </Grid>
            <Grid item xs={6} md={6} xl={6}>
              <CustomNumberField
                variable={turbine.batterySelfDischargeCoefficient}
                name="batterySelfDischargeCoefficient"
              ></CustomNumberField>
            </Grid>
            <Grid item xs={6} md={6} xl={6}>
              <CustomNumberField
                variable={turbine.batteryChargeDischargeEfficiency}
                name="batteryChargeDischargeEfficiency"
              ></CustomNumberField>
            </Grid>
            <Grid item xs={6} md={6} xl={6}>
              <CustomNumberField
                variable={turbine.batteryTemperatureCompensationCoefficient}
                name="batteryTemperatureCompensationCoefficient"
              ></CustomNumberField>
            </Grid>
          </Grid>
        </Grid>
        <Grid item xs={12} md={6} xl={1.5}>
          <h3>Inversor</h3>
          <Grid container spacing={2}>
            <Grid item xs={12} md={12} xl={12}>
              <CustomNumberField
                variable={turbine.inverterEfficiency}
                name="inverterEfficiency"
                handleChange={handleChange}
              ></CustomNumberField>
            </Grid>
            <Grid item xs={12} md={12} xl={12}>
              <CustomNumberField
                variable={turbine.inverterNominalPower}
                name="inverterNominalPower"
                handleChange={handleChange}
              ></CustomNumberField>
            </Grid>
          </Grid>
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
                        checked={turbine.inputOfflineOperation}
                        name="inputOfflineOperation"
                        onChange={(e: any) => handleChange(e)}
                        color="default"
                      />
                    }
                    label={turbine.inputOfflineOperation ? 'Offline' : 'Online'}
                  />
                </Grid>
                <Grid item xs={12} md={12} xl={12}>
                  <h3>Parámetros turbina</h3>
                </Grid>
                <Grid item xs={12} md={12} xl={12}>
                  <ToggleCustomNumberField
                    variable={turbine.inputPressure}
                    name="inputPressure"
                    handleChange={handleChange}
                    offlineOperation={turbine.inputOfflineOperation}
                  ></ToggleCustomNumberField>
                </Grid>
                <Grid item xs={12} md={12} xl={12}>
                  <ToggleCustomNumberField
                    variable={turbine.inputFlow}
                    name="inputFlow"
                    handleChange={handleChange}
                    offlineOperation={turbine.inputOfflineOperation}
                  ></ToggleCustomNumberField>
                </Grid>
                {turbine.turbineType === TurbineType.Turgo && (
                  <>
                    <Grid item xs={12} md={12} xl={12}>
                      <h3>Parámetros carga CD</h3>
                    </Grid>
                    <FormControlLabel
                      control={
                        <Switch
                          checked={turbine.inputDirectCurrentPower}
                          name="inputDirectCurrentPower"
                          onChange={(e) => {
                            if (handleChange) {
                              handleChange(e);
                            }
                          }}
                          color="default"
                        />
                      }
                      label={
                        turbine.inputDirectCurrentPower
                          ? 'Conectado: 2.4 W'
                          : 'Desconectado: 0.0 W'
                      }
                    />
                  </>
                )}
                <Grid item xs={12} md={12} xl={12}>
                  <h3>Parámetros carga CA</h3>
                </Grid>
                <Grid item xs={12} md={12} xl={12}>
                  <ToggleCustomNumberField
                    variable={turbine.inputActivePower}
                    name="inputActivePower"
                    handleChange={handleChange}
                    offlineOperation={turbine.inputOfflineOperation}
                  ></ToggleCustomNumberField>
                </Grid>
                <Grid item xs={12} md={12} xl={12}>
                  <ToggleCustomNumberField
                    variable={turbine.inputPowerFactor}
                    name="inputPowerFactor"
                    handleChange={handleChange}
                    offlineOperation={turbine.inputOfflineOperation}
                  ></ToggleCustomNumberField>
                </Grid>
              </Grid>
            </Grid>
            <Grid item xs={12} md={9} xl={9}>
              {playerControl}
              <Diagram<TurbineOutput>
                diagram={
                  turbine.turbineType === TurbineType.Pelton
                    ? peltonDiagram
                    : turbine.inputDirectCurrentPower
                    ? turgoDiagram
                    : turgoDiagramNoCharge
                }
                data={data}
                variables={TURBINE_DIAGRAM_VARIABLES}
                width={800}
                height={800}
              ></Diagram>
            </Grid>
          </Grid>
        </Grid>
        {graphs !== undefined && turbine.timeMultiplier && (
          <>
            <Grid item xs={12} md={12} xl={12}>
              <TimeGraphs
                timeMultiplier={turbine.timeMultiplier}
                handleChange={handleChange}
                graphs={graphs}
                variables={TURBINE_DIAGRAM_VARIABLES}
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

export default Turbine;
