import {
  Accordion,
  AccordionDetails,
  AccordionSummary,
  FormControl,
  Grid,
  InputLabel,
  MenuItem,
  Select,
  TextField,
  Typography,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { useEffect, useState } from 'react';
import {
  ControllerStateType,
  PELTON_TURBINE,
  TURBINE,
  PELTON_TURBINE_DIAGRAM_VARIABLES,
  TURGO_TURBINE,
  TurbineOutput,
  TurbineParameters,
  TurbineType,
  TURGO_TURBINE_DIAGRAM_VARIABLES,
} from '../../types/models/turbine';
import TimeGraphs from '../../components/models/common/TimeGraphs';
import PlayerControls from '../../components/UI/PlayerControls';
import { setFormState } from '../../utils/setFormState';
import { useControlPlayer } from '../../hooks/useControlPlayer';
import CustomNumberField from '../../components/UI/CustomNumberField';
import ToggleCustomNumberField from '../../components/UI/ToggleCustomNumberField';
import Battery from '../../components/models/Battery';
import CustomToggle from '../../components/UI/CustomToggle';

import turbineIllustration from '../../assets/illustrations/turbine.jpg';
import TurbineDiagram from '../../components/models/diagram/TurbineDiagram';
import ErrorDialog from '../../components/UI/ErrorDialog';

type Props = {};

const Turbine = (props: Props) => {
  const [system, setSystem] = useState<TurbineParameters>({ ...TURBINE });
  const [isImageExpanded, setIsImageExpanded] = useState(true);
  const [isParametersExpanded, setIsParametersExpanded] = useState(true);
  const [isOpen, setIsOpen] = useState(false);

  const [data, graphs, isPlaying, error, onPlay, onPause, onStop] =
    useControlPlayer<TurbineParameters, TurbineOutput>('turbine', system);

  useEffect(() => {
    setSystem((o) => {
      return { ...o, disableParameters: isPlaying };
    });
  }, [isPlaying]);

  useEffect(() => {
    if (error !== '') {
      setIsOpen(true);
    }
  }, [error]);

  useEffect(() => {
    if (data !== undefined) {
      setSystem((o) => ({
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
      setSystem((o) => ({
        ...o,
        simulatedBatteryStateOfCharge: undefined,
        simulatedDirectCurrentVoltage: undefined,
        simulatedInverterState: undefined,
        simulatedSinkLoadState: undefined,
      }));
    }
  }, [data]);

  const handleChange = (e: any, variableName?: string) => {
    const newState = setFormState<TurbineParameters>(e, system, variableName);
    if (newState) {
      setSystem(newState as TurbineParameters);
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
      <ErrorDialog
        isOpen={isOpen}
        setIsOpen={setIsOpen}
        error={error}
      ></ErrorDialog>
      <Grid container spacing={2}>
        <Grid item xs={12} md={12} xl={12}>
          <Accordion
            expanded={isImageExpanded}
            onChange={() => setIsImageExpanded(!isImageExpanded)}
          >
            <AccordionSummary
              expandIcon={<ExpandMoreIcon />}
              aria-controls="panel1-content"
              id="panel1-header"
              sx={{ margin: 0 }}
            >
              <Typography variant="h4">Sistema</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <img
                style={{
                  height: '500px',
                  display: 'block',
                  marginLeft: 'auto',
                  marginRight: 'auto',
                }}
                src={turbineIllustration}
                alt="turbineIllustration"
              ></img>
            </AccordionDetails>
          </Accordion>
        </Grid>
        <Grid item xs={12} md={12} xl={12}>
          <Accordion
            expanded={isParametersExpanded}
            onChange={() => setIsParametersExpanded(!isParametersExpanded)}
          >
            <AccordionSummary
              expandIcon={<ExpandMoreIcon />}
              aria-controls="panel2-content"
              id="panel2-header"
              sx={{ margin: 0 }}
            >
              <Typography variant="h4">Parámetros del sistema</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <Grid container spacing={2}>
                <Grid item xs={12} md={12} xl={12}>
                  <FormControl fullWidth>
                    <TextField
                      label="Nombre"
                      value={system.name}
                      name="name"
                      autoComplete="off"
                      onChange={handleChange}
                      disabled={system.disableParameters}
                    />
                  </FormControl>
                </Grid>
                <Grid item xs={12} md={6} xl={3.5}>
                  <h3>Turbina</h3>
                  <Grid container spacing={2}>
                    <Grid item xs={12} md={12} xl={12}>
                      <FormControl fullWidth>
                        <InputLabel id="turbine-type">
                          Tipo de turbina
                        </InputLabel>
                        <Select
                          labelId="turbine-type"
                          label="Tipo de turbina"
                          value={system.turbineType}
                          name="turbineType"
                          onChange={(e: any) => handleChange(e)}
                          disabled={system.disableParameters}
                        >
                          {Object.keys(TurbineType).map((key) => (
                            <MenuItem key={key} value={key}>
                              {key}
                            </MenuItem>
                          ))}
                        </Select>
                      </FormControl>
                    </Grid>
                    {system.turbineType === TurbineType.Pelton &&
                      PELTON_TURBINE.map((variable) => (
                        <Grid
                          key={
                            variable.variableString + variable.variableSubString
                          }
                          item
                          xs={6}
                          md={6}
                          xl={6}
                        >
                          <CustomNumberField
                            variable={variable}
                          ></CustomNumberField>
                        </Grid>
                      ))}
                    {system.turbineType === TurbineType.Turgo &&
                      TURGO_TURBINE.map((variable) => (
                        <Grid
                          key={
                            variable.variableString + variable.variableSubString
                          }
                          item
                          xs={6}
                          md={6}
                          xl={6}
                        >
                          <CustomNumberField
                            variable={variable}
                          ></CustomNumberField>
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
                          value={system.controller.sinkLoadInitialState}
                          name="controller.sinkLoadInitialState"
                          onChange={(e: any) => handleChange(e)}
                          disabled={system.disableParameters}
                        >
                          {Object.keys(ControllerStateType).map((key) => (
                            <MenuItem key={key} value={key}>
                              {key}
                            </MenuItem>
                          ))}
                        </Select>
                      </FormControl>
                    </Grid>
                    <Grid item xs={6} md={6} xl={6} alignContent={'center'}>
                      <CustomToggle
                        name="controller.customize"
                        value={system.controller.customize}
                        handleChange={handleChange}
                        disabled={system.disableParameters}
                      ></CustomToggle>
                    </Grid>
                    <Grid item xs={6} md={6} xl={6}>
                      <CustomNumberField
                        variable={system.controller.efficiency}
                        name="controller.efficiency"
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={6} md={6} xl={6}>
                      <CustomNumberField
                        variable={system.controller.chargeVoltageBulk}
                        name="controller.chargeVoltageBulk"
                        handleChange={handleChange}
                        disabled={system.disableParameters}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={6} md={6} xl={6}>
                      <CustomNumberField
                        variable={system.controller.chargeVoltageFloat}
                        name="controller.chargeVoltageFloat"
                        handleChange={handleChange}
                        disabled={system.disableParameters}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={6} md={6} xl={6}>
                      <CustomNumberField
                        variable={system.controller.chargingMinimunVoltage}
                        name="controller.chargingMinimunVoltage"
                        handleChange={handleChange}
                        disabled={system.disableParameters}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={6} md={6} xl={6}>
                      <CustomNumberField
                        variable={system.controller.sinkOffVoltage}
                        name="controller.sinkOffVoltage"
                        handleChange={handleChange}
                        disabled={system.disableParameters}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={6} md={6} xl={6}>
                      <CustomNumberField
                        variable={system.controller.sinkOnVoltage}
                        name="controller.sinkOnVoltage"
                        handleChange={handleChange}
                        disabled={system.disableParameters}
                      ></CustomNumberField>
                    </Grid>
                  </Grid>
                </Grid>
                <Grid item xs={12} md={6} xl={3.5}>
                  <h3>Baterías</h3>
                  <Battery
                    propertyName="battery"
                    battery={system.battery}
                    handleChange={handleChange}
                    disabled={system.disableParameters}
                  ></Battery>
                </Grid>
                <Grid item xs={12} md={6} xl={1.5}>
                  <h3>Inversor</h3>
                  <Grid container spacing={2}>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={system.inverterEfficiency}
                        name="inverterEfficiency"
                        handleChange={handleChange}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={system.inverterNominalPower}
                        name="inverterNominalPower"
                        handleChange={handleChange}
                      ></CustomNumberField>
                    </Grid>
                  </Grid>
                </Grid>
              </Grid>
            </AccordionDetails>
          </Accordion>
        </Grid>
        <Grid item xs={12} md={12} xl={12}>
          <Grid container spacing={2}>
            <Grid item xs={12} md={2.5} xl={2.5}>
              <Grid container spacing={2}>
                <Grid item xs={12} md={12} xl={12}>
                  <h2>Operación planta</h2>
                </Grid>
                <Grid item xs={12} md={12} xl={12} alignContent={'center'}>
                  <CustomToggle
                    name="inputOfflineOperation"
                    value={system.inputOfflineOperation}
                    handleChange={handleChange}
                    trueString="Offline"
                    falseString="Online"
                  ></CustomToggle>
                </Grid>
                <Grid item xs={12} md={12} xl={12}>
                  <h3>Parámetros turbina</h3>
                </Grid>
                <Grid item xs={12} md={12} xl={12}>
                  <ToggleCustomNumberField
                    variable={system.inputPressure}
                    name="inputPressure"
                    handleChange={handleChange}
                    disabled={system.inputOfflineOperation}
                  ></ToggleCustomNumberField>
                </Grid>
                <Grid item xs={12} md={12} xl={12}>
                  <ToggleCustomNumberField
                    variable={system.inputFlow}
                    name="inputFlow"
                    handleChange={handleChange}
                    disabled={system.inputOfflineOperation}
                  ></ToggleCustomNumberField>
                </Grid>
                {system.turbineType === TurbineType.Turgo && (
                  <>
                    <Grid item xs={12} md={12} xl={12}>
                      <h3>Parámetros carga CD</h3>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12} alignContent={'center'}>
                      <CustomToggle
                        name="inputDirectCurrentPower"
                        value={system.inputDirectCurrentPower}
                        handleChange={handleChange}
                        trueString="Conectado: 2.4 W"
                        falseString="Desconectado: 0.0 W"
                      ></CustomToggle>
                    </Grid>
                  </>
                )}
                <Grid item xs={12} md={12} xl={12}>
                  <h3>Parámetros carga CA</h3>
                </Grid>
                <Grid item xs={12} md={12} xl={12}>
                  <ToggleCustomNumberField
                    variable={system.inputActivePower}
                    name="inputActivePower"
                    handleChange={handleChange}
                    disabled={system.inputOfflineOperation}
                  ></ToggleCustomNumberField>
                </Grid>
                <Grid item xs={12} md={12} xl={12}>
                  <ToggleCustomNumberField
                    variable={system.inputPowerFactor}
                    name="inputPowerFactor"
                    handleChange={handleChange}
                    disabled={system.inputOfflineOperation}
                  ></ToggleCustomNumberField>
                </Grid>
              </Grid>
            </Grid>
            <Grid item xs={12} md={9.5} xl={9.5}>
              {playerControl}
              <TurbineDiagram
                turbine={system}
                data={data}
                isPlaying={isPlaying}
              ></TurbineDiagram>
            </Grid>
          </Grid>
        </Grid>
        {graphs !== undefined && system.timeMultiplier && (
          <>
            <Grid item xs={12} md={12} xl={12}>
              <TimeGraphs
                timeMultiplier={system.timeMultiplier}
                handleChange={handleChange}
                graphs={graphs}
                variables={
                  system.turbineType === TurbineType.Pelton
                    ? PELTON_TURBINE_DIAGRAM_VARIABLES
                    : TURGO_TURBINE_DIAGRAM_VARIABLES
                }
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
