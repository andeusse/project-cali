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
import React, { useEffect, useState } from 'react';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import {
  BIOGAS,
  BIOGAS_DIAGRAM_VARIABLES,
  BiogasOutput,
  BiogasParameters,
  OperationModeType,
  SpeedLawOrderType,
} from '../../types/models/biogas';
import Diagram from '../../components/UI/Diagram';
import { useControlPlayer } from '../../hooks/useControlPlayer';
import { setFormState } from '../../utils/setFormState';
import PlayerControls from '../../components/UI/PlayerControls';
import CustomNumberField from '../../components/UI/CustomNumberField';
import TimeGraphs from '../../components/models/common/TimeGraphs';
import ToggleCustomNumberField from '../../components/UI/ToggleCustomNumberField';
import CustomToggle from '../../components/UI/CustomToggle';

import biogasDiagram from '../../assets/biogas/biogasPlantDiagram.svg';
import biogasIllustration from '../../assets/illustrations/biogas.jpg';
import ErrorDialog from '../../components/UI/ErrorDialog';

type Props = {};

const Biogas = (props: Props) => {
  const [biogas, setBiogas] = useState<BiogasParameters>(BIOGAS);
  const [isImageExpanded, setIsImageExpanded] = useState(true);
  const [isParametersExpanded, setIsParametersExpanded] = useState(true);
  const [isOpen, setIsOpen] = useState(false);

  const [data, graphs, isPlaying, error, onPlay, onPause, onStop] =
    useControlPlayer<BiogasParameters, BiogasOutput>('biogas', biogas);

  useEffect(() => {
    setBiogas((o) => {
      return { ...o, disableParameters: isPlaying };
    });
  }, [isPlaying]);

  useEffect(() => {
    if (error !== '') {
      setIsOpen(true);
    }
  }, [error]);

  const handleChange = (e: any, variableName?: string) => {
    const newState = setFormState<BiogasParameters>(e, biogas, variableName);
    if (newState) {
      setBiogas(newState as BiogasParameters);
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
                src={biogasIllustration}
                alt="biogasIllustration"
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
                <Grid item xs={12} md={12} xl={12}>
                  <FormControl fullWidth>
                    <TextField
                      label="Nombre"
                      value={biogas.name}
                      name="name"
                      autoComplete="off"
                      onChange={handleChange}
                      disabled={biogas.disableParameters}
                    />
                  </FormControl>
                </Grid>
                <Grid item xs={12} md={6} xl={3}>
                  <Grid container spacing={2}>
                    <Grid item xs={12} md={12} xl={12} sx={{ height: '72px' }}>
                      <h3>Operación planta</h3>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={biogas.anaerobicReactorVolume1}
                        name="anaerobicReactorVolume1"
                        handleChange={handleChange}
                        disabled={biogas.disableParameters}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={biogas.anaerobicReactorVolume2}
                        name="anaerobicReactorVolume2"
                        handleChange={handleChange}
                        disabled={biogas.disableParameters}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12} sx={{ height: '72px' }}>
                      <h3>Tanques de biogás</h3>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={biogas.biogasTankVolume1}
                        name="biogasTankVolume1"
                        handleChange={handleChange}
                        disabled={biogas.disableParameters}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={biogas.biogasTankVolume2}
                        name="biogasTankVolume2"
                        handleChange={handleChange}
                        disabled={biogas.disableParameters}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={biogas.biogasTankVolume3}
                        name="biogasTankVolume3"
                        handleChange={handleChange}
                        disabled={biogas.disableParameters}
                      ></CustomNumberField>
                    </Grid>
                  </Grid>
                </Grid>
                <Grid item xs={12} md={6} xl={4}>
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
                        value={biogas.inputDigitalTwin}
                        handleChange={handleChange}
                        trueString="Gemelo on"
                        falseString="Gemelo off"
                        disabled={biogas.disableParameters}
                      ></CustomToggle>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={biogas.inputDigitalTwinStepTime}
                        name="inputDigitalTwinStepTime"
                        handleChange={handleChange}
                        disabled={biogas.disableParameters}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={biogas.inputDigitalTwinTrainingTime}
                        name="inputDigitalTwinTrainingTime"
                        handleChange={handleChange}
                        disabled={biogas.disableParameters}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={biogas.inputDigitalTwinForecastTime}
                        name="inputDigitalTwinForecastTime"
                        handleChange={handleChange}
                        disabled={biogas.disableParameters}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12} sx={{ height: '72px' }}>
                      <h3>Parámetro cinético</h3>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={biogas.inputKineticParameterInitialValue}
                        name="inputKineticParameterInitialValue"
                        handleChange={handleChange}
                        disabled={biogas.disableParameters}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12} sx={{ height: '72px' }}>
                      <h3>Ley de velocidad</h3>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <FormControl fullWidth>
                        <InputLabel>Orden</InputLabel>
                        <Select
                          label="Orden"
                          value={biogas.inputSpeedLawOrder}
                          name="inputSpeedLawOrder"
                          onChange={(e: any) => handleChange(e)}
                          disabled={biogas.inputDigitalTwin}
                        >
                          {Object.values(SpeedLawOrderType).map((key) => (
                            <MenuItem key={key} value={key}>
                              {key}
                            </MenuItem>
                          ))}
                        </Select>
                      </FormControl>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={biogas.inputSpeedLawExponentialFactor}
                        name="inputSpeedLawExponentialFactor"
                        handleChange={handleChange}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={biogas.inputSpeedLawStartEnergy}
                        name="inputSpeedLawStartEnergy"
                        handleChange={handleChange}
                      ></CustomNumberField>
                    </Grid>
                  </Grid>
                </Grid>
                <Grid item xs={12} md={12} xl={5}>
                  <Grid container spacing={2}>
                    <Grid item xs={12} md={12} xl={12} sx={{ height: '72px' }}>
                      <h3>Operación planta</h3>
                    </Grid>
                    <Grid item xs={12} md={6} xl={6}>
                      <FormControl fullWidth>
                        <InputLabel>Modo de operación</InputLabel>
                        <Select
                          label="Modo de operación"
                          value={biogas.inputOperationMode}
                          name="inputOperationMode"
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
                        value={biogas.inputOfflineOperation}
                        handleChange={handleChange}
                        trueString="Offline"
                        falseString="Online"
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
                        value={biogas.inputSubstrateConditions}
                        handleChange={handleChange}
                        disabled={biogas.inputOfflineOperation}
                      ></CustomToggle>
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
                          <h4>Análisis elemental</h4>
                        </Grid>
                        <Grid item xs={12} md={12} xl={12}>
                          <CustomNumberField
                            variable={
                              biogas.inputElementalAnalysisCarbonContent
                            }
                            name="inputElementalAnalysisCarbonContent"
                            handleChange={handleChange}
                          ></CustomNumberField>
                        </Grid>
                        <Grid item xs={12} md={12} xl={12}>
                          <CustomNumberField
                            variable={
                              biogas.inputElementalAnalysisHydrogenContent
                            }
                            name="inputElementalAnalysisHydrogenContent"
                            handleChange={handleChange}
                          ></CustomNumberField>
                        </Grid>
                        <Grid item xs={12} md={12} xl={12}>
                          <CustomNumberField
                            variable={
                              biogas.inputElementalAnalysisOxygenContent
                            }
                            name="inputElementalAnalysisOxygenContent"
                            handleChange={handleChange}
                          ></CustomNumberField>
                        </Grid>
                        <Grid item xs={12} md={12} xl={12}>
                          <CustomNumberField
                            variable={
                              biogas.inputElementalAnalysisNitrogenContent
                            }
                            name="inputElementalAnalysisNitrogenContent"
                            handleChange={handleChange}
                          ></CustomNumberField>
                        </Grid>
                        <Grid item xs={12} md={12} xl={12}>
                          <CustomNumberField
                            variable={
                              biogas.inputElementalAnalysisSulfurContent
                            }
                            name="inputElementalAnalysisSulfurContent"
                            handleChange={handleChange}
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
                          <h4>Análisis próximo</h4>
                        </Grid>
                        <Grid item xs={12} md={12} xl={12}>
                          <CustomNumberField
                            variable={biogas.inputProximateAnalysisTotalSolids}
                            name="inputProximateAnalysisTotalSolids"
                            handleChange={handleChange}
                          ></CustomNumberField>
                        </Grid>
                        <Grid item xs={12} md={12} xl={12}>
                          <CustomNumberField
                            variable={
                              biogas.inputProximateAnalysisVolatileSolids
                            }
                            name="inputProximateAnalysisVolatileSolids"
                            handleChange={handleChange}
                          ></CustomNumberField>
                        </Grid>
                        <Grid item xs={12} md={12} xl={12}>
                          <CustomNumberField
                            variable={biogas.inputProximateAnalysisDensity}
                            name="inputProximateAnalysisDensity"
                            handleChange={handleChange}
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
        <Grid item xs={12} md={12} xl={12}>
          <Grid container spacing={2}>
            <Grid item xs={12} md={2.5} xl={2.5}>
              <Grid container spacing={2}>
                <Grid item xs={12} md={6} xl={6}>
                  <h3>Bomba P-104</h3>
                </Grid>
                <Grid item xs={12} md={6} xl={6} alignContent={'center'}>
                  <CustomToggle
                    name="inputPump104"
                    value={biogas.inputPump104}
                    handleChange={handleChange}
                    disabled={biogas.inputOfflineOperation}
                  ></CustomToggle>
                </Grid>
                <Grid item xs={12} md={12} xl={12}>
                  <CustomNumberField
                    variable={biogas.inputPump104HydraulicRetentionTime}
                    name="inputPump104HydraulicRetentionTime"
                    handleChange={handleChange}
                  ></CustomNumberField>
                </Grid>
                <Grid item xs={12} md={12} xl={12}>
                  <CustomNumberField
                    variable={biogas.inputPump104StartTime}
                    name="inputPump104StartTime"
                    handleChange={handleChange}
                  ></CustomNumberField>
                </Grid>
                <Grid item xs={12} md={12} xl={12}>
                  <CustomNumberField
                    variable={biogas.inputPump104StartsPerDay}
                    name="inputPump104StartsPerDay"
                    handleChange={handleChange}
                  ></CustomNumberField>
                </Grid>
              </Grid>
              {biogas.inputOperationMode !== OperationModeType.Modo1 && (
                <Grid container spacing={2}>
                  <Grid item xs={12} md={6} xl={6}>
                    <h3>Bomba P-101</h3>
                  </Grid>
                  <Grid item xs={12} md={6} xl={6} alignContent={'center'}>
                    <CustomToggle
                      name="inputPump101"
                      value={biogas.inputPump101}
                      handleChange={handleChange}
                      disabled={
                        biogas.inputOfflineOperation ||
                        biogas.inputOperationMode === OperationModeType.Modo3 ||
                        biogas.inputOperationMode === OperationModeType.Modo4
                      }
                    ></CustomToggle>
                  </Grid>
                  <Grid item xs={12} md={12} xl={12}>
                    <CustomNumberField
                      variable={biogas.inputPump101Flow}
                      name="inputPump101Flow"
                      handleChange={handleChange}
                    ></CustomNumberField>
                  </Grid>
                  <Grid item xs={12} md={12} xl={12}>
                    <CustomNumberField
                      variable={biogas.inputPump101StartTime}
                      name="inputPump101StartTime"
                      handleChange={handleChange}
                    ></CustomNumberField>
                  </Grid>
                  <Grid item xs={12} md={12} xl={12}>
                    <CustomNumberField
                      variable={biogas.inputPump101StartsPerDay}
                      name="inputPump101StartsPerDay"
                      handleChange={handleChange}
                    ></CustomNumberField>
                  </Grid>
                </Grid>
              )}
              {biogas.inputOperationMode === OperationModeType.Modo4 && (
                <Grid container spacing={2}>
                  <Grid item xs={12} md={6} xl={6}>
                    <h3>Bomba P-102</h3>
                  </Grid>
                  <Grid item xs={12} md={6} xl={6} alignContent={'center'}>
                    <CustomToggle
                      name="inputPump102"
                      value={biogas.inputPump102}
                      handleChange={handleChange}
                      disabled={biogas.inputOfflineOperation}
                    ></CustomToggle>
                  </Grid>
                  <Grid item xs={12} md={12} xl={12}>
                    <CustomNumberField
                      variable={biogas.inputPump102Flow}
                      name="inputPump102Flow"
                      handleChange={handleChange}
                    ></CustomNumberField>
                  </Grid>
                  <Grid item xs={12} md={12} xl={12}>
                    <CustomNumberField
                      variable={biogas.inputPump102StartTime}
                      name="inputPump102StartTime"
                      handleChange={handleChange}
                    ></CustomNumberField>
                  </Grid>
                  <Grid item xs={12} md={12} xl={12}>
                    <CustomNumberField
                      variable={biogas.inputPump102StartsPerDay}
                      name="inputPump102StartsPerDay"
                      handleChange={handleChange}
                    ></CustomNumberField>
                  </Grid>
                </Grid>
              )}
              <Grid item xs={12} md={12} xl={12}>
                <h3>Temperatura R-101</h3>
                <ToggleCustomNumberField
                  variable={biogas.inputTemperature101}
                  name="inputTemperature101"
                  handleChange={handleChange}
                  disabled={biogas.inputOfflineOperation}
                ></ToggleCustomNumberField>
              </Grid>
              {(biogas.inputOperationMode === OperationModeType.Modo3 ||
                biogas.inputOperationMode === OperationModeType.Modo4) && (
                <Grid item xs={12} md={12} xl={12}>
                  <h3>Temperatura R-102</h3>
                  <ToggleCustomNumberField
                    variable={biogas.inputTemperature102}
                    name="inputTemperature102"
                    handleChange={handleChange}
                    disabled={biogas.inputOfflineOperation}
                  ></ToggleCustomNumberField>
                </Grid>
              )}
            </Grid>
            <Grid item xs={12} md={9.5} xl={9.5}>
              {playerControl}
              <Diagram<BiogasOutput>
                diagram={biogasDiagram}
                data={data}
                variables={BIOGAS_DIAGRAM_VARIABLES}
                width={255}
                height={150}
              ></Diagram>
            </Grid>
          </Grid>
        </Grid>
        {graphs !== undefined && biogas.timeMultiplier && (
          <>
            <Grid item xs={12} md={12} xl={12}>
              <TimeGraphs
                timeMultiplier={biogas.timeMultiplier}
                handleChange={handleChange}
                graphs={graphs}
                variables={BIOGAS_DIAGRAM_VARIABLES}
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
