import {
  Accordion,
  AccordionDetails,
  AccordionSummary,
  Button,
  FormControl,
  Grid,
  InputLabel,
  MenuItem,
  Select,
  TextField,
  Typography,
} from '@mui/material';
import React, { useEffect, useState } from 'react';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import {
  BIOGAS,
  BIOGAS_MODE1,
  BIOGAS_MODE2,
  BIOGAS_MODE3,
  BIOGAS_MODE4,
  BIOGAS_MODE5,
  BiogasOutput,
  BiogasParameters,
  DiagramBiogasText,
  DiagramBiogasType,
  DiagramCompoundText,
  DiagramCompoundType,
  DiagramHumidityText,
  DiagramHumidityType,
  DiagramBiogasUnitText,
  DiagramBiogasUnitType,
  OperationModeType,
} from '../../types/models/biogas';
import { useControlPlayer } from '../../hooks/useControlPlayer';
import { setFormState } from '../../utils/setFormState';
import PlayerControls from '../../components/UI/PlayerControls';
import CustomNumberField from '../../components/UI/CustomNumberField';
import TimeGraphs from '../../components/models/common/TimeGraphs';
import ToggleCustomNumberField from '../../components/UI/ToggleCustomNumberField';
import CustomToggle from '../../components/UI/CustomToggle';
import ErrorDialog from '../../components/UI/ErrorDialog';

import biogasIllustration from '../../assets/illustrations/biogas.png';
import BiogasDiagram from '../../components/models/diagram/BiogasDiagram';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import FileUploadIcon from '@mui/icons-material/FileUpload';
import saveAs from 'file-saver';
import { getValueByKey } from '../../utils/getValueByKey';

const Biogas = () => {
  const [system, setSystem] = useState<BiogasParameters>({ ...BIOGAS });
  const [isImageExpanded, setIsImageExpanded] = useState(true);
  const [isParametersExpanded, setIsParametersExpanded] = useState(true);
  const [isOpen, setIsOpen] = useState(false);

  const [diagramVariables, setDiagramVariables] = useState(BIOGAS_MODE1);

  const [data, charts, isPlaying, error, onPlay, onPause, onStop, setError] =
    useControlPlayer<BiogasParameters, BiogasOutput>('biogas', system);

  useEffect(() => {
    if (system.inputOperationMode === OperationModeType.Modo1) {
      setDiagramVariables(BIOGAS_MODE1);
    }
    if (system.inputOperationMode === OperationModeType.Modo2) {
      setDiagramVariables(BIOGAS_MODE2);
    }
    if (system.inputOperationMode === OperationModeType.Modo3) {
      setDiagramVariables(BIOGAS_MODE3);
    }
    if (system.inputOperationMode === OperationModeType.Modo4) {
      setDiagramVariables(BIOGAS_MODE4);
    }
    if (system.inputOperationMode === OperationModeType.Modo5) {
      setDiagramVariables(BIOGAS_MODE5);
    }
  }, [system.inputOperationMode]);

  useEffect(() => {
    setSystem((o) => {
      return { ...o, disableParameters: isPlaying };
    });
  }, [isPlaying]);

  useEffect(() => {
    if (data !== undefined) {
      setSystem((o) => ({ ...o, restartFlag: false }));
    } else {
      setSystem((o) => ({ ...o, restartFlag: true }));
    }
  }, [data]);

  useEffect(() => {
    if (error !== '') {
      setIsOpen(true);
    }
  }, [error]);

  const handleChange = (e: any, variableName?: string) => {
    const newState = setFormState<BiogasParameters>(e, system, variableName);
    if (newState) {
      setSystem(newState as BiogasParameters);
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
        const jsonData: BiogasParameters = JSON.parse(
          e.target.result
        ) as BiogasParameters;
        if ('anaerobicReactorVolume1' in jsonData) {
          setSystem(jsonData);
        } else {
          setError('El archivo no corresponde a un gemelo digital de biogas');
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
                  height: '500px',
                  display: 'block',
                  marginLeft: 'auto',
                  marginRight: 'auto',
                }}
                src={biogasIllustration}
                alt="biogasIllustration"
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
                <Grid item xs={12} md={6} xl={2.5}>
                  <Grid container spacing={2}>
                    <Grid item xs={12} md={12} xl={12} sx={{ height: '72px' }}>
                      <h3>Operación planta</h3>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={system.anaerobicReactorVolume1}
                        name="anaerobicReactorVolume1"
                        handleChange={handleChange}
                        disabled={system.disableParameters}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={system.anaerobicReactorVolume2}
                        name="anaerobicReactorVolume2"
                        handleChange={handleChange}
                        disabled={system.disableParameters}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12} sx={{ height: '72px' }}>
                      <h3>Tanques de biogás</h3>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={system.biogasTankVolume1}
                        name="biogasTankVolume1"
                        handleChange={handleChange}
                        disabled={system.disableParameters}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={system.biogasTankVolume2}
                        name="biogasTankVolume2"
                        handleChange={handleChange}
                        disabled={system.disableParameters}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={system.biogasTankVolume3}
                        name="biogasTankVolume3"
                        handleChange={handleChange}
                        disabled={system.disableParameters}
                      ></CustomNumberField>
                    </Grid>
                  </Grid>
                </Grid>
                <Grid item xs={12} md={6} xl={3.5}>
                  <Grid container spacing={2}>
                    <Grid item xs={12} md={6} xl={6} sx={{ height: '72px' }}>
                      <h3>Parámetros gemelo</h3>
                    </Grid>
                    <Grid
                      item
                      xs={12}
                      md={6}
                      xl={6}
                      sx={{ alignContent: 'center' }}
                    >
                      <CustomToggle
                        name="inputDigitalTwin"
                        value={system.digitalTwinState}
                        handleChange={handleChange}
                        trueString="Gemelo on"
                        falseString="Gemelo off"
                        disabled={system.disableParameters}
                      ></CustomToggle>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={system.digitalTwinStepTime}
                        name="inputDigitalTwinStepTime"
                        handleChange={handleChange}
                        disabled={system.disableParameters}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={system.digitalTwinForecastTime}
                        name="inputDigitalTwinForecastTime"
                        handleChange={handleChange}
                        disabled={system.disableParameters}
                      ></CustomNumberField>
                    </Grid>
                  </Grid>
                </Grid>
                <Grid item xs={12} md={12} xl={3}>
                  <Grid container spacing={2}>
                    <Grid item xs={12} md={12} xl={12} sx={{ height: '72px' }}>
                      <h3>Operación planta</h3>
                    </Grid>
                    <Grid item xs={12} md={6} xl={6}>
                      <FormControl fullWidth>
                        <InputLabel>Modo de operación</InputLabel>
                        <Select
                          label="Modo de operación"
                          value={system.inputOperationMode}
                          name="inputOperationMode"
                          disabled={isPlaying}
                          onChange={(e: any) => handleChange(e)}
                        >
                          {Object.values(OperationModeType).map((key) => (
                            <MenuItem key={key} value={key}>
                              {key}
                            </MenuItem>
                          ))}
                        </Select>
                      </FormControl>
                    </Grid>
                    <Grid
                      item
                      xs={12}
                      md={6}
                      xl={6}
                      sx={{ alignContent: 'center' }}
                    >
                      <CustomToggle
                        name="inputOfflineOperation"
                        value={system.inputOfflineOperation}
                        handleChange={handleChange}
                        trueString="Offline"
                        falseString="Online"
                      ></CustomToggle>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12} sx={{ height: '72px' }}>
                      <h3>Parámetro cinético</h3>
                    </Grid>
                  </Grid>
                </Grid>
                <Grid item xs={12} md={12} xl={6}>
                  <Grid container spacing={2}>
                    <Grid item xs={12} md={6} xl={6} sx={{ height: '72px' }}>
                      <h3>Condiciones iniciales R101</h3>
                    </Grid>
                    <Grid
                      item
                      xs={12}
                      md={6}
                      xl={6}
                      sx={{ alignContent: 'center' }}
                    >
                      <CustomToggle
                        name="initialAnalysisConditions101.enabled"
                        value={system.initialAnalysisConditionsR101.enabled}
                        handleChange={handleChange}
                        disabled={system.inputOfflineOperation}
                      ></CustomToggle>
                    </Grid>
                    <Grid item xs={12} md={6} xl={6}>
                      <CustomNumberField
                        variable={
                          system.initialAnalysisConditionsR101
                            .totalSubstrateSolids
                        }
                        name="initialAnalysisConditions101.totalSubstrateSolids"
                        handleChange={handleChange}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={6} xl={6}>
                      <CustomNumberField
                        variable={
                          system.initialAnalysisConditionsR101
                            .volatileSubstrateSolids
                        }
                        name="initialAnalysisConditions101.volatileSubstrateSolids"
                        handleChange={handleChange}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={6} xl={6}>
                      <CustomNumberField
                        variable={
                          system.initialAnalysisConditionsR101.substrateDensity
                        }
                        name="initialAnalysisConditions101.substrateDensity"
                        handleChange={handleChange}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={6} xl={6}>
                      <CustomNumberField
                        variable={
                          system.initialAnalysisConditionsR101
                            .atomicCarbonSubstrateConcetration
                        }
                        name="initialAnalysisConditions101.atomicCarbonSubstrateConcetration"
                        handleChange={handleChange}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={6} xl={6}>
                      <CustomNumberField
                        variable={
                          system.initialAnalysisConditionsR101
                            .atomicHydrogenSubstrateConcetration
                        }
                        name="initialAnalysisConditions101.atomicHydrogenSubstrateConcetration"
                        handleChange={handleChange}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={6} xl={6}>
                      <CustomNumberField
                        variable={
                          system.initialAnalysisConditionsR101
                            .atomicOxygenSubstrateConcetration
                        }
                        name="initialAnalysisConditions101.atomicOxygenSubstrateConcetration"
                        handleChange={handleChange}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={6} xl={6}>
                      <CustomNumberField
                        variable={
                          system.initialAnalysisConditionsR101
                            .atomicNitrogenSubstrateConcetration
                        }
                        name="initialAnalysisConditions101.atomicNitrogenSubstrateConcetration"
                        handleChange={handleChange}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={6} xl={6}>
                      <CustomNumberField
                        variable={
                          system.initialAnalysisConditionsR101
                            .atomicSulfurSubstrateConcetration
                        }
                        name="initialAnalysisConditions101.atomicSulfurSubstrateConcetration"
                        handleChange={handleChange}
                      ></CustomNumberField>
                    </Grid>
                  </Grid>
                </Grid>
                <Grid item xs={12} md={12} xl={6}>
                  <Grid container spacing={2}>
                    <Grid item xs={12} md={6} xl={6} sx={{ height: '72px' }}>
                      <h3>Condiciones iniciales R102</h3>
                    </Grid>
                    <Grid
                      item
                      xs={12}
                      md={6}
                      xl={6}
                      sx={{ alignContent: 'center' }}
                    >
                      <CustomToggle
                        name="initialAnalysisConditions102.enabled"
                        value={system.initialAnalysisConditionsR102.enabled}
                        handleChange={handleChange}
                        disabled={system.inputOfflineOperation}
                      ></CustomToggle>
                    </Grid>
                    <Grid item xs={12} md={6} xl={6}>
                      <CustomNumberField
                        variable={
                          system.initialAnalysisConditionsR102
                            .totalSubstrateSolids
                        }
                        name="initialAnalysisConditions102.totalSubstrateSolids"
                        handleChange={handleChange}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={6} xl={6}>
                      <CustomNumberField
                        variable={
                          system.initialAnalysisConditionsR102
                            .volatileSubstrateSolids
                        }
                        name="initialAnalysisConditions102.volatileSubstrateSolids"
                        handleChange={handleChange}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={6} xl={6}>
                      <CustomNumberField
                        variable={
                          system.initialAnalysisConditionsR102.substrateDensity
                        }
                        name="initialAnalysisConditions102.substrateDensity"
                        handleChange={handleChange}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={6} xl={6}>
                      <CustomNumberField
                        variable={
                          system.initialAnalysisConditionsR102
                            .atomicCarbonSubstrateConcetration
                        }
                        name="initialAnalysisConditions102.atomicCarbonSubstrateConcetration"
                        handleChange={handleChange}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={6} xl={6}>
                      <CustomNumberField
                        variable={
                          system.initialAnalysisConditionsR102
                            .atomicHydrogenSubstrateConcetration
                        }
                        name="initialAnalysisConditions102.atomicHydrogenSubstrateConcetration"
                        handleChange={handleChange}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={6} xl={6}>
                      <CustomNumberField
                        variable={
                          system.initialAnalysisConditionsR102
                            .atomicOxygenSubstrateConcetration
                        }
                        name="initialAnalysisConditions102.atomicOxygenSubstrateConcetration"
                        handleChange={handleChange}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={6} xl={6}>
                      <CustomNumberField
                        variable={
                          system.initialAnalysisConditionsR102
                            .atomicNitrogenSubstrateConcetration
                        }
                        name="initialAnalysisConditions102.atomicNitrogenSubstrateConcetration"
                        handleChange={handleChange}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={6} xl={6}>
                      <CustomNumberField
                        variable={
                          system.initialAnalysisConditionsR102
                            .atomicSulfurSubstrateConcetration
                        }
                        name="initialAnalysisConditions102.atomicSulfurSubstrateConcetration"
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
            <Grid item xs={12} md={6} xl={6}>
              <Grid container spacing={2}>
                <Grid item xs={12} md={6} xl={6} sx={{ height: '72px' }}>
                  <h3>Condiciones del sustrato</h3>
                </Grid>
                <Grid
                  item
                  xs={12}
                  md={6}
                  xl={6}
                  sx={{ alignContent: 'center' }}
                >
                  <CustomToggle
                    name="inputSubstrateConditions"
                    value={system.inputSubstrateConditions}
                    handleChange={handleChange}
                    disabled={system.inputOfflineOperation}
                  ></CustomToggle>
                </Grid>
                <Grid item xs={12} md={6} xl={6}>
                  <Grid container spacing={2}>
                    <Grid item xs={12} md={12} xl={12} sx={{ height: '72px' }}>
                      <h4>Análisis elemental</h4>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={system.inputElementalAnalysisCarbonContent}
                        name="inputElementalAnalysisCarbonContent"
                        handleChange={handleChange}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={system.inputElementalAnalysisHydrogenContent}
                        name="inputElementalAnalysisHydrogenContent"
                        handleChange={handleChange}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={system.inputElementalAnalysisOxygenContent}
                        name="inputElementalAnalysisOxygenContent"
                        handleChange={handleChange}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={system.inputElementalAnalysisNitrogenContent}
                        name="inputElementalAnalysisNitrogenContent"
                        handleChange={handleChange}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={system.inputElementalAnalysisSulfurContent}
                        name="inputElementalAnalysisSulfurContent"
                        handleChange={handleChange}
                      ></CustomNumberField>
                    </Grid>
                  </Grid>
                </Grid>
                <Grid item xs={12} md={6} xl={6}>
                  <Grid container spacing={2}>
                    <Grid item xs={12} md={12} xl={12} sx={{ height: '72px' }}>
                      <h4>Análisis próximo</h4>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={system.inputProximateAnalysisTotalSolids}
                        name="inputProximateAnalysisTotalSolids"
                        handleChange={handleChange}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={system.inputProximateAnalysisVolatileSolids}
                        name="inputProximateAnalysisVolatileSolids"
                        handleChange={handleChange}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={system.inputProximateAnalysisDensity}
                        name="inputProximateAnalysisDensity"
                        handleChange={handleChange}
                      ></CustomNumberField>
                    </Grid>
                  </Grid>
                </Grid>
              </Grid>
            </Grid>
            <Grid item xs={12} md={3} xl={3}>
              <Grid container spacing={2}>
                <Grid item xs={12} md={6} xl={6}>
                  <h3>Bomba P-104</h3>
                </Grid>
                <Grid item xs={12} md={6} xl={6} alignContent={'center'}>
                  <CustomToggle
                    name="inputPump104"
                    value={system.inputPump104}
                    handleChange={handleChange}
                    disabled={system.inputOfflineOperation}
                  ></CustomToggle>
                </Grid>
                <Grid item xs={12} md={12} xl={12}>
                  <CustomNumberField
                    variable={system.inputPump104HydraulicRetentionTime}
                    name="inputPump104HydraulicRetentionTime"
                    handleChange={handleChange}
                  ></CustomNumberField>
                </Grid>
                <Grid item xs={12} md={12} xl={12}>
                  <CustomNumberField
                    variable={system.inputPump104StartTime}
                    name="inputPump104StartTime"
                    handleChange={handleChange}
                  ></CustomNumberField>
                </Grid>
                <Grid item xs={12} md={12} xl={12}>
                  <CustomNumberField
                    variable={system.inputPump104StartsPerDay}
                    name="inputPump104StartsPerDay"
                    handleChange={handleChange}
                  ></CustomNumberField>
                </Grid>
              </Grid>
              {system.inputOperationMode !== OperationModeType.Modo1 && (
                <Grid container spacing={2}>
                  <Grid item xs={12} md={6} xl={6}>
                    <h3>Bomba P-101</h3>
                  </Grid>
                  <Grid item xs={12} md={6} xl={6} alignContent={'center'}>
                    <CustomToggle
                      name="inputPump101"
                      value={system.inputPump101}
                      handleChange={handleChange}
                      disabled={
                        system.inputOfflineOperation ||
                        system.inputOperationMode === OperationModeType.Modo3 ||
                        system.inputOperationMode === OperationModeType.Modo4
                      }
                    ></CustomToggle>
                  </Grid>
                  <Grid item xs={12} md={12} xl={12}>
                    <CustomNumberField
                      variable={system.inputPump101Flow}
                      name="inputPump101Flow"
                      handleChange={handleChange}
                    ></CustomNumberField>
                  </Grid>
                  <Grid item xs={12} md={12} xl={12}>
                    <CustomNumberField
                      variable={system.inputPump101StartTime}
                      name="inputPump101StartTime"
                      handleChange={handleChange}
                    ></CustomNumberField>
                  </Grid>
                  <Grid item xs={12} md={12} xl={12}>
                    <CustomNumberField
                      variable={system.inputPump101StartsPerDay}
                      name="inputPump101StartsPerDay"
                      handleChange={handleChange}
                    ></CustomNumberField>
                  </Grid>
                </Grid>
              )}
              {(system.inputOperationMode === OperationModeType.Modo4 ||
                system.inputOperationMode === OperationModeType.Modo5) && (
                <Grid container spacing={2}>
                  <Grid item xs={12} md={6} xl={6}>
                    <h3>Bomba P-102</h3>
                  </Grid>
                  <Grid item xs={12} md={6} xl={6} alignContent={'center'}>
                    <CustomToggle
                      name="inputPump102"
                      value={system.inputPump102}
                      handleChange={handleChange}
                      disabled={system.inputOfflineOperation}
                    ></CustomToggle>
                  </Grid>
                  <Grid item xs={12} md={12} xl={12}>
                    <CustomNumberField
                      variable={system.inputPump102Flow}
                      name="inputPump102Flow"
                      handleChange={handleChange}
                    ></CustomNumberField>
                  </Grid>
                  <Grid item xs={12} md={12} xl={12}>
                    <CustomNumberField
                      variable={system.inputPump102StartTime}
                      name="inputPump102StartTime"
                      handleChange={handleChange}
                    ></CustomNumberField>
                  </Grid>
                  <Grid item xs={12} md={12} xl={12}>
                    <CustomNumberField
                      variable={system.inputPump102StartsPerDay}
                      name="inputPump102StartsPerDay"
                      handleChange={handleChange}
                    ></CustomNumberField>
                  </Grid>
                </Grid>
              )}
              <Grid item xs={12} md={12} xl={12}>
                <h3>Temperatura R-101</h3>
                <ToggleCustomNumberField
                  variable={system.inputTemperatureR101}
                  name="inputTemperature101"
                  handleChange={handleChange}
                  disabled={system.inputOfflineOperation}
                ></ToggleCustomNumberField>
              </Grid>
              {(system.inputOperationMode === OperationModeType.Modo3 ||
                system.inputOperationMode === OperationModeType.Modo4 ||
                system.inputOperationMode === OperationModeType.Modo5) && (
                <Grid item xs={12} md={12} xl={12}>
                  <h3>Temperatura R-102</h3>
                  <ToggleCustomNumberField
                    variable={system.inputTemperatureR102}
                    name="inputTemperature102"
                    handleChange={handleChange}
                    disabled={system.inputOfflineOperation}
                  ></ToggleCustomNumberField>
                </Grid>
              )}
            </Grid>
          </Grid>
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
          {playerControl}
        </Grid>
        <Grid item xs={12} md={12} xl={12}>
          <Grid container spacing={2}>
            <Grid item xs={12} md={6} xl={3}>
              <FormControl fullWidth>
                <InputLabel>Biogás</InputLabel>
                <Select
                  label="Biogás"
                  value={system.diagramBiogas}
                  name="diagramBiogas"
                  onChange={(e: any) => handleChange(e)}
                >
                  {Object.keys(DiagramBiogasType).map((key) => (
                    <MenuItem key={key} value={key}>
                      {getValueByKey(DiagramBiogasText, key)}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={6} xl={3}>
              <FormControl fullWidth>
                <InputLabel>Unidades</InputLabel>
                <Select
                  label="Unidades"
                  value={system.diagramBiogasUnit}
                  name="diagramBiogasUnit"
                  onChange={(e: any) => handleChange(e)}
                >
                  {Object.keys(DiagramBiogasUnitType).map((key) => (
                    <MenuItem key={key} value={key}>
                      {getValueByKey(DiagramBiogasUnitText, key)}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={6} xl={3}>
              <FormControl fullWidth>
                <InputLabel>Componentes</InputLabel>
                <Select
                  label="Componentes"
                  value={system.diagramCompound}
                  name="diagramCompound"
                  onChange={(e: any) => handleChange(e)}
                >
                  {Object.keys(DiagramCompoundType).map((key) => (
                    <MenuItem key={key} value={key}>
                      {getValueByKey(DiagramCompoundText, key)}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={6} xl={3}>
              <FormControl fullWidth>
                <InputLabel>Humedad</InputLabel>
                <Select
                  label="Humedad"
                  value={system.diagramHumidity}
                  name="diagramHumidity"
                  onChange={(e: any) => handleChange(e)}
                >
                  {Object.keys(DiagramHumidityType).map((key) => (
                    <MenuItem key={key} value={key}>
                      {getValueByKey(DiagramHumidityText, key)}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
          </Grid>
        </Grid>

        <Grid item xs={12} md={12} xl={12}>
          <BiogasDiagram
            biogas={system}
            data={data}
            isPlaying={isPlaying}
            diagramVariables={diagramVariables}
          ></BiogasDiagram>
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

export default Biogas;
