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
  Button,
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
  MODE_2_HYBRID,
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

import solarIllustration from '../../assets/illustrations/solar.png';
import ErrorDialog from '../../components/UI/ErrorDialog';
import SolarDiagram from '../../components/models/diagram/SolarDiagram';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import FileUploadIcon from '@mui/icons-material/FileUpload';
import saveAs from 'file-saver';
import { StepUnitText, StepUnitType } from '../../types/common';

const Solar = () => {
  const [system, setSystem] = useState<SolarWindParameters>({ ...SOLAR_WIND });
  const [isImageExpanded, setIsImageExpanded] = useState(true);
  const [isSingleDiagramExpanded, setIsSingleDiagramExpanded] = useState(true);
  const [isParametersExpanded, setIsParametersExpanded] = useState(true);
  const [isMetInformationExpanded, setIsMetInformationExpanded] =
    useState(false);
  const [isOpen, setIsOpen] = useState(false);

  const [data, charts, isPlaying, error, onPlay, onPause, onStop, setError] =
    useControlPlayer<SolarWindParameters, SolarWindOutput>('solar', system);

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

  const [diagramVariables, setDiagramVariables] = useState(MODE_1_MODE_3);

  useEffect(() => {
    if (
      (system.inputOperationMode === OperationModeType.Mode1 &&
        system.cadmiumTelluridePanel.isConnected) ||
      (system.inputOperationMode === OperationModeType.Mode2 &&
        !system.hybridInverter.isConnected)
    ) {
      setDiagramVariables(MODE_1_CADMIO_MODE_2);
    } else if (
      (system.inputOperationMode === OperationModeType.Mode1 &&
        !system.cadmiumTelluridePanel.isConnected) ||
      system.inputOperationMode === OperationModeType.Mode3
    ) {
      setDiagramVariables(MODE_1_MODE_3);
    } else if (
      system.inputOperationMode === OperationModeType.Mode2 &&
      system.hybridInverter.isConnected
    ) {
      setDiagramVariables(MODE_2_HYBRID);
    } else if (system.inputOperationMode === OperationModeType.Mode4) {
      setDiagramVariables(MODE_4);
    } else if (system.inputOperationMode === OperationModeType.Mode5) {
      setDiagramVariables(MODE_5);
    }
  }, [
    system.cadmiumTelluridePanel.isConnected,
    system.hybridInverter.isConnected,
    system.inputOperationMode,
  ]);

  useEffect(() => {
    if (data !== undefined) {
      setSystem((o) => ({
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
        windSpeed: {
          ...o.windSpeed,
          value: data.inputWindSpeed ? data.inputWindSpeed : o.windSpeed.value,
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
        simulatedChargeCycleInitialSOC: data.chargeCycleInitialSOC,
      }));
    } else {
      setSystem((o) => ({
        ...o,
        simulatedBatteryStateOfCharge: undefined,
        simulatedDirectCurrentVoltage: undefined,
        simulatedChargeCycle: undefined,
        simulatedInverterState: undefined,
      }));
    }
  }, [data]);

  const handleChange = (e: any, variableName?: string) => {
    const newState = setFormState<SolarWindParameters>(e, system, variableName);
    if (newState) {
      setSystem(newState as SolarWindParameters);
    }
  };

  const handleSaveSystem = () => {
    var blob = new Blob([JSON.stringify(system)], {
      type: 'application/json',
    });
    saveAs(blob, `${system.name}.json`);
  };

  const handleUploadSystem = async (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    if (event.target.files && event.target.files.length !== 0) {
      const selectedFile = event.target.files[0];
      const reader = new FileReader();
      reader.onload = (e: any) => {
        const jsonData: SolarWindParameters = JSON.parse(
          e.target.result
        ) as SolarWindParameters;
        if ('monocrystallinePanel' in jsonData) {
          setSystem(jsonData);
        } else {
          setError('El archivo no corresponde a un gemelo digital solar');
          setIsOpen(true);
        }
        event.target.value = '';
      };
      reader.readAsText(selectedFile);
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
                  height: '400px',
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
            expanded={isSingleDiagramExpanded}
            onChange={() =>
              setIsSingleDiagramExpanded(!isSingleDiagramExpanded)
            }
          >
            <AccordionSummary
              expandIcon={<ExpandMoreIcon />}
              aria-controls="panel1-content"
              id="panel1-header"
              sx={{ margin: 0 }}
            >
              <Typography variant="h4">Unifilar</Typography>
            </AccordionSummary>
            <AccordionDetails>
              {/* <img
                style={{
                  height: '500px',
                  display: 'block',
                  marginLeft: 'auto',
                  marginRight: 'auto',
                }}
                src={turbineIllustration}
                alt="turbineIllustration"
              ></img> */}
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
                <Grid item xs={12} md={6} xl={3}>
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
                <Grid item xs={12} md={3} xl={3}>
                  <CustomNumberField
                    variable={system.steps}
                    name="steps"
                    handleChange={handleChange}
                    isInteger={true}
                  ></CustomNumberField>
                </Grid>
                <Grid item xs={12} md={3} xl={3}>
                  <CustomNumberField
                    variable={system.stepTime}
                    name="stepTime"
                    handleChange={handleChange}
                  ></CustomNumberField>
                </Grid>
                <Grid item xs={12} md={3} xl={3}>
                  <FormControl fullWidth>
                    <InputLabel id="step-unit-type">Unidad</InputLabel>
                    <Select
                      labelId="step-unit-type"
                      label="Unidad"
                      value={system.stepUnit}
                      name="stepUnit"
                      onChange={(e: any) => handleChange(e)}
                    >
                      {Object.keys(StepUnitType).map((key) => (
                        <MenuItem key={key} value={key}>
                          {getValueByKey(StepUnitText, key)}
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                </Grid>
                <Grid item xs={12} md={6} xl={12}>
                  <FormControl fullWidth>
                    <InputLabel>Modo de operación</InputLabel>
                    <Select
                      label="Modo de operación"
                      value={system.inputOperationMode}
                      name="inputOperationMode"
                      onChange={(e: any) => handleChange(e)}
                      disabled={system.disableParameters}
                    >
                      {Object.keys(OperationModeType).map((key) => (
                        <MenuItem key={key} value={key}>
                          {getValueByKey(OperationModeText, key)}
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                </Grid>
                {system.inputOperationMode !== OperationModeType.Mode4 && (
                  <>
                    <Grid item xs={12} md={6} xl={3}>
                      <SolarPanel
                        name="monocristalino"
                        propertyName="monocrystallinePanel"
                        handleChange={handleChange}
                        panel={system.monocrystallinePanel}
                        disabled={system.disableParameters}
                      ></SolarPanel>
                    </Grid>
                    <Grid item xs={12} md={6} xl={3}>
                      <SolarPanel
                        name="policristalino"
                        propertyName="policrystallinePanel"
                        handleChange={handleChange}
                        panel={system.policrystallinePanel}
                        disabled={system.disableParameters}
                      ></SolarPanel>
                    </Grid>
                    <Grid item xs={12} md={6} xl={3}>
                      <SolarPanel
                        name="monocristalino flexible"
                        propertyName="flexPanel"
                        handleChange={handleChange}
                        panel={system.flexPanel}
                        disabled={system.disableParameters}
                      ></SolarPanel>
                    </Grid>
                  </>
                )}
                {system.inputOperationMode === OperationModeType.Mode1 && (
                  <Grid item xs={12} md={6} xl={3}>
                    <SolarPanel
                      name="telururo de cadmio"
                      propertyName="cadmiumTelluridePanel"
                      handleChange={handleChange}
                      panel={system.cadmiumTelluridePanel}
                      disabled={system.disableParameters}
                    ></SolarPanel>
                  </Grid>
                )}
                {(system.inputOperationMode === OperationModeType.Mode4 ||
                  system.inputOperationMode === OperationModeType.Mode5) && (
                  <Grid item xs={12} md={6} xl={3}>
                    <h3>Aerogenerador</h3>
                    <Grid container spacing={2}>
                      <Grid item xs={6} md={12} xl={12}>
                        <CustomNumberField
                          variable={system.windTurbine.peakPower}
                          name="windTurbine.peakPower"
                          handleChange={handleChange}
                        ></CustomNumberField>
                      </Grid>
                      <Grid item xs={6} md={12} xl={6}>
                        <CustomNumberField
                          variable={system.windTurbine.rotorHeight}
                          name="windTurbine.rotorHeight"
                          handleChange={handleChange}
                          disabled={system.disableParameters}
                        ></CustomNumberField>
                      </Grid>
                      <Grid item xs={6} md={12} xl={6}>
                        <CustomNumberField
                          variable={system.windTurbine.anemometerHeight}
                          name="windTurbine.anemometerHeight"
                          handleChange={handleChange}
                          disabled={system.disableParameters}
                        ></CustomNumberField>
                      </Grid>
                      <Grid item xs={6} md={6} xl={12}>
                        <CustomNumberField
                          variable={system.windTurbine.ratedWindSpeed}
                          name="windTurbine.ratedWindSpeed"
                          handleChange={handleChange}
                        ></CustomNumberField>
                      </Grid>
                      <Grid item xs={6} md={6} xl={12}>
                        <CustomNumberField
                          variable={system.windTurbine.lowerCutoffWindSpeed}
                          name="windTurbine.lowerCutoffWindSpeed"
                          handleChange={handleChange}
                        ></CustomNumberField>
                      </Grid>
                      <Grid item xs={6} md={6} xl={12}>
                        <CustomNumberField
                          variable={system.windTurbine.upperCutoffWindSpeed}
                          name="windTurbine.upperCutoffWindSpeed"
                          handleChange={handleChange}
                        ></CustomNumberField>
                      </Grid>
                    </Grid>
                  </Grid>
                )}
                {!system.hybridInverter.isConnected && (
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
                          value={system.controller.customize}
                          handleChange={handleChange}
                          disabled={system.disableParameters}
                        ></CustomToggle>
                      </Grid>
                      <Grid item xs={6} md={6} xl={6}>
                        <CustomNumberField
                          variable={system.controller.efficiency}
                          name="controller.efficiency"
                          handleChange={handleChange}
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
                    </Grid>
                  </Grid>
                )}
                {((system.inputOperationMode === OperationModeType.Mode1 &&
                  system.cadmiumTelluridePanel.isConnected) ||
                  system.inputOperationMode === OperationModeType.Mode2) && (
                  <Grid item xs={12} md={6} xl={3}>
                    <Grid container spacing={2}>
                      {((system.inputOperationMode ===
                        OperationModeType.Mode1 &&
                        system.cadmiumTelluridePanel.isConnected) ||
                        system.inputOperationMode ===
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
                              value={system.offgridInverter.isConnected}
                              handleChange={handleChange}
                              trueString="Conectado"
                              falseString="Desconectado"
                              disabled={
                                system.offgridInverter.isConnectedDisabled ||
                                system.disableParameters
                              }
                            ></CustomToggle>
                          </Grid>
                          <Grid item xs={6} md={6} xl={6}>
                            <CustomNumberField
                              variable={system.offgridInverter.efficiency}
                              name="offgridInverter.efficiency"
                              handleChange={handleChange}
                            ></CustomNumberField>
                          </Grid>
                          <Grid item xs={6} md={6} xl={6}>
                            <CustomNumberField
                              variable={system.offgridInverter.nominalPower}
                              name="offgridInverter.nominalPower"
                              handleChange={handleChange}
                            ></CustomNumberField>
                          </Grid>
                        </>
                      )}
                      {system.inputOperationMode ===
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
                              value={system.hybridInverter.isConnected}
                              handleChange={handleChange}
                              trueString="Conectado"
                              falseString="Desconectado"
                              disabled={
                                system.hybridInverter.isConnectedDisabled ||
                                system.disableParameters
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
                              value={system.hybridInverter.customize}
                              handleChange={handleChange}
                              disabled={
                                system.disableParameters ||
                                !system.hybridInverter.isConnected
                              }
                            ></CustomToggle>
                          </Grid>
                          <Grid item xs={6} md={6} xl={6}>
                            <CustomNumberField
                              variable={system.hybridInverter.efficiency}
                              name="hybridInverter.efficiency"
                              handleChange={handleChange}
                            ></CustomNumberField>
                          </Grid>
                          <Grid item xs={6} md={6} xl={6}>
                            <CustomNumberField
                              variable={system.hybridInverter.nominalPower}
                              name="hybridInverter.nominalPower"
                              handleChange={handleChange}
                              disabled={system.disableParameters}
                            ></CustomNumberField>
                          </Grid>
                          <Grid item xs={6} md={6} xl={6}>
                            <CustomNumberField
                              variable={system.hybridInverter.chargeVoltageBulk}
                              name="hybridInverter.chargeVoltageBulk"
                              handleChange={handleChange}
                              disabled={system.disableParameters}
                            ></CustomNumberField>
                          </Grid>
                          <Grid item xs={6} md={6} xl={6}>
                            <CustomNumberField
                              variable={
                                system.hybridInverter.chargeVoltageFloat
                              }
                              name="hybridInverter.chargeVoltageFloat"
                              handleChange={handleChange}
                              disabled={system.disableParameters}
                            ></CustomNumberField>
                          </Grid>
                          <Grid item xs={6} md={6} xl={6}>
                            <CustomNumberField
                              variable={
                                system.hybridInverter.chargingMinimunVoltage
                              }
                              name="hybridInverter.chargingMinimunVoltage"
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
                        battery={system.battery1}
                        handleChange={handleChange}
                        disabled={system.disableParameters}
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
                        value={system.isBattery2}
                        handleChange={handleChange}
                        trueString="Conectado"
                        falseString="Desconectado"
                        disabled={
                          (system.inputOperationMode ===
                            OperationModeType.Mode1 &&
                            system.cadmiumTelluridePanel.isConnected) ||
                          system.inputOperationMode ===
                            OperationModeType.Mode2 ||
                          system.disableParameters
                        }
                      ></CustomToggle>
                    </Grid>
                    {system.isBattery2 && (
                      <Grid item xs={12} md={12} xl={12}>
                        <Battery
                          propertyName="battery2"
                          battery={system.battery2}
                          handleChange={handleChange}
                          disabled={system.disableParameters}
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
          <Accordion
            expanded={isMetInformationExpanded}
            onChange={() =>
              setIsMetInformationExpanded(!isMetInformationExpanded)
            }
          >
            <AccordionSummary
              expandIcon={<ExpandMoreIcon />}
              aria-controls="panel1-content"
              id="panel1-header"
              sx={{ margin: 0 }}
            >
              <Typography variant="h4">Información meteorológica</Typography>
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

        <Grid
          item
          xs={12}
          md={12}
          xl={12}
          sx={{ paddingTop: '0px', textAlign: 'center' }}
        >
          <Button
            variant="contained"
            color="info"
            onClick={handleSaveSystem}
            startIcon={<FileDownloadIcon />}
            sx={{ width: '120px', margin: '5px' }}
          >
            Guardar
          </Button>
          <Button
            component="label"
            variant="contained"
            color="info"
            startIcon={<FileUploadIcon />}
            sx={{ width: '120px', margin: '5px' }}
          >
            Cargar
            <input
              type="file"
              accept=".json"
              hidden
              onChange={handleUploadSystem}
              multiple={false}
            />
          </Button>
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
                  <h3>Parámetros ambientales</h3>
                </Grid>
                <>
                  {(system.monocrystallinePanel.isConnected ||
                    system.policrystallinePanel.isConnected) &&
                    system.inputOperationMode !== OperationModeType.Mode4 && (
                      <Grid item xs={12} md={12} xl={12}>
                        <ToggleCustomNumberField
                          variable={system.solarRadiation1}
                          name="solarRadiation1"
                          handleChange={handleChange}
                          disabled={system.inputOfflineOperation}
                        ></ToggleCustomNumberField>
                      </Grid>
                    )}
                  {(system.flexPanel.isConnected ||
                    system.cadmiumTelluridePanel.isConnected) &&
                    system.inputOperationMode !== OperationModeType.Mode4 && (
                      <Grid item xs={12} md={12} xl={12}>
                        <ToggleCustomNumberField
                          variable={system.solarRadiation2}
                          name="solarRadiation2"
                          handleChange={handleChange}
                          disabled={system.inputOfflineOperation}
                        ></ToggleCustomNumberField>
                      </Grid>
                    )}
                  {system.inputOperationMode !== OperationModeType.Mode4 && (
                    <Grid item xs={7} md={7} xl={7}>
                      <CustomNumberField
                        variable={system.temperature}
                        name="temperature"
                        handleChange={handleChange}
                      ></CustomNumberField>
                    </Grid>
                  )}
                </>
                {(system.inputOperationMode === OperationModeType.Mode4 ||
                  system.inputOperationMode === OperationModeType.Mode5) && (
                  <>
                    <Grid item xs={12} md={12} xl={12}>
                      <ToggleCustomNumberField
                        variable={system.windSpeed}
                        name="windSpeed"
                        handleChange={handleChange}
                        disabled={system.inputOfflineOperation}
                      ></ToggleCustomNumberField>
                    </Grid>
                    <Grid item xs={7} md={7} xl={7}>
                      <CustomNumberField
                        variable={system.windDensity}
                        name="windDensity"
                        handleChange={handleChange}
                      ></CustomNumberField>
                    </Grid>
                  </>
                )}
                {((system.inputOperationMode === OperationModeType.Mode1 &&
                  system.cadmiumTelluridePanel.isConnected &&
                  system.offgridInverter.isConnected) ||
                  (system.inputOperationMode === OperationModeType.Mode2 &&
                    (system.offgridInverter.isConnected ||
                      system.hybridInverter.isConnected))) && (
                  <>
                    <Grid item xs={12} md={12} xl={12}>
                      <h3>Parámetros carga CA</h3>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <ToggleCustomNumberField
                        variable={system.alternCurrentLoadPower}
                        name="alternCurrentLoadPower"
                        handleChange={handleChange}
                        disabled={system.inputOfflineOperation}
                      ></ToggleCustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <ToggleCustomNumberField
                        variable={system.alternCurrentLoadPowerFactor}
                        name="alternCurrentLoadPowerFactor"
                        handleChange={handleChange}
                        disabled={system.inputOfflineOperation}
                      ></ToggleCustomNumberField>
                    </Grid>
                  </>
                )}
                {!(
                  system.inputOperationMode === OperationModeType.Mode2 &&
                  system.hybridInverter.isConnected
                ) && (
                  <>
                    <Grid item xs={12} md={12} xl={12}>
                      <h3>Parámetros carga CC</h3>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <ToggleCustomNumberField
                        variable={system.directCurrentLoadPower}
                        name="directCurrentLoadPower"
                        handleChange={handleChange}
                        disabled={system.inputOfflineOperation}
                      ></ToggleCustomNumberField>
                    </Grid>
                  </>
                )}
                {system.inputOperationMode === OperationModeType.Mode2 &&
                  system.hybridInverter.isConnected && (
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
                          value={system.externalGridState}
                          handleChange={handleChange}
                          trueString="Conectado"
                          falseString="Desconectado"
                        ></CustomToggle>
                      </Grid>
                    </>
                  )}
                <Grid item xs={12} md={12} xl={12}>
                  <h3>Conexión baterías</h3>
                </Grid>
                <Grid item xs={12} md={12} xl={12} alignContent={'center'}>
                  <CustomToggle
                    name="isBatteryConnected"
                    value={system.isBatteryConnected}
                    handleChange={handleChange}
                    trueString="Conectada"
                    falseString="Desconectada"
                  ></CustomToggle>
                </Grid>
              </Grid>
            </Grid>
            <Grid item xs={12} md={9.5} xl={9.5}>
              {playerControl}
              <SolarDiagram
                solarWind={system}
                data={data}
                isPlaying={isPlaying}
                diagramVariables={diagramVariables}
              ></SolarDiagram>
            </Grid>
          </Grid>
        </Grid>

        {charts !== undefined && system.timeMultiplier && (
          <>
            <Grid item xs={12} md={12} xl={12}>
              <TimeGraphs
                timeMultiplier={system.timeMultiplier}
                handleChange={handleChange}
                charts={charts}
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
