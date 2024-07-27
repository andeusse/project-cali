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
  OperationModelType,
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
                    <Grid item xs={12} md={6} xl={12} sx={{ height: '72px' }}>
                      <h3>Operación planta</h3>
                    </Grid>
                    <Grid item xs={12} md={6} xl={12}>
                      <CustomNumberField
                        variable={system.anaerobicReactorVolume1}
                        name="anaerobicReactorVolume1"
                        handleChange={handleChange}
                        disabled={system.disableParameters}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={6} xl={12}>
                      <CustomNumberField
                        variable={system.anaerobicReactorVolume2}
                        name="anaerobicReactorVolume2"
                        handleChange={handleChange}
                        disabled={system.disableParameters}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={6} xl={12}>
                      <FormControl fullWidth>
                        <InputLabel>Modo de operación</InputLabel>
                        <Select
                          label="Modo de operación"
                          value={system.inputOperationMode}
                          name="inputOperationMode"
                          disabled={system.disableParameters}
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
                <Grid item xs={12} md={6} xl={2.5}>
                  <Grid container spacing={2}>
                    <Grid item xs={12} md={6} xl={6} sx={{ height: '72px' }}>
                      <h3>Gemelo</h3>
                    </Grid>
                    <Grid
                      item
                      xs={12}
                      md={6}
                      xl={6}
                      sx={{ alignContent: 'center' }}
                    >
                      <CustomToggle
                        name="digitalTwinState"
                        value={system.digitalTwinState}
                        handleChange={handleChange}
                        trueString="Gemelo on"
                        falseString="Gemelo off"
                        disabled={system.disableParameters}
                      ></CustomToggle>
                    </Grid>
                    <Grid item xs={12} md={6} xl={12}>
                      <CustomNumberField
                        variable={system.digitalTwinStepTime}
                        name="digitalTwinStepTime"
                        handleChange={handleChange}
                        disabled={system.disableParameters}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={6} xl={12}>
                      <CustomNumberField
                        variable={system.digitalTwinForecastTime}
                        name="digitalTwinForecastTime"
                        handleChange={handleChange}
                        disabled={system.disableParameters}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12} sx={{ height: '72px' }}>
                      <h3>Parámetro cinético</h3>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <FormControl fullWidth>
                        <InputLabel>Modelo cinético</InputLabel>
                        <Select
                          label="Modelo cinético"
                          value={system.operationModelType}
                          name="operationModelType"
                          disabled={system.disableParameters}
                          onChange={(e: any) => handleChange(e)}
                        >
                          {Object.values(OperationModelType).map((key) => (
                            <MenuItem key={key} value={key}>
                              {key}
                            </MenuItem>
                          ))}
                        </Select>
                      </FormControl>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12} sx={{ height: '72px' }}>
                      <h3>Reactor 1 R101</h3>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={system.exponentialFactorR101}
                        name="exponentialFactorR101"
                        handleChange={handleChange}
                        disabled={system.disableParameters}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={system.activationEnergyR101}
                        name="activationEnergyR101"
                        handleChange={handleChange}
                        disabled={system.disableParameters}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={system.lambdaR101}
                        name="lambdaR101"
                        handleChange={handleChange}
                        disabled={system.disableParameters}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12} sx={{ height: '72px' }}>
                      <h3>Reactor 2 R102</h3>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={system.exponentialFactorR102}
                        name="exponentialFactorR102"
                        handleChange={handleChange}
                        disabled={system.disableParameters}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={system.activationEnergyR102}
                        name="activationEnergyR102"
                        handleChange={handleChange}
                        disabled={system.disableParameters}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={system.lambdaR102}
                        name="lambdaR102"
                        handleChange={handleChange}
                        disabled={system.disableParameters}
                      ></CustomNumberField>
                    </Grid>
                  </Grid>
                </Grid>
                <Grid item xs={12} md={6} xl={2.5}>
                  <Grid container spacing={2}>
                    <Grid item xs={12} md={12} xl={12} sx={{ height: '72px' }}>
                      <h3>Sistema de tratamiento de biogás</h3>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12} sx={{ height: '72px' }}>
                      <h3>Torre 1</h3>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={system.difussionCoefficientTower1}
                        name="difussionCoefficientTower1"
                        handleChange={handleChange}
                        disabled={system.disableParameters}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={system.adsorbentWeightTower1}
                        name="adsorbentWeightTower1"
                        handleChange={handleChange}
                        disabled={system.disableParameters}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={system.lengthTower1}
                        name="lengthTower1"
                        handleChange={handleChange}
                        disabled={system.disableParameters}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12} sx={{ height: '72px' }}>
                      <h3>Torre 2</h3>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={system.difussionCoefficientTower2}
                        name="difussionCoefficientTower2"
                        handleChange={handleChange}
                        disabled={system.disableParameters}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={system.adsorbentWeightTower2}
                        name="adsorbentWeightTower2"
                        handleChange={handleChange}
                        disabled={system.disableParameters}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={system.lengthTower2}
                        name="lengthTower2"
                        handleChange={handleChange}
                        disabled={system.disableParameters}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12} sx={{ height: '72px' }}>
                      <h3>Torre 3</h3>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={system.difussionCoefficientTower3}
                        name="difussionCoefficientTower3"
                        handleChange={handleChange}
                        disabled={system.disableParameters}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={system.adsorbentWeightTower3}
                        name="adsorbentWeightTower3"
                        handleChange={handleChange}
                        disabled={system.disableParameters}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={system.lengthTower3}
                        name="lengthTower3"
                        handleChange={handleChange}
                        disabled={system.disableParameters}
                      ></CustomNumberField>
                    </Grid>
                  </Grid>
                </Grid>
                <Grid item xs={12} md={6} xl={4.5}>
                  <Grid container spacing={2}>
                    <Grid item xs={12} md={12} xl={12} sx={{ height: '72px' }}>
                      <h3>Condiciones iniciales</h3>
                    </Grid>
                    <Grid item xs={12} md={6} xl={6}>
                      <Grid container spacing={2}>
                        <Grid
                          item
                          xs={12}
                          md={12}
                          xl={12}
                          sx={{ height: '72px' }}
                        >
                          <h3>Reactor 1 R101</h3>
                        </Grid>
                        <Grid item xs={12} md={12} xl={12}>
                          <CustomNumberField
                            variable={
                              system.initialAnalysisConditionsR101
                                .totalSubstrateSolids
                            }
                            name="initialAnalysisConditionsR101.totalSubstrateSolids"
                            handleChange={handleChange}
                            disabled={system.disableParameters}
                          ></CustomNumberField>
                        </Grid>
                        <Grid item xs={12} md={12} xl={12}>
                          <CustomNumberField
                            variable={
                              system.initialAnalysisConditionsR101
                                .volatileSubstrateSolids
                            }
                            name="initialAnalysisConditionsR101.volatileSubstrateSolids"
                            handleChange={handleChange}
                            disabled={system.disableParameters}
                          ></CustomNumberField>
                        </Grid>
                        <Grid item xs={12} md={12} xl={12}>
                          <CustomNumberField
                            variable={
                              system.initialAnalysisConditionsR101
                                .substrateDensity
                            }
                            name="initialAnalysisConditionsR101.substrateDensity"
                            handleChange={handleChange}
                            disabled={system.disableParameters}
                          ></CustomNumberField>
                        </Grid>
                        <Grid
                          item
                          xs={12}
                          md={12}
                          xl={12}
                          sx={{ height: '72px' }}
                        >
                          <h3>Análisis elemental</h3>
                        </Grid>
                        <Grid item xs={12} md={12} xl={12}>
                          <CustomNumberField
                            variable={
                              system.initialAnalysisConditionsR101
                                .atomicCarbonSubstrateConcetration
                            }
                            name="initialAnalysisConditionsR101.atomicCarbonSubstrateConcetration"
                            handleChange={handleChange}
                            disabled={system.disableParameters}
                          ></CustomNumberField>
                        </Grid>
                        <Grid item xs={12} md={12} xl={12}>
                          <CustomNumberField
                            variable={
                              system.initialAnalysisConditionsR101
                                .atomicHydrogenSubstrateConcetration
                            }
                            name="initialAnalysisConditionsR101.atomicHydrogenSubstrateConcetration"
                            handleChange={handleChange}
                            disabled={system.disableParameters}
                          ></CustomNumberField>
                        </Grid>
                        <Grid item xs={12} md={12} xl={12}>
                          <CustomNumberField
                            variable={
                              system.initialAnalysisConditionsR101
                                .atomicOxygenSubstrateConcetration
                            }
                            name="initialAnalysisConditionsR101.atomicOxygenSubstrateConcetration"
                            handleChange={handleChange}
                            disabled={system.disableParameters}
                          ></CustomNumberField>
                        </Grid>
                        <Grid item xs={12} md={12} xl={12}>
                          <CustomNumberField
                            variable={
                              system.initialAnalysisConditionsR101
                                .atomicNitrogenSubstrateConcetration
                            }
                            name="initialAnalysisConditionsR101.atomicNitrogenSubstrateConcetration"
                            handleChange={handleChange}
                            disabled={system.disableParameters}
                          ></CustomNumberField>
                        </Grid>
                        <Grid item xs={12} md={12} xl={12}>
                          <CustomNumberField
                            variable={
                              system.initialAnalysisConditionsR101
                                .atomicSulfurSubstrateConcetration
                            }
                            name="initialAnalysisConditionsR101.atomicSulfurSubstrateConcetration"
                            handleChange={handleChange}
                            disabled={system.disableParameters}
                          ></CustomNumberField>
                        </Grid>
                      </Grid>
                    </Grid>
                    <Grid item xs={12} md={6} xl={6}>
                      <Grid container spacing={2}>
                        <Grid
                          item
                          xs={12}
                          md={12}
                          xl={12}
                          sx={{ height: '72px' }}
                        >
                          <h3>Reactor 2 R102</h3>
                        </Grid>
                        <Grid item xs={12} md={12} xl={12}>
                          <CustomNumberField
                            variable={
                              system.initialAnalysisConditionsR102
                                .totalSubstrateSolids
                            }
                            name="initialAnalysisConditionsR102.totalSubstrateSolids"
                            handleChange={handleChange}
                            disabled={system.disableParameters}
                          ></CustomNumberField>
                        </Grid>
                        <Grid item xs={12} md={12} xl={12}>
                          <CustomNumberField
                            variable={
                              system.initialAnalysisConditionsR102
                                .volatileSubstrateSolids
                            }
                            name="initialAnalysisConditionsR102.volatileSubstrateSolids"
                            handleChange={handleChange}
                            disabled={system.disableParameters}
                          ></CustomNumberField>
                        </Grid>
                        <Grid item xs={12} md={12} xl={12}>
                          <CustomNumberField
                            variable={
                              system.initialAnalysisConditionsR102
                                .substrateDensity
                            }
                            name="initialAnalysisConditionsR102.substrateDensity"
                            handleChange={handleChange}
                            disabled={system.disableParameters}
                          ></CustomNumberField>
                        </Grid>
                        <Grid
                          item
                          xs={12}
                          md={12}
                          xl={12}
                          sx={{ height: '72px' }}
                        >
                          <h3>Análisis elemental</h3>
                        </Grid>
                        <Grid item xs={12} md={12} xl={12}>
                          <CustomNumberField
                            variable={
                              system.initialAnalysisConditionsR102
                                .atomicCarbonSubstrateConcetration
                            }
                            name="initialAnalysisConditionsR102.atomicCarbonSubstrateConcetration"
                            handleChange={handleChange}
                            disabled={system.disableParameters}
                          ></CustomNumberField>
                        </Grid>
                        <Grid item xs={12} md={12} xl={12}>
                          <CustomNumberField
                            variable={
                              system.initialAnalysisConditionsR102
                                .atomicHydrogenSubstrateConcetration
                            }
                            name="initialAnalysisConditionsR102.atomicHydrogenSubstrateConcetration"
                            handleChange={handleChange}
                            disabled={system.disableParameters}
                          ></CustomNumberField>
                        </Grid>
                        <Grid item xs={12} md={12} xl={12}>
                          <CustomNumberField
                            variable={
                              system.initialAnalysisConditionsR102
                                .atomicOxygenSubstrateConcetration
                            }
                            name="initialAnalysisConditionsR102.atomicOxygenSubstrateConcetration"
                            handleChange={handleChange}
                            disabled={system.disableParameters}
                          ></CustomNumberField>
                        </Grid>
                        <Grid item xs={12} md={12} xl={12}>
                          <CustomNumberField
                            variable={
                              system.initialAnalysisConditionsR102
                                .atomicNitrogenSubstrateConcetration
                            }
                            name="initialAnalysisConditionsR102.atomicNitrogenSubstrateConcetration"
                            handleChange={handleChange}
                            disabled={system.disableParameters}
                          ></CustomNumberField>
                        </Grid>
                        <Grid item xs={12} md={12} xl={12}>
                          <CustomNumberField
                            variable={
                              system.initialAnalysisConditionsR102
                                .atomicSulfurSubstrateConcetration
                            }
                            name="initialAnalysisConditionsR102.atomicSulfurSubstrateConcetration"
                            handleChange={handleChange}
                            disabled={system.disableParameters}
                          ></CustomNumberField>
                        </Grid>
                      </Grid>
                    </Grid>
                  </Grid>
                </Grid>
              </Grid>
            </AccordionDetails>
          </Accordion>
        </Grid>

        <Grid item xs={12} md={6} xl={6}>
          <h3>Variables de operación</h3>
        </Grid>

        <Grid item xs={12} md={12} xl={12}>
          <Grid container spacing={2}>
            <Grid item xs={12} md={6} xl={4.5}>
              <Grid container spacing={2}>
                <Grid item xs={12} md={6} xl={6} sx={{ height: '72px' }}>
                  <h3>Variables de entrada</h3>
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
                    disabled={!system.digitalTwinState}
                  ></CustomToggle>
                </Grid>
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
            <Grid item xs={12} md={6} xl={2.5}>
              <Grid container spacing={2}>
                <Grid item xs={12} md={6} xl={6} sx={{ height: '72px' }}>
                  <h3>Premezcla</h3>
                </Grid>
                <Grid
                  item
                  xs={12}
                  md={6}
                  xl={6}
                  sx={{ alignContent: 'center' }}
                >
                  <CustomToggle
                    name="inputMixTK100"
                    value={system.inputMixTK100}
                    handleChange={handleChange}
                    disabled={system.inputOfflineOperation}
                  ></CustomToggle>
                </Grid>
                <Grid item xs={12} md={12} xl={12}>
                  <CustomNumberField
                    variable={system.inputSpeedMixTK100}
                    name="inputSpeedMixTK100"
                    handleChange={handleChange}
                  ></CustomNumberField>
                </Grid>
                <Grid item xs={12} md={12} xl={12}>
                  <CustomNumberField
                    variable={system.inputStartsPerDayMixTK100}
                    name="inputStartsPerDayMixTK100"
                    handleChange={handleChange}
                  ></CustomNumberField>
                </Grid>
                <Grid item xs={12} md={12} xl={12}>
                  <CustomNumberField
                    variable={system.inputStartTimeMixTK100}
                    name="inputStartTimeMixTK100"
                    handleChange={handleChange}
                  ></CustomNumberField>
                </Grid>
                <Grid item xs={12} md={6} xl={6} sx={{ height: '72px' }}>
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
                    variable={system.inputPump104StartsPerDay}
                    name="inputPump104StartsPerDay"
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
              </Grid>
            </Grid>
            <Grid item xs={12} md={6} xl={2.5}>
              <Grid container spacing={2}>
                {system.inputOperationMode === OperationModeType.Modo2 && (
                  <>
                    <Grid item xs={12} md={6} xl={6} sx={{ height: '72px' }}>
                      <h3>Bomba P-101</h3>
                    </Grid>
                    <Grid item xs={12} md={6} xl={6} alignContent={'center'}>
                      <CustomToggle
                        name="inputPump101"
                        value={system.inputPump101}
                        handleChange={handleChange}
                        disabled={system.inputOfflineOperation}
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
                        variable={system.inputPump101StartsPerDay}
                        name="inputPump101StartsPerDay"
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
                  </>
                )}
                {(system.inputOperationMode === OperationModeType.Modo4 ||
                  system.inputOperationMode === OperationModeType.Modo5) && (
                  <>
                    <Grid item xs={12} md={6} xl={6} sx={{ height: '72px' }}>
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
                        variable={system.inputPump102StartsPerDay}
                        name="inputPump102StartsPerDay"
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
                  </>
                )}
              </Grid>
            </Grid>
            <Grid item xs={12} md={6} xl={2.5}>
              <Grid container spacing={2}>
                <Grid item xs={12} md={6} xl={6} sx={{ height: '72px' }}>
                  <h3>Agitación R101</h3>
                </Grid>
                <Grid item xs={12} md={6} xl={6} alignContent={'center'}>
                  <CustomToggle
                    name="inputMixR101"
                    value={system.inputMixR101}
                    handleChange={handleChange}
                    disabled={system.inputOfflineOperation}
                  ></CustomToggle>
                </Grid>
                <Grid item xs={12} md={12} xl={12}>
                  <CustomNumberField
                    variable={system.inputSpeedMixR101}
                    name="inputSpeedMixR101"
                    handleChange={handleChange}
                  ></CustomNumberField>
                </Grid>
                <Grid item xs={12} md={12} xl={12}>
                  <CustomNumberField
                    variable={system.inputStartsPerDayMixR101}
                    name="inputStartsPerDayMixR101"
                    handleChange={handleChange}
                  ></CustomNumberField>
                </Grid>
                <Grid item xs={12} md={12} xl={12}>
                  <CustomNumberField
                    variable={system.inputStartTimeMixR101}
                    name="inputStartTimeMixR101"
                    handleChange={handleChange}
                  ></CustomNumberField>
                </Grid>
                <Grid item xs={12} md={12} xl={12}>
                  <ToggleCustomNumberField
                    variable={system.inputPHR101}
                    name="inputPHR101"
                    handleChange={handleChange}
                    disabled={system.inputOfflineOperation}
                  ></ToggleCustomNumberField>
                </Grid>
                <Grid item xs={12} md={12} xl={12}>
                  <ToggleCustomNumberField
                    variable={system.inputTemperatureR101}
                    name="inputTemperatureR101"
                    handleChange={handleChange}
                    disabled={system.inputOfflineOperation}
                  ></ToggleCustomNumberField>
                </Grid>

                {(system.inputOperationMode === OperationModeType.Modo3 ||
                  system.inputOperationMode === OperationModeType.Modo4 ||
                  system.inputOperationMode === OperationModeType.Modo5) && (
                  <>
                    <Grid item xs={12} md={6} xl={6} sx={{ height: '72px' }}>
                      <h3>Agitación R102</h3>
                    </Grid>
                    <Grid item xs={12} md={6} xl={6} alignContent={'center'}>
                      <CustomToggle
                        name="inputMixR102"
                        value={system.inputMixR102}
                        handleChange={handleChange}
                        disabled={system.inputOfflineOperation}
                      ></CustomToggle>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={system.inputSpeedMixR102}
                        name="inputSpeedMixR102"
                        handleChange={handleChange}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={system.inputStartsPerDayMixR102}
                        name="inputStartsPerDayMixR102"
                        handleChange={handleChange}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={system.inputStartTimeMixR102}
                        name="inputStartTimeMixR102"
                        handleChange={handleChange}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <ToggleCustomNumberField
                        variable={system.inputPHR102}
                        name="inputPHR102"
                        handleChange={handleChange}
                        disabled={system.inputOfflineOperation}
                      ></ToggleCustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <ToggleCustomNumberField
                        variable={system.inputTemperatureR102}
                        name="inputTemperatureR102"
                        handleChange={handleChange}
                        disabled={system.inputOfflineOperation}
                      ></ToggleCustomNumberField>
                    </Grid>
                  </>
                )}
              </Grid>
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
