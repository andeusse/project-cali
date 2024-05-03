import {
  Grid,
  FormControl,
  TextField,
  InputLabel,
  MenuItem,
  Select,
  Accordion,
  AccordionDetails,
  AccordionSummary,
  Typography,
} from '@mui/material';
import { useEffect, useState } from 'react';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import {
  SOLAR_WIND,
  SolarWindParameters,
  OperationModeType,
  OperationModeText,
  SolarWindOutput,
  MODE_1_CADMIO_MODE_2,
  MODE_1_MODE_3,
  MODE_2_HYBRID_DIAGRAM_VARIABLES,
  MODE_4,
  MODE_5,
} from '../../types/models/solar';
import { setFormState } from '../../utils/setFormState';
import Iframe from 'react-iframe';
import Config from '../../config/config';
import TimeGraphs from '../../components/models/common/TimeGraphs';
import PlayerControls from '../../components/UI/PlayerControls';
import { useControlPlayer } from '../../hooks/useControlPlayer';
import ToggleCustomNumberField from '../../components/UI/ToggleCustomNumberField';
import CustomNumberField from '../../components/UI/CustomNumberField';
import { getValueByKey } from '../../utils/getValueByKey';
import SolarPanel from '../../components/models/SolarPanel';
import Battery from '../../components/models/Battery';
import CustomToggle from '../../components/UI/CustomToggle';

import solarIllustration from '../../assets/illustrations/solar.jpg';
import ErrorDialog from '../../components/UI/ErrorDialog';
import SolarDiagram from '../../components/models/diagram/SolarDiagram';

type Props = {};

const Solar = (props: Props) => {
  const [solarWind, setSolarWind] = useState<SolarWindParameters>(SOLAR_WIND);
  const [isImageExpanded, setIsImageExpanded] = useState(true);
  const [isParametersExpanded, setIsParametersExpanded] = useState(true);
  const [isMetInformationExpanded, setIsMetInformationExpanded] =
    useState(false);
  const [isOpen, setIsOpen] = useState(false);

  const [data, graphs, isPlaying, error, onPlay, onPause, onStop] =
    useControlPlayer<SolarWindParameters, SolarWindOutput>('solar', solarWind);

  useEffect(() => {
    setSolarWind((o) => {
      return { ...o, disableParameters: isPlaying };
    });
  }, [isPlaying]);

  useEffect(() => {
    if (error !== '') {
      setIsOpen(true);
    }
  }, [error]);

  const [diagramVariables, setDiagramVariables] = useState(MODE_1_MODE_3);

  useEffect(() => {
    if (
      (solarWind.inputOperationMode === OperationModeType.Mode1 &&
        solarWind.cadmiumTelluridePanel.isConnected) ||
      (solarWind.inputOperationMode === OperationModeType.Mode2 &&
        !solarWind.hybridInverter.isConnected)
    ) {
      setDiagramVariables(MODE_1_CADMIO_MODE_2);
    } else if (
      (solarWind.inputOperationMode === OperationModeType.Mode1 &&
        !solarWind.cadmiumTelluridePanel.isConnected) ||
      solarWind.inputOperationMode === OperationModeType.Mode3
    ) {
      setDiagramVariables(MODE_1_MODE_3);
    } else if (
      solarWind.inputOperationMode === OperationModeType.Mode2 &&
      solarWind.hybridInverter.isConnected
    ) {
      setDiagramVariables(MODE_2_HYBRID_DIAGRAM_VARIABLES);
    } else if (solarWind.inputOperationMode === OperationModeType.Mode4) {
      setDiagramVariables(MODE_4);
    } else if (solarWind.inputOperationMode === OperationModeType.Mode5) {
      setDiagramVariables(MODE_5);
    }
  }, [
    solarWind.cadmiumTelluridePanel.isConnected,
    solarWind.hybridInverter.isConnected,
    solarWind.inputOperationMode,
  ]);

  useEffect(() => {
    if (data !== undefined) {
      setSolarWind((o) => ({
        ...o,
        solarRadiation1: {
          ...o.solarRadiation1,
          value: data.inputSolarRadiation1
            ? data.inputSolarRadiation1
            : o.solarRadiation1.value,
        },
        solarRadiation2: {
          ...o.solarRadiation2,
          value: data.inputSolarRadiation2
            ? data.inputSolarRadiation2
            : o.solarRadiation2.value,
        },
        alternCurrentLoadPower: {
          ...o.alternCurrentLoadPower,
          value: data.inputAlternCurrentLoadPower
            ? data.inputAlternCurrentLoadPower
            : o.alternCurrentLoadPower.value,
        },
        alternCurrentLoadPowerFactor: {
          ...o.alternCurrentLoadPowerFactor,
          value: data.inputAlternCurrentLoadPowerFactor
            ? data.inputAlternCurrentLoadPowerFactor
            : o.alternCurrentLoadPowerFactor.value,
        },
        directCurrentLoadPower: {
          ...o.directCurrentLoadPower,
          value: data.inputDirectCurrentLoadPower
            ? data.inputDirectCurrentLoadPower
            : o.directCurrentLoadPower.value,
        },
        simulatedBatteryStateOfCharge: data.batteryStateOfCharge,
        simulatedDirectCurrentVoltage: data.directCurrentVoltage,
        simulatedChargeCycle: data.chargeCycle,
        simulatedInverterState: data.inverterState,
      }));
    } else {
      setSolarWind((o) => ({
        ...o,
        simulatedBatteryStateOfCharge: undefined,
        simulatedDirectCurrentVoltage: undefined,
        simulatedChargeCycle: undefined,
        simulatedInverterState: undefined,
      }));
    }
  }, [data]);

  const handleChange = (e: any, variableName?: string) => {
    const newState = setFormState<SolarWindParameters>(
      e,
      solarWind,
      variableName
    );
    if (newState) {
      setSolarWind(newState as SolarWindParameters);
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

  const handleImageExpanded = () => {
    setIsImageExpanded(!isImageExpanded);
  };

  const handleParametersExpanded = () => {
    setIsParametersExpanded(!isParametersExpanded);
  };

  const handleMetInformationExpanded = () => {
    setIsMetInformationExpanded(!isMetInformationExpanded);
  };

  return (
    <>
      <ErrorDialog
        isOpen={isOpen}
        setIsOpen={setIsOpen}
        error={error}
      ></ErrorDialog>
      <Grid container spacing={2}>
        <Grid item xs={12} md={12} xl={12}>
          <Accordion expanded={isImageExpanded} onChange={handleImageExpanded}>
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
                src={solarIllustration}
                alt="solarIllustration"
              ></img>
            </AccordionDetails>
          </Accordion>
        </Grid>
        <Grid item xs={12} md={12} xl={12}>
          <Accordion
            expanded={isParametersExpanded}
            onChange={handleParametersExpanded}
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
                <Grid item xs={12} md={6} xl={4}>
                  <FormControl fullWidth>
                    <InputLabel>Modo de operación</InputLabel>
                    <Select
                      label="Modo de operación"
                      value={solarWind.inputOperationMode}
                      name="inputOperationMode"
                      onChange={(e: any) => handleChange(e)}
                      disabled={solarWind.disableParameters}
                    >
                      {Object.keys(OperationModeType).map((key) => (
                        <MenuItem key={key} value={key}>
                          {getValueByKey(OperationModeText, key)}
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                </Grid>
                <Grid item xs={12} md={6} xl={8}>
                  <FormControl fullWidth>
                    <TextField
                      label="Nombre"
                      value={solarWind.name}
                      name="name"
                      autoComplete="off"
                      onChange={handleChange}
                      disabled={solarWind.disableParameters}
                    />
                  </FormControl>
                </Grid>
                {solarWind.inputOperationMode !== OperationModeType.Mode4 && (
                  <>
                    <Grid item xs={12} md={6} xl={3}>
                      <SolarPanel
                        name="monocristalino"
                        propertyName="monocrystallinePanel"
                        handleChange={handleChange}
                        panel={solarWind.monocrystallinePanel}
                        disabled={solarWind.disableParameters}
                      ></SolarPanel>
                    </Grid>
                    <Grid item xs={12} md={6} xl={3}>
                      <SolarPanel
                        name="policristalino"
                        propertyName="policrystallinePanel"
                        handleChange={handleChange}
                        panel={solarWind.policrystallinePanel}
                        disabled={solarWind.disableParameters}
                      ></SolarPanel>
                    </Grid>
                    <Grid item xs={12} md={6} xl={3}>
                      <SolarPanel
                        name="monocristalino flexible"
                        propertyName="flexPanel"
                        handleChange={handleChange}
                        panel={solarWind.flexPanel}
                        disabled={solarWind.disableParameters}
                      ></SolarPanel>
                    </Grid>
                  </>
                )}
                {solarWind.inputOperationMode === OperationModeType.Mode1 && (
                  <Grid item xs={12} md={6} xl={3}>
                    <SolarPanel
                      name="telururo de cadmio"
                      propertyName="cadmiumTelluridePanel"
                      handleChange={handleChange}
                      panel={solarWind.cadmiumTelluridePanel}
                      disabled={solarWind.disableParameters}
                    ></SolarPanel>
                  </Grid>
                )}
                {(solarWind.inputOperationMode === OperationModeType.Mode4 ||
                  solarWind.inputOperationMode === OperationModeType.Mode5) && (
                  <Grid item xs={12} md={6} xl={3}>
                    <h3>Aerogenerador</h3>
                    <Grid container spacing={2}>
                      <Grid item xs={6} md={12} xl={12}>
                        <CustomNumberField
                          variable={solarWind.windTurbine.peakPower}
                          name="windTurbine.peakPower"
                          handleChange={handleChange}
                        ></CustomNumberField>
                      </Grid>
                      <Grid item xs={6} md={12} xl={6}>
                        <CustomNumberField
                          variable={solarWind.windTurbine.rotorHeight}
                          name="windTurbine.rotorHeight"
                          handleChange={handleChange}
                          disabled={solarWind.disableParameters}
                        ></CustomNumberField>
                      </Grid>
                      <Grid item xs={6} md={12} xl={6}>
                        <CustomNumberField
                          variable={solarWind.windTurbine.anemometerHeight}
                          name="windTurbine.anemometerHeight"
                          handleChange={handleChange}
                          disabled={solarWind.disableParameters}
                        ></CustomNumberField>
                      </Grid>
                      <Grid item xs={6} md={6} xl={12}>
                        <CustomNumberField
                          variable={solarWind.windTurbine.ratedWindSpeed}
                          name="windTurbine.ratedWindSpeed"
                          handleChange={handleChange}
                        ></CustomNumberField>
                      </Grid>
                      <Grid item xs={6} md={6} xl={12}>
                        <CustomNumberField
                          variable={solarWind.windTurbine.lowerCutoffWindSpeed}
                          name="windTurbine.lowerCutoffWindSpeed"
                          handleChange={handleChange}
                        ></CustomNumberField>
                      </Grid>
                      <Grid item xs={6} md={6} xl={12}>
                        <CustomNumberField
                          variable={solarWind.windTurbine.upperCutoffWindSpeed}
                          name="windTurbine.upperCutoffWindSpeed"
                          handleChange={handleChange}
                        ></CustomNumberField>
                      </Grid>
                    </Grid>
                  </Grid>
                )}
                {!solarWind.hybridInverter.isConnected && (
                  <Grid item xs={12} md={6} xl={3}>
                    <h3>Controlador carga</h3>
                    <Grid container spacing={2}>
                      <Grid
                        item
                        xs={12}
                        md={12}
                        xl={12}
                        alignContent={'center'}
                        height={'72px'}
                      >
                        <CustomToggle
                          name="controller.customize"
                          value={solarWind.controller.customize}
                          handleChange={handleChange}
                          disabled={solarWind.disableParameters}
                        ></CustomToggle>
                      </Grid>
                      <Grid item xs={6} md={6} xl={6}>
                        <CustomNumberField
                          variable={solarWind.controller.efficiency}
                          name="controller.efficiency"
                          handleChange={handleChange}
                        ></CustomNumberField>
                      </Grid>
                      <Grid item xs={6} md={6} xl={6}>
                        <CustomNumberField
                          variable={solarWind.controller.chargeVoltageBulk}
                          name="controller.chargeVoltageBulk"
                          handleChange={handleChange}
                          disabled={solarWind.disableParameters}
                        ></CustomNumberField>
                      </Grid>
                      <Grid item xs={6} md={6} xl={6}>
                        <CustomNumberField
                          variable={solarWind.controller.chargeVoltageFloat}
                          name="controller.chargeVoltageFloat"
                          handleChange={handleChange}
                          disabled={solarWind.disableParameters}
                        ></CustomNumberField>
                      </Grid>
                      <Grid item xs={6} md={6} xl={6}>
                        <CustomNumberField
                          variable={solarWind.controller.chargingMinimunVoltage}
                          name="controller.chargingMinimunVoltage"
                          handleChange={handleChange}
                          disabled={solarWind.disableParameters}
                        ></CustomNumberField>
                      </Grid>
                    </Grid>
                  </Grid>
                )}
                {((solarWind.inputOperationMode === OperationModeType.Mode1 &&
                  solarWind.cadmiumTelluridePanel.isConnected) ||
                  solarWind.inputOperationMode === OperationModeType.Mode2) && (
                  <Grid item xs={12} md={6} xl={3}>
                    <Grid container spacing={2}>
                      {((solarWind.inputOperationMode ===
                        OperationModeType.Mode1 &&
                        solarWind.cadmiumTelluridePanel.isConnected) ||
                        solarWind.inputOperationMode ===
                          OperationModeType.Mode2) && (
                        <>
                          <Grid item xs={12} md={6} xl={6}>
                            <h3>Inversor offgrid</h3>
                          </Grid>
                          <Grid
                            item
                            xs={12}
                            md={12}
                            xl={12}
                            alignContent={'center'}
                          >
                            <CustomToggle
                              name="offgridInverter.isConnected"
                              value={solarWind.offgridInverter.isConnected}
                              handleChange={handleChange}
                              trueString="Conectado"
                              falseString="Desconectado"
                              disabled={
                                solarWind.offgridInverter.isConnectedDisabled ||
                                solarWind.disableParameters
                              }
                            ></CustomToggle>
                          </Grid>
                          <Grid item xs={6} md={6} xl={6}>
                            <CustomNumberField
                              variable={solarWind.offgridInverter.efficiency}
                              name="offgridInverter.efficiency"
                              handleChange={handleChange}
                            ></CustomNumberField>
                          </Grid>
                          <Grid item xs={6} md={6} xl={6}>
                            <CustomNumberField
                              variable={solarWind.offgridInverter.nominalPower}
                              name="offgridInverter.nominalPower"
                              handleChange={handleChange}
                            ></CustomNumberField>
                          </Grid>
                        </>
                      )}
                      {solarWind.inputOperationMode ===
                        OperationModeType.Mode2 && (
                        <>
                          <Grid
                            item
                            xs={12}
                            md={12}
                            xl={12}
                            sx={{ height: '72px' }}
                          >
                            <h3>Inversor híbrido</h3>
                          </Grid>
                          <Grid
                            item
                            xs={6}
                            md={6}
                            xl={6}
                            alignContent={'center'}
                            height={'72px'}
                          >
                            <CustomToggle
                              name="hybridInverter.isConnected"
                              value={solarWind.hybridInverter.isConnected}
                              handleChange={handleChange}
                              trueString="Conectado"
                              falseString="Desconectado"
                              disabled={
                                solarWind.hybridInverter.isConnectedDisabled ||
                                solarWind.disableParameters
                              }
                            ></CustomToggle>
                          </Grid>
                          <Grid
                            item
                            xs={6}
                            md={6}
                            xl={6}
                            alignContent={'center'}
                          >
                            <CustomToggle
                              name="hybridInverter.customize"
                              value={solarWind.hybridInverter.customize}
                              handleChange={handleChange}
                              disabled={
                                solarWind.disableParameters ||
                                !solarWind.hybridInverter.isConnected
                              }
                            ></CustomToggle>
                          </Grid>
                          <Grid item xs={6} md={6} xl={6}>
                            <CustomNumberField
                              variable={solarWind.hybridInverter.efficiency}
                              name="hybridInverter.efficiency"
                              handleChange={handleChange}
                            ></CustomNumberField>
                          </Grid>
                          <Grid item xs={6} md={6} xl={6}>
                            <CustomNumberField
                              variable={solarWind.hybridInverter.nominalPower}
                              name="hybridInverter.nominalPower"
                              handleChange={handleChange}
                            ></CustomNumberField>
                          </Grid>
                          <Grid item xs={6} md={6} xl={6}>
                            <CustomNumberField
                              variable={
                                solarWind.hybridInverter.chargeVoltageBulk
                              }
                              name="controller.chargeVoltageBulk"
                              handleChange={handleChange}
                            ></CustomNumberField>
                          </Grid>
                          <Grid item xs={6} md={6} xl={6}>
                            <CustomNumberField
                              variable={
                                solarWind.hybridInverter.chargeVoltageFloat
                              }
                              name="controller.chargeVoltageFloat"
                              handleChange={handleChange}
                              disabled={false}
                            ></CustomNumberField>
                          </Grid>
                          <Grid item xs={6} md={6} xl={6}>
                            <CustomNumberField
                              variable={
                                solarWind.hybridInverter.chargingMinimunVoltage
                              }
                              name="controller.chargingMinimunVoltage"
                              handleChange={handleChange}
                            ></CustomNumberField>
                          </Grid>
                        </>
                      )}
                    </Grid>
                  </Grid>
                )}
                <Grid item xs={12} md={6} xl={3}>
                  <Grid container>
                    <Grid item xs={12} md={12} xl={12}>
                      <h3>Batería 1:</h3>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <Battery
                        propertyName="battery1"
                        battery={solarWind.battery1}
                        handleChange={handleChange}
                        disabled={solarWind.disableParameters}
                      ></Battery>
                    </Grid>{' '}
                  </Grid>
                </Grid>
                <Grid item xs={12} md={6} xl={3}>
                  <Grid container>
                    <Grid item xs={12} md={6} xl={6}>
                      <h3>Batería 2:</h3>
                    </Grid>
                    <Grid item xs={12} md={6} xl={6} alignContent={'center'}>
                      <CustomToggle
                        name="isBattery2"
                        value={solarWind.isBattery2}
                        handleChange={handleChange}
                        trueString="Conectado"
                        falseString="Desconectado"
                        disabled={
                          (solarWind.inputOperationMode ===
                            OperationModeType.Mode1 &&
                            solarWind.cadmiumTelluridePanel.isConnected) ||
                          solarWind.inputOperationMode ===
                            OperationModeType.Mode2 ||
                          solarWind.disableParameters
                        }
                      ></CustomToggle>
                    </Grid>
                    {solarWind.isBattery2 && (
                      <Grid item xs={12} md={12} xl={12}>
                        <Battery
                          propertyName="battery2"
                          battery={solarWind.battery2}
                          handleChange={handleChange}
                          disabled={solarWind.disableParameters}
                        ></Battery>
                      </Grid>
                    )}
                  </Grid>
                </Grid>
              </Grid>
            </AccordionDetails>
          </Accordion>
        </Grid>
        <Grid item xs={12} md={12} xl={12}>
          <Grid container spacing={2}>
            <Grid item xs={12} md={12} xl={12}>
              <Accordion
                expanded={isMetInformationExpanded}
                onChange={handleMetInformationExpanded}
              >
                <AccordionSummary
                  expandIcon={<ExpandMoreIcon />}
                  aria-controls="panel1-content"
                  id="panel1-header"
                  sx={{ margin: 0 }}
                >
                  <Typography variant="h4">
                    Información meteorológica
                  </Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <Grid container spacing={2}>
                    <Grid item xs={12} md={4} xl={4}>
                      <Iframe
                        styles={{
                          width: '100%',
                          height: '500px',
                        }}
                        url={Config.getInstance().params.windyUrlRadiation}
                      ></Iframe>
                    </Grid>
                    <Grid item xs={12} md={4} xl={4}>
                      <Iframe
                        styles={{
                          width: '100%',
                          height: '500px',
                        }}
                        url={Config.getInstance().params.windyUrlTemperature}
                      ></Iframe>
                    </Grid>
                    <Grid item xs={12} md={4} xl={4}>
                      <Iframe
                        styles={{
                          width: '100%',
                          height: '500px',
                        }}
                        url={Config.getInstance().params.windyUrlWindSpeed}
                      ></Iframe>
                    </Grid>
                  </Grid>
                </AccordionDetails>
              </Accordion>
            </Grid>
            <Grid item xs={12} md={2.5} xl={2.5}>
              <Grid container spacing={2}>
                <Grid item xs={12} md={12} xl={12}>
                  <h2>Operación planta</h2>
                </Grid>
                <Grid item xs={12} md={12} xl={12} alignContent={'center'}>
                  <CustomToggle
                    name="inputOfflineOperation"
                    value={solarWind.inputOfflineOperation}
                    handleChange={handleChange}
                    trueString="Offline"
                    falseString="Online"
                  ></CustomToggle>
                </Grid>
                <Grid item xs={12} md={12} xl={12}>
                  <h3>Parámetros ambientales</h3>
                </Grid>
                <>
                  {(solarWind.monocrystallinePanel.isConnected ||
                    solarWind.policrystallinePanel.isConnected) &&
                    solarWind.inputOperationMode !==
                      OperationModeType.Mode4 && (
                      <Grid item xs={12} md={12} xl={12}>
                        <ToggleCustomNumberField
                          variable={solarWind.solarRadiation1}
                          name="solarRadiation1"
                          handleChange={handleChange}
                          disabled={solarWind.inputOfflineOperation}
                        ></ToggleCustomNumberField>
                      </Grid>
                    )}
                  {(solarWind.flexPanel.isConnected ||
                    solarWind.cadmiumTelluridePanel.isConnected) &&
                    solarWind.inputOperationMode !==
                      OperationModeType.Mode4 && (
                      <Grid item xs={12} md={12} xl={12}>
                        <ToggleCustomNumberField
                          variable={solarWind.solarRadiation2}
                          name="solarRadiation2"
                          handleChange={handleChange}
                          disabled={solarWind.inputOfflineOperation}
                        ></ToggleCustomNumberField>
                      </Grid>
                    )}
                  {solarWind.inputOperationMode !== OperationModeType.Mode4 && (
                    <Grid item xs={7} md={7} xl={7}>
                      <CustomNumberField
                        variable={solarWind.temperature}
                        name="temperature"
                        handleChange={handleChange}
                      ></CustomNumberField>
                    </Grid>
                  )}
                </>
                {(solarWind.inputOperationMode === OperationModeType.Mode4 ||
                  solarWind.inputOperationMode === OperationModeType.Mode5) && (
                  <>
                    <Grid item xs={12} md={12} xl={12}>
                      <ToggleCustomNumberField
                        variable={solarWind.windSpeed}
                        name="windSpeed"
                        handleChange={handleChange}
                        disabled={solarWind.inputOfflineOperation}
                      ></ToggleCustomNumberField>
                    </Grid>
                    <Grid item xs={7} md={7} xl={7}>
                      <CustomNumberField
                        variable={solarWind.windDensity}
                        name="windDensity"
                        handleChange={handleChange}
                      ></CustomNumberField>
                    </Grid>
                  </>
                )}
                {((solarWind.inputOperationMode === OperationModeType.Mode1 &&
                  solarWind.cadmiumTelluridePanel.isConnected &&
                  solarWind.offgridInverter.isConnected) ||
                  (solarWind.inputOperationMode === OperationModeType.Mode2 &&
                    (solarWind.offgridInverter.isConnected ||
                      solarWind.hybridInverter.isConnected))) && (
                  <>
                    <Grid item xs={12} md={12} xl={12}>
                      <h3>Parámetros carga CA</h3>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <ToggleCustomNumberField
                        variable={solarWind.alternCurrentLoadPower}
                        name="alternCurrentLoadPower"
                        handleChange={handleChange}
                        disabled={solarWind.inputOfflineOperation}
                      ></ToggleCustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <ToggleCustomNumberField
                        variable={solarWind.alternCurrentLoadPowerFactor}
                        name="alternCurrentLoadPowerFactor"
                        handleChange={handleChange}
                        disabled={solarWind.inputOfflineOperation}
                      ></ToggleCustomNumberField>
                    </Grid>
                  </>
                )}
                {!(
                  solarWind.inputOperationMode === OperationModeType.Mode2 &&
                  solarWind.hybridInverter.isConnected
                ) && (
                  <>
                    <Grid item xs={12} md={12} xl={12}>
                      <h3>Parámetros carga CD</h3>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <ToggleCustomNumberField
                        variable={solarWind.directCurrentLoadPower}
                        name="directCurrentLoadPower"
                        handleChange={handleChange}
                        disabled={solarWind.inputOfflineOperation}
                      ></ToggleCustomNumberField>
                    </Grid>
                  </>
                )}
                {solarWind.inputOperationMode === OperationModeType.Mode2 &&
                  solarWind.hybridInverter.isConnected && (
                    <>
                      <Grid item xs={12} md={12} xl={12}>
                        <h3>Parámetros red externa</h3>
                      </Grid>
                      <Grid
                        item
                        xs={12}
                        md={12}
                        xl={12}
                        alignContent={'center'}
                      >
                        <CustomToggle
                          name="externalGridState"
                          value={solarWind.externalGridState}
                          handleChange={handleChange}
                          trueString="Conectado"
                          falseString="Desconectado"
                        ></CustomToggle>
                      </Grid>
                    </>
                  )}
              </Grid>
            </Grid>
            <Grid item xs={12} md={9.5} xl={9.5}>
              {playerControl}
              <SolarDiagram
                solarWind={solarWind}
                data={data}
                isPlaying={isPlaying}
              ></SolarDiagram>
            </Grid>
          </Grid>
        </Grid>
        {graphs !== undefined && solarWind.timeMultiplier && (
          <>
            <Grid item xs={12} md={12} xl={12}>
              <TimeGraphs
                timeMultiplier={solarWind.timeMultiplier}
                handleChange={handleChange}
                graphs={graphs}
                variables={diagramVariables}
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
