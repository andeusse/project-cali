import React, { useEffect, useState } from 'react';
import {
  BiochemicalMethanePotentialOutput,
  BiochemicalMethanePotentialParameters,
  BMP,
  BMP_VARIABLES,
  DiagramBiogasMeasurementMethodText,
  DiagramBiogasMeasurementMethodType,
  DiagramBiogasText,
  DiagramBiogasType,
  DiagramBiogasUnitText,
  DiagramBiogasUnitType,
  DiagramCompoundUnitText,
  DiagramCompoundUnitType,
  DosageText,
  DosageType,
  MixRuleText,
  MixRuleType,
  PlantOperationText,
  PlantOperationType,
} from '../../types/models/biochemicalMethanePotential';
import { useControlPlayer } from '../../hooks/useControlPlayer';
import { setFormState } from '../../utils/setFormState';
import saveAs from 'file-saver';
import PlayerControls from '../../components/UI/PlayerControls';
import ErrorDialog from '../../components/UI/ErrorDialog';
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
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import FileUploadIcon from '@mui/icons-material/FileUpload';
import BMPIllustration from '../../assets/illustrations/biogas.png';
import { getValueByKey } from '../../utils/getValueByKey';
import CustomNumberField from '../../components/UI/CustomNumberField';
import CustomToggle from '../../components/UI/CustomToggle';
import { OperationModelType } from '../../types/common';
import TimeGraphs from '../../components/models/common/TimeGraphs';
import BiochemicalMethanePotentialDiagram from '../../components/models/diagram/BiochemicalMethanePotentialDiagram';
import ToggleCustomNumberField from '../../components/UI/ToggleCustomNumberField';

type Props = {};

const BiochemicalMethanePotential = (props: Props) => {
  const [system, setSystem] = useState<BiochemicalMethanePotentialParameters>({
    ...BMP,
  });
  const [isImageExpanded, setIsImageExpanded] = useState(true);
  const [isParametersExpanded, setIsParametersExpanded] = useState(true);
  const [isOpen, setIsOpen] = useState(false);

  const [data, charts, isPlaying, error, onPlay, onPause, onStop, setError] =
    useControlPlayer<
      BiochemicalMethanePotentialParameters,
      BiochemicalMethanePotentialOutput
    >('bmp', system);

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
    const newState = setFormState<BiochemicalMethanePotentialParameters>(
      e,
      system,
      variableName
    );
    if (newState) {
      setSystem(newState as BiochemicalMethanePotentialParameters);
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
        const jsonData: BiochemicalMethanePotentialParameters = JSON.parse(
          e.target.result
        ) as BiochemicalMethanePotentialParameters;
        if ('plantOperation' in jsonData) {
          setSystem(jsonData);
        } else {
          setError('El archivo no corresponde a un gemelo digital de BMP');
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
                src={BMPIllustration}
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
                {system.plantOperation === PlantOperationType.SideA && (
                  <Grid item xs={12} md={12} xl={6}>
                    <Grid container spacing={2}>
                      <Grid item xs={12} md={6} xl={6}>
                        <Grid container spacing={2}>
                          <Grid
                            item
                            xs={12}
                            md={12}
                            xl={12}
                            sx={{ height: '72px' }}
                          >
                            <h3>Operación planta</h3>
                          </Grid>
                          <Grid item xs={12} md={6} xl={12}>
                            <FormControl fullWidth>
                              <InputLabel>Proceso</InputLabel>
                              <Select
                                label="Proceso"
                                value={system.plantOperation}
                                name="plantOperation"
                                disabled={system.disableParameters}
                                onChange={(e: any) => handleChange(e)}
                              >
                                {Object.values(PlantOperationType).map(
                                  (key) => (
                                    <MenuItem key={key} value={key}>
                                      {getValueByKey(PlantOperationText, key)}
                                    </MenuItem>
                                  )
                                )}
                              </Select>
                            </FormControl>
                          </Grid>{' '}
                          <Grid item xs={12} md={6} xl={12}>
                            <FormControl fullWidth>
                              <InputLabel>Método medición</InputLabel>
                              <Select
                                label="Método medición"
                                value={system.measurementMethodSideA}
                                name="measurementMethodSideA"
                                disabled={system.disableParameters}
                                onChange={(e: any) => handleChange(e)}
                              >
                                {Object.values(
                                  DiagramBiogasMeasurementMethodType
                                ).map((key) => (
                                  <MenuItem key={key} value={key}>
                                    {getValueByKey(
                                      DiagramBiogasMeasurementMethodText,
                                      key
                                    )}
                                  </MenuItem>
                                ))}
                              </Select>
                            </FormControl>
                          </Grid>
                          <Grid
                            item
                            xs={12}
                            md={12}
                            xl={12}
                            sx={{ height: '72px' }}
                          >
                            <h3>Tanques de biogás</h3>
                          </Grid>
                          <Grid item xs={12} md={6} xl={12}>
                            <CustomNumberField
                              variable={system.rxnVolumeSideA}
                              name="rxnVolumeSideA"
                              handleChange={handleChange}
                              disabled={system.disableParameters}
                            ></CustomNumberField>
                          </Grid>
                          <Grid item xs={12} md={6} xl={12}>
                            <CustomNumberField
                              variable={system.freeVolumeSideA}
                              name="freeVolumeSideA"
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
                            md={6}
                            xl={6}
                            sx={{ height: '72px' }}
                          >
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
                              value={system.stateSelectionSideA}
                              name="stateSelectionSideA"
                              handleChange={handleChange}
                              trueString="Offline"
                              falseString="Online"
                              disabled={system.disableParameters}
                            ></CustomToggle>
                          </Grid>
                          <Grid item xs={12} md={6} xl={12}>
                            <CustomNumberField
                              variable={system.timeStepSideA}
                              name="timeStepSideA"
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
                            <h3>Parámetros cinéticos</h3>
                          </Grid>
                          <Grid item xs={12} md={6} xl={12}>
                            <FormControl fullWidth>
                              <InputLabel>Proceso</InputLabel>
                              <Select
                                label="Proceso"
                                value={system.modelSelectionSideA}
                                name="modelSelectionSideA"
                                disabled={system.disableParameters}
                                onChange={(e: any) => handleChange(e)}
                              >
                                {Object.values(OperationModelType).map(
                                  (key) => (
                                    <MenuItem key={key} value={key}>
                                      {key}
                                    </MenuItem>
                                  )
                                )}
                              </Select>
                            </FormControl>
                          </Grid>
                          <Grid item xs={12} md={6} xl={12}>
                            <CustomNumberField
                              variable={system.kineticKSideA}
                              name="kineticKSideA"
                              handleChange={handleChange}
                              disabled={system.disableParameters}
                            ></CustomNumberField>
                          </Grid>
                          <Grid item xs={12} md={6} xl={12}>
                            <CustomNumberField
                              variable={system.kineticEaSideA}
                              name="kineticEaSideA"
                              handleChange={handleChange}
                              disabled={system.disableParameters}
                            ></CustomNumberField>
                          </Grid>
                          <Grid item xs={12} md={6} xl={12}>
                            <CustomNumberField
                              variable={system.kineticLambdaSideA}
                              name="kineticLambdaSideA"
                              handleChange={handleChange}
                              disabled={system.disableParameters}
                            ></CustomNumberField>
                          </Grid>
                        </Grid>
                      </Grid>
                      {!system.stateSelectionSideA && (
                        <Grid item xs={12} md={12} xl={12}>
                          <Grid container spacing={2}>
                            <Grid
                              item
                              xs={12}
                              md={6}
                              xl={6}
                              sx={{ height: '72px' }}
                            >
                              <h3>Composiciones del biogás</h3>
                            </Grid>
                            <Grid
                              item
                              xs={12}
                              md={6}
                              xl={6}
                              sx={{ alignContent: 'center' }}
                            >
                              <CustomToggle
                                value={system.manualBiogasCompositionSideA}
                                name="manualBiogasCompositionSideA"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.stateSelectionSideA
                                }
                              ></CustomToggle>
                            </Grid>
                            <Grid item xs={12} md={6} xl={2.4}>
                              <Grid container spacing={2}>
                                <Grid
                                  item
                                  xs={12}
                                  md={6}
                                  xl={6}
                                  sx={{ height: '72px' }}
                                >
                                  <h3>R-101</h3>
                                </Grid>
                                <Grid item xs={12} md={6} xl={12}>
                                  <CustomNumberField
                                    variable={system.methaneR101}
                                    name="methaneR101"
                                    handleChange={handleChange}
                                    disabled={
                                      system.disableParameters ||
                                      !system.manualBiogasCompositionSideA
                                    }
                                  ></CustomNumberField>
                                </Grid>
                                <Grid item xs={12} md={6} xl={12}>
                                  <CustomNumberField
                                    variable={system.carbonDioxideR101}
                                    name="carbonDioxideR101"
                                    handleChange={handleChange}
                                    disabled={
                                      system.disableParameters ||
                                      !system.manualBiogasCompositionSideA
                                    }
                                  ></CustomNumberField>
                                </Grid>
                                <Grid item xs={12} md={6} xl={12}>
                                  <CustomNumberField
                                    variable={system.oxygenR101}
                                    name="oxygenR101"
                                    handleChange={handleChange}
                                    disabled={
                                      system.disableParameters ||
                                      !system.manualBiogasCompositionSideA
                                    }
                                  ></CustomNumberField>
                                </Grid>
                                <Grid item xs={12} md={6} xl={12}>
                                  <CustomNumberField
                                    variable={system.sulfurHydrogenR101}
                                    name="sulfurHydrogenR101"
                                    handleChange={handleChange}
                                    disabled={
                                      system.disableParameters ||
                                      !system.manualBiogasCompositionSideA
                                    }
                                  ></CustomNumberField>
                                </Grid>
                                <Grid item xs={12} md={6} xl={12}>
                                  <CustomNumberField
                                    variable={system.hydrogenR101}
                                    name="hydrogenR101"
                                    handleChange={handleChange}
                                    disabled={
                                      system.disableParameters ||
                                      !system.manualBiogasCompositionSideA
                                    }
                                  ></CustomNumberField>
                                </Grid>
                              </Grid>
                            </Grid>
                            <Grid item xs={12} md={6} xl={2.4}>
                              <Grid container spacing={2}>
                                <Grid
                                  item
                                  xs={12}
                                  md={6}
                                  xl={6}
                                  sx={{ height: '72px' }}
                                >
                                  <h3>R-102</h3>
                                </Grid>
                                <Grid item xs={12} md={6} xl={12}>
                                  <CustomNumberField
                                    variable={system.methaneR102}
                                    name="methaneR102"
                                    handleChange={handleChange}
                                    disabled={
                                      system.disableParameters ||
                                      !system.manualBiogasCompositionSideA
                                    }
                                  ></CustomNumberField>
                                </Grid>
                                <Grid item xs={12} md={6} xl={12}>
                                  <CustomNumberField
                                    variable={system.carbonDioxideR102}
                                    name="carbonDioxideR102"
                                    handleChange={handleChange}
                                    disabled={
                                      system.disableParameters ||
                                      !system.manualBiogasCompositionSideA
                                    }
                                  ></CustomNumberField>
                                </Grid>
                                <Grid item xs={12} md={6} xl={12}>
                                  <CustomNumberField
                                    variable={system.oxygenR102}
                                    name="oxygenR102"
                                    handleChange={handleChange}
                                    disabled={
                                      system.disableParameters ||
                                      !system.manualBiogasCompositionSideA
                                    }
                                  ></CustomNumberField>
                                </Grid>
                                <Grid item xs={12} md={6} xl={12}>
                                  <CustomNumberField
                                    variable={system.sulfurHydrogenR102}
                                    name="sulfurHydrogenR102"
                                    handleChange={handleChange}
                                    disabled={
                                      system.disableParameters ||
                                      !system.manualBiogasCompositionSideA
                                    }
                                  ></CustomNumberField>
                                </Grid>
                                <Grid item xs={12} md={6} xl={12}>
                                  <CustomNumberField
                                    variable={system.hydrogenR102}
                                    name="hydrogenR102"
                                    handleChange={handleChange}
                                    disabled={
                                      system.disableParameters ||
                                      !system.manualBiogasCompositionSideA
                                    }
                                  ></CustomNumberField>
                                </Grid>
                              </Grid>
                            </Grid>
                            <Grid item xs={12} md={6} xl={2.4}>
                              <Grid container spacing={2}>
                                <Grid
                                  item
                                  xs={12}
                                  md={6}
                                  xl={6}
                                  sx={{ height: '72px' }}
                                >
                                  <h3>R-103</h3>
                                </Grid>
                                <Grid item xs={12} md={6} xl={12}>
                                  <CustomNumberField
                                    variable={system.methaneR103}
                                    name="methaneR103"
                                    handleChange={handleChange}
                                    disabled={
                                      system.disableParameters ||
                                      !system.manualBiogasCompositionSideA
                                    }
                                  ></CustomNumberField>
                                </Grid>
                                <Grid item xs={12} md={6} xl={12}>
                                  <CustomNumberField
                                    variable={system.carbonDioxideR103}
                                    name="carbonDioxideR103"
                                    handleChange={handleChange}
                                    disabled={
                                      system.disableParameters ||
                                      !system.manualBiogasCompositionSideA
                                    }
                                  ></CustomNumberField>
                                </Grid>
                                <Grid item xs={12} md={6} xl={12}>
                                  <CustomNumberField
                                    variable={system.oxygenR103}
                                    name="oxygenR103"
                                    handleChange={handleChange}
                                    disabled={
                                      system.disableParameters ||
                                      !system.manualBiogasCompositionSideA
                                    }
                                  ></CustomNumberField>
                                </Grid>
                                <Grid item xs={12} md={6} xl={12}>
                                  <CustomNumberField
                                    variable={system.sulfurHydrogenR103}
                                    name="sulfurHydrogenR103"
                                    handleChange={handleChange}
                                    disabled={
                                      system.disableParameters ||
                                      !system.manualBiogasCompositionSideA
                                    }
                                  ></CustomNumberField>
                                </Grid>
                                <Grid item xs={12} md={6} xl={12}>
                                  <CustomNumberField
                                    variable={system.hydrogenR103}
                                    name="hydrogenR103"
                                    handleChange={handleChange}
                                    disabled={
                                      system.disableParameters ||
                                      !system.manualBiogasCompositionSideA
                                    }
                                  ></CustomNumberField>
                                </Grid>
                              </Grid>
                            </Grid>
                            <Grid item xs={12} md={6} xl={2.4}>
                              <Grid container spacing={2}>
                                <Grid
                                  item
                                  xs={12}
                                  md={6}
                                  xl={6}
                                  sx={{ height: '72px' }}
                                >
                                  <h3>R-104</h3>
                                </Grid>
                                <Grid item xs={12} md={6} xl={12}>
                                  <CustomNumberField
                                    variable={system.methaneR104}
                                    name="methaneR104"
                                    handleChange={handleChange}
                                    disabled={
                                      system.disableParameters ||
                                      !system.manualBiogasCompositionSideA
                                    }
                                  ></CustomNumberField>
                                </Grid>
                                <Grid item xs={12} md={6} xl={12}>
                                  <CustomNumberField
                                    variable={system.carbonDioxideR104}
                                    name="carbonDioxideR104"
                                    handleChange={handleChange}
                                    disabled={
                                      system.disableParameters ||
                                      !system.manualBiogasCompositionSideA
                                    }
                                  ></CustomNumberField>
                                </Grid>
                                <Grid item xs={12} md={6} xl={12}>
                                  <CustomNumberField
                                    variable={system.oxygenR104}
                                    name="oxygenR104"
                                    handleChange={handleChange}
                                    disabled={
                                      system.disableParameters ||
                                      !system.manualBiogasCompositionSideA
                                    }
                                  ></CustomNumberField>
                                </Grid>
                                <Grid item xs={12} md={6} xl={12}>
                                  <CustomNumberField
                                    variable={system.sulfurHydrogenR104}
                                    name="sulfurHydrogenR104"
                                    handleChange={handleChange}
                                    disabled={
                                      system.disableParameters ||
                                      !system.manualBiogasCompositionSideA
                                    }
                                  ></CustomNumberField>
                                </Grid>
                                <Grid item xs={12} md={6} xl={12}>
                                  <CustomNumberField
                                    variable={system.hydrogenR104}
                                    name="hydrogenR104"
                                    handleChange={handleChange}
                                    disabled={
                                      system.disableParameters ||
                                      !system.manualBiogasCompositionSideA
                                    }
                                  ></CustomNumberField>
                                </Grid>
                              </Grid>
                            </Grid>
                            <Grid item xs={12} md={6} xl={2.4}>
                              <Grid container spacing={2}>
                                <Grid
                                  item
                                  xs={12}
                                  md={6}
                                  xl={6}
                                  sx={{ height: '72px' }}
                                >
                                  <h3>R-105</h3>
                                </Grid>
                                <Grid item xs={12} md={6} xl={12}>
                                  <CustomNumberField
                                    variable={system.methaneR105}
                                    name="methaneR105"
                                    handleChange={handleChange}
                                    disabled={
                                      system.disableParameters ||
                                      !system.manualBiogasCompositionSideA
                                    }
                                  ></CustomNumberField>
                                </Grid>
                                <Grid item xs={12} md={6} xl={12}>
                                  <CustomNumberField
                                    variable={system.carbonDioxideR105}
                                    name="carbonDioxideR105"
                                    handleChange={handleChange}
                                    disabled={
                                      system.disableParameters ||
                                      !system.manualBiogasCompositionSideA
                                    }
                                  ></CustomNumberField>
                                </Grid>
                                <Grid item xs={12} md={6} xl={12}>
                                  <CustomNumberField
                                    variable={system.oxygenR105}
                                    name="oxygenR105"
                                    handleChange={handleChange}
                                    disabled={
                                      system.disableParameters ||
                                      !system.manualBiogasCompositionSideA
                                    }
                                  ></CustomNumberField>
                                </Grid>
                                <Grid item xs={12} md={6} xl={12}>
                                  <CustomNumberField
                                    variable={system.sulfurHydrogenR105}
                                    name="sulfurHydrogenR105"
                                    handleChange={handleChange}
                                    disabled={
                                      system.disableParameters ||
                                      !system.manualBiogasCompositionSideA
                                    }
                                  ></CustomNumberField>
                                </Grid>
                                <Grid item xs={12} md={6} xl={12}>
                                  <CustomNumberField
                                    variable={system.hydrogenR105}
                                    name="hydrogenR105"
                                    handleChange={handleChange}
                                    disabled={
                                      system.disableParameters ||
                                      !system.manualBiogasCompositionSideA
                                    }
                                  ></CustomNumberField>
                                </Grid>
                              </Grid>
                            </Grid>
                          </Grid>
                        </Grid>
                      )}
                    </Grid>
                  </Grid>
                )}
                {system.plantOperation === PlantOperationType.SideB && (
                  <Grid item xs={12} md={12} xl={6}>
                    <Grid container spacing={2}>
                      <Grid item xs={12} md={6} xl={6}>
                        <Grid container spacing={2}>
                          <Grid
                            item
                            xs={12}
                            md={12}
                            xl={12}
                            sx={{ height: '72px' }}
                          >
                            <h3>Operación planta</h3>
                          </Grid>
                          <Grid item xs={12} md={6} xl={12}>
                            <FormControl fullWidth>
                              <InputLabel>Proceso</InputLabel>
                              <Select
                                label="Proceso"
                                value={system.plantOperation}
                                name="plantOperation"
                                disabled={system.disableParameters}
                                onChange={(e: any) => handleChange(e)}
                              >
                                {Object.values(PlantOperationType).map(
                                  (key) => (
                                    <MenuItem key={key} value={key}>
                                      {getValueByKey(PlantOperationText, key)}
                                    </MenuItem>
                                  )
                                )}
                              </Select>
                            </FormControl>
                          </Grid>{' '}
                          <Grid item xs={12} md={6} xl={12}>
                            <FormControl fullWidth>
                              <InputLabel>Método medición</InputLabel>
                              <Select
                                label="Método medición"
                                value={system.measurementMethodSideB}
                                name="measurementMethodSideB"
                                disabled={system.disableParameters}
                                onChange={(e: any) => handleChange(e)}
                              >
                                {Object.values(
                                  DiagramBiogasMeasurementMethodType
                                ).map((key) => (
                                  <MenuItem key={key} value={key}>
                                    {getValueByKey(
                                      DiagramBiogasMeasurementMethodText,
                                      key
                                    )}
                                  </MenuItem>
                                ))}
                              </Select>
                            </FormControl>
                          </Grid>
                          <Grid
                            item
                            xs={12}
                            md={12}
                            xl={12}
                            sx={{ height: '72px' }}
                          >
                            <h3>Tanques de biogás</h3>
                          </Grid>
                          <Grid item xs={12} md={6} xl={12}>
                            <CustomNumberField
                              variable={system.rxnVolumeSideB}
                              name="rxnVolumeSideB"
                              handleChange={handleChange}
                              disabled={system.disableParameters}
                            ></CustomNumberField>
                          </Grid>
                          <Grid item xs={12} md={6} xl={12}>
                            <CustomNumberField
                              variable={system.freeVolumeSideB}
                              name="freeVolumeSideB"
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
                            md={6}
                            xl={6}
                            sx={{ height: '72px' }}
                          >
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
                              value={system.stateSelectionSideB}
                              name="stateSelectionSideB"
                              handleChange={handleChange}
                              trueString="Offline"
                              falseString="Online"
                              disabled={system.disableParameters}
                            ></CustomToggle>
                          </Grid>
                          <Grid item xs={12} md={6} xl={12}>
                            <CustomNumberField
                              variable={system.timeStepSideB}
                              name="timeStepSideB"
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
                            <h3>Parámetros cinéticos</h3>
                          </Grid>
                          <Grid item xs={12} md={6} xl={12}>
                            <FormControl fullWidth>
                              <InputLabel>Proceso</InputLabel>
                              <Select
                                label="Proceso"
                                value={system.modelSelectionSideB}
                                name="modelSelectionSideB"
                                disabled={system.disableParameters}
                                onChange={(e: any) => handleChange(e)}
                              >
                                {Object.values(OperationModelType).map(
                                  (key) => (
                                    <MenuItem key={key} value={key}>
                                      {key}
                                    </MenuItem>
                                  )
                                )}
                              </Select>
                            </FormControl>
                          </Grid>
                          <Grid item xs={12} md={6} xl={12}>
                            <CustomNumberField
                              variable={system.kineticKSideB}
                              name="kineticKSideB"
                              handleChange={handleChange}
                              disabled={system.disableParameters}
                            ></CustomNumberField>
                          </Grid>
                          <Grid item xs={12} md={6} xl={12}>
                            <CustomNumberField
                              variable={system.kineticEaSideB}
                              name="kineticEaSideB"
                              handleChange={handleChange}
                              disabled={system.disableParameters}
                            ></CustomNumberField>
                          </Grid>
                          <Grid item xs={12} md={6} xl={12}>
                            <CustomNumberField
                              variable={system.kineticLambdaSideB}
                              name="kineticLambdaSideB"
                              handleChange={handleChange}
                              disabled={system.disableParameters}
                            ></CustomNumberField>
                          </Grid>
                        </Grid>
                      </Grid>
                      {!system.stateSelectionSideB && (
                        <Grid item xs={12} md={12} xl={12}>
                          <Grid container spacing={2}>
                            <Grid
                              item
                              xs={12}
                              md={6}
                              xl={6}
                              sx={{ height: '72px' }}
                            >
                              <h3>Composiciones del biogás</h3>
                            </Grid>
                            <Grid
                              item
                              xs={12}
                              md={6}
                              xl={6}
                              sx={{ alignContent: 'center' }}
                            >
                              <CustomToggle
                                value={system.manualBiogasCompositionSideB}
                                name="manualBiogasCompositionSideB"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.stateSelectionSideB
                                }
                              ></CustomToggle>
                            </Grid>
                            <Grid item xs={12} md={6} xl={2.4}>
                              <Grid container spacing={2}>
                                <Grid
                                  item
                                  xs={12}
                                  md={6}
                                  xl={6}
                                  sx={{ height: '72px' }}
                                >
                                  <h3>R-106</h3>
                                </Grid>
                                <Grid item xs={12} md={6} xl={12}>
                                  <CustomNumberField
                                    variable={system.methaneR106}
                                    name="methaneR106"
                                    handleChange={handleChange}
                                    disabled={
                                      system.disableParameters ||
                                      !system.manualBiogasCompositionSideB
                                    }
                                  ></CustomNumberField>
                                </Grid>
                                <Grid item xs={12} md={6} xl={12}>
                                  <CustomNumberField
                                    variable={system.carbonDioxideR106}
                                    name="carbonDioxideR106"
                                    handleChange={handleChange}
                                    disabled={
                                      system.disableParameters ||
                                      !system.manualBiogasCompositionSideB
                                    }
                                  ></CustomNumberField>
                                </Grid>
                                <Grid item xs={12} md={6} xl={12}>
                                  <CustomNumberField
                                    variable={system.oxygenR106}
                                    name="oxygenR106"
                                    handleChange={handleChange}
                                    disabled={
                                      system.disableParameters ||
                                      !system.manualBiogasCompositionSideB
                                    }
                                  ></CustomNumberField>
                                </Grid>
                                <Grid item xs={12} md={6} xl={12}>
                                  <CustomNumberField
                                    variable={system.sulfurHydrogenR106}
                                    name="sulfurHydrogenR106"
                                    handleChange={handleChange}
                                    disabled={
                                      system.disableParameters ||
                                      !system.manualBiogasCompositionSideB
                                    }
                                  ></CustomNumberField>
                                </Grid>
                                <Grid item xs={12} md={6} xl={12}>
                                  <CustomNumberField
                                    variable={system.hydrogenR106}
                                    name="hydrogenR106"
                                    handleChange={handleChange}
                                    disabled={
                                      system.disableParameters ||
                                      !system.manualBiogasCompositionSideB
                                    }
                                  ></CustomNumberField>
                                </Grid>
                              </Grid>
                            </Grid>
                            <Grid item xs={12} md={6} xl={2.4}>
                              <Grid container spacing={2}>
                                <Grid
                                  item
                                  xs={12}
                                  md={6}
                                  xl={6}
                                  sx={{ height: '72px' }}
                                >
                                  <h3>R-107</h3>
                                </Grid>
                                <Grid item xs={12} md={6} xl={12}>
                                  <CustomNumberField
                                    variable={system.methaneR107}
                                    name="methaneR107"
                                    handleChange={handleChange}
                                    disabled={
                                      system.disableParameters ||
                                      !system.manualBiogasCompositionSideB
                                    }
                                  ></CustomNumberField>
                                </Grid>
                                <Grid item xs={12} md={6} xl={12}>
                                  <CustomNumberField
                                    variable={system.carbonDioxideR107}
                                    name="carbonDioxideR107"
                                    handleChange={handleChange}
                                    disabled={
                                      system.disableParameters ||
                                      !system.manualBiogasCompositionSideB
                                    }
                                  ></CustomNumberField>
                                </Grid>
                                <Grid item xs={12} md={6} xl={12}>
                                  <CustomNumberField
                                    variable={system.oxygenR107}
                                    name="oxygenR107"
                                    handleChange={handleChange}
                                    disabled={
                                      system.disableParameters ||
                                      !system.manualBiogasCompositionSideB
                                    }
                                  ></CustomNumberField>
                                </Grid>
                                <Grid item xs={12} md={6} xl={12}>
                                  <CustomNumberField
                                    variable={system.sulfurHydrogenR107}
                                    name="sulfurHydrogenR107"
                                    handleChange={handleChange}
                                    disabled={
                                      system.disableParameters ||
                                      !system.manualBiogasCompositionSideB
                                    }
                                  ></CustomNumberField>
                                </Grid>
                                <Grid item xs={12} md={6} xl={12}>
                                  <CustomNumberField
                                    variable={system.hydrogenR107}
                                    name="hydrogenR107"
                                    handleChange={handleChange}
                                    disabled={
                                      system.disableParameters ||
                                      !system.manualBiogasCompositionSideB
                                    }
                                  ></CustomNumberField>
                                </Grid>
                              </Grid>
                            </Grid>
                            <Grid item xs={12} md={6} xl={2.4}>
                              <Grid container spacing={2}>
                                <Grid
                                  item
                                  xs={12}
                                  md={6}
                                  xl={6}
                                  sx={{ height: '72px' }}
                                >
                                  <h3>R-108</h3>
                                </Grid>
                                <Grid item xs={12} md={6} xl={12}>
                                  <CustomNumberField
                                    variable={system.methaneR108}
                                    name="methaneR108"
                                    handleChange={handleChange}
                                    disabled={
                                      system.disableParameters ||
                                      !system.manualBiogasCompositionSideB
                                    }
                                  ></CustomNumberField>
                                </Grid>
                                <Grid item xs={12} md={6} xl={12}>
                                  <CustomNumberField
                                    variable={system.carbonDioxideR108}
                                    name="carbonDioxideR108"
                                    handleChange={handleChange}
                                    disabled={
                                      system.disableParameters ||
                                      !system.manualBiogasCompositionSideB
                                    }
                                  ></CustomNumberField>
                                </Grid>
                                <Grid item xs={12} md={6} xl={12}>
                                  <CustomNumberField
                                    variable={system.oxygenR108}
                                    name="oxygenR108"
                                    handleChange={handleChange}
                                    disabled={
                                      system.disableParameters ||
                                      !system.manualBiogasCompositionSideB
                                    }
                                  ></CustomNumberField>
                                </Grid>
                                <Grid item xs={12} md={6} xl={12}>
                                  <CustomNumberField
                                    variable={system.sulfurHydrogenR108}
                                    name="sulfurHydrogenR108"
                                    handleChange={handleChange}
                                    disabled={
                                      system.disableParameters ||
                                      !system.manualBiogasCompositionSideB
                                    }
                                  ></CustomNumberField>
                                </Grid>
                                <Grid item xs={12} md={6} xl={12}>
                                  <CustomNumberField
                                    variable={system.hydrogenR108}
                                    name="hydrogenR108"
                                    handleChange={handleChange}
                                    disabled={
                                      system.disableParameters ||
                                      !system.manualBiogasCompositionSideB
                                    }
                                  ></CustomNumberField>
                                </Grid>
                              </Grid>
                            </Grid>
                            <Grid item xs={12} md={6} xl={2.4}>
                              <Grid container spacing={2}>
                                <Grid
                                  item
                                  xs={12}
                                  md={6}
                                  xl={6}
                                  sx={{ height: '72px' }}
                                >
                                  <h3>R-109</h3>
                                </Grid>
                                <Grid item xs={12} md={6} xl={12}>
                                  <CustomNumberField
                                    variable={system.methaneR109}
                                    name="methaneR109"
                                    handleChange={handleChange}
                                    disabled={
                                      system.disableParameters ||
                                      !system.manualBiogasCompositionSideB
                                    }
                                  ></CustomNumberField>
                                </Grid>
                                <Grid item xs={12} md={6} xl={12}>
                                  <CustomNumberField
                                    variable={system.carbonDioxideR109}
                                    name="carbonDioxideR109"
                                    handleChange={handleChange}
                                    disabled={
                                      system.disableParameters ||
                                      !system.manualBiogasCompositionSideB
                                    }
                                  ></CustomNumberField>
                                </Grid>
                                <Grid item xs={12} md={6} xl={12}>
                                  <CustomNumberField
                                    variable={system.oxygenR109}
                                    name="oxygenR109"
                                    handleChange={handleChange}
                                    disabled={
                                      system.disableParameters ||
                                      !system.manualBiogasCompositionSideB
                                    }
                                  ></CustomNumberField>
                                </Grid>
                                <Grid item xs={12} md={6} xl={12}>
                                  <CustomNumberField
                                    variable={system.sulfurHydrogenR109}
                                    name="sulfurHydrogenR109"
                                    handleChange={handleChange}
                                    disabled={
                                      system.disableParameters ||
                                      !system.manualBiogasCompositionSideB
                                    }
                                  ></CustomNumberField>
                                </Grid>
                                <Grid item xs={12} md={6} xl={12}>
                                  <CustomNumberField
                                    variable={system.hydrogenR109}
                                    name="hydrogenR109"
                                    handleChange={handleChange}
                                    disabled={
                                      system.disableParameters ||
                                      !system.manualBiogasCompositionSideB
                                    }
                                  ></CustomNumberField>
                                </Grid>
                              </Grid>
                            </Grid>
                            <Grid item xs={12} md={6} xl={2.4}>
                              <Grid container spacing={2}>
                                <Grid
                                  item
                                  xs={12}
                                  md={6}
                                  xl={6}
                                  sx={{ height: '72px' }}
                                >
                                  <h3>R-110</h3>
                                </Grid>
                                <Grid item xs={12} md={6} xl={12}>
                                  <CustomNumberField
                                    variable={system.methaneR110}
                                    name="methaneR110"
                                    handleChange={handleChange}
                                    disabled={
                                      system.disableParameters ||
                                      !system.manualBiogasCompositionSideB
                                    }
                                  ></CustomNumberField>
                                </Grid>
                                <Grid item xs={12} md={6} xl={12}>
                                  <CustomNumberField
                                    variable={system.carbonDioxideR110}
                                    name="carbonDioxideR110"
                                    handleChange={handleChange}
                                    disabled={
                                      system.disableParameters ||
                                      !system.manualBiogasCompositionSideB
                                    }
                                  ></CustomNumberField>
                                </Grid>
                                <Grid item xs={12} md={6} xl={12}>
                                  <CustomNumberField
                                    variable={system.oxygenR110}
                                    name="oxygenR110"
                                    handleChange={handleChange}
                                    disabled={
                                      system.disableParameters ||
                                      !system.manualBiogasCompositionSideB
                                    }
                                  ></CustomNumberField>
                                </Grid>
                                <Grid item xs={12} md={6} xl={12}>
                                  <CustomNumberField
                                    variable={system.sulfurHydrogenR110}
                                    name="sulfurHydrogenR110"
                                    handleChange={handleChange}
                                    disabled={
                                      system.disableParameters ||
                                      !system.manualBiogasCompositionSideB
                                    }
                                  ></CustomNumberField>
                                </Grid>
                                <Grid item xs={12} md={6} xl={12}>
                                  <CustomNumberField
                                    variable={system.hydrogenR110}
                                    name="hydrogenR110"
                                    handleChange={handleChange}
                                    disabled={
                                      system.disableParameters ||
                                      !system.manualBiogasCompositionSideB
                                    }
                                  ></CustomNumberField>
                                </Grid>
                              </Grid>
                            </Grid>
                          </Grid>
                        </Grid>
                      )}
                    </Grid>
                  </Grid>
                )}
                {system.plantOperation === PlantOperationType.SideA && (
                  <Grid item xs={12} md={12} xl={6}>
                    <Grid container spacing={2}>
                      <Grid
                        item
                        xs={12}
                        md={12}
                        xl={12}
                        sx={{ height: '72px' }}
                      >
                        <h3>Condiciones del sustrato</h3>
                      </Grid>
                      <Grid item xs={12} md={6} xl={4}>
                        <CustomNumberField
                          variable={system.amountOfSubstratesSideA}
                          name="amountOfSubstratesSideA"
                          handleChange={handleChange}
                          disabled={system.disableParameters}
                          isInteger
                          disableKeyDown
                        ></CustomNumberField>
                      </Grid>
                      <Grid item xs={12} md={6} xl={4}>
                        <FormControl fullWidth>
                          <InputLabel>Regla de mezcla</InputLabel>
                          <Select
                            label="Regla de mezcla"
                            value={system.mixRuleSideA}
                            name="mixRuleSideA"
                            disabled={system.disableParameters}
                            onChange={(e: any) => handleChange(e)}
                          >
                            {Object.values(MixRuleType).map((key) => (
                              <MenuItem key={key} value={key}>
                                {getValueByKey(MixRuleText, key)}
                              </MenuItem>
                            ))}
                          </Select>
                        </FormControl>
                      </Grid>
                      <Grid item xs={12} md={6} xl={4}>
                        <CustomNumberField
                          variable={system.waterCompositionSideA}
                          name="waterCompositionSideA"
                          handleChange={handleChange}
                          disabled={system.disableParameters}
                          isInteger
                        ></CustomNumberField>
                      </Grid>
                      {system.amountOfSubstratesSideA.value >= 1 && (
                        <Grid item xs={12} md={6} xl={3}>
                          <Grid container spacing={2}>
                            <Grid
                              item
                              xs={12}
                              md={12}
                              xl={12}
                              sx={{ height: '72px' }}
                            >
                              <h3>Sustrato 1</h3>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <FormControl fullWidth>
                                <TextField
                                  label="Nombre"
                                  value={system.nameSubstrate1SideA}
                                  name="nameSubstrate1SideA"
                                  autoComplete="off"
                                  onChange={handleChange}
                                  disabled={system.disableParameters}
                                />
                              </FormControl>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.substrate1CompositionSideA}
                                name="substrate1CompositionSideA"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate1SideA === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.totalSolidsSubstrate1SideA}
                                name="totalSolidsSubstrate1SideA"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate1SideA === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.volatileSolidsSubstrate1SIdeA}
                                name="volatileSolidsSubstrate1SIdeA"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate1SideA === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.densitySubstrate1SideA}
                                name="densitySubstrate1SideA"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate1SideA === ''
                                }
                              ></CustomNumberField>
                            </Grid>
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
                                variable={system.carbonContentSubstrate1SideA}
                                name="carbonContentSubstrate1SideA"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate1SideA === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.hydrogenContentSubstrate1SideA}
                                name="hydrogenContentSubstrate1SideA"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate1SideA === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.oxygenContentSubstrate1SideA}
                                name="oxygenContentSubstrate1SideA"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate1SideA === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.nitrogenContentSubstrate1SideA}
                                name="nitrogenContentSubstrate1SideA"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate1SideA === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.sulfurContentSubstrate1SideA}
                                name="sulfurContentSubstrate1SideA"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate1SideA === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                          </Grid>
                        </Grid>
                      )}
                      {system.amountOfSubstratesSideA.value >= 2 && (
                        <Grid item xs={12} md={6} xl={3}>
                          <Grid container spacing={2}>
                            <Grid
                              item
                              xs={12}
                              md={12}
                              xl={12}
                              sx={{ height: '72px' }}
                            >
                              <h3>Sustrato 2</h3>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <FormControl fullWidth>
                                <TextField
                                  label="Nombre"
                                  value={system.nameSubstrate2SideA}
                                  name="nameSubstrate2SideA"
                                  autoComplete="off"
                                  onChange={handleChange}
                                  disabled={system.disableParameters}
                                />
                              </FormControl>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.substrate2CompositionSideA}
                                name="substrate2CompositionSideA"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate2SideA === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.totalSolidsSubstrate2SideA}
                                name="totalSolidsSubstrate2SideA"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate2SideA === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.volatileSolidsSubstrate2SideA}
                                name="volatileSolidsSubstrate2SideA"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate2SideA === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.densitySubstrate2SideA}
                                name="densitySubstrate2SideA"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate2SideA === ''
                                }
                              ></CustomNumberField>
                            </Grid>
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
                                variable={system.carbonContentSubstrate2SideA}
                                name="carbonContentSubstrate2SideA"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate2SideA === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.hydrogenContentSubstrate2SideA}
                                name="hydrogenContentSubstrate2SideA"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate2SideA === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.oxygenContentSubstrate2SideA}
                                name="oxygenContentSubstrate2SideA"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate2SideA === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.nitrogenContentSubstrate2SideA}
                                name="nitrogenContentSubstrate2SideA"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate2SideA === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.sulfurContentSubstrate2SideA}
                                name="sulfurContentSubstrate2SideA"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate2SideA === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                          </Grid>
                        </Grid>
                      )}
                      {system.amountOfSubstratesSideA.value >= 3 && (
                        <Grid item xs={12} md={6} xl={3}>
                          <Grid container spacing={2}>
                            <Grid
                              item
                              xs={12}
                              md={12}
                              xl={12}
                              sx={{ height: '72px' }}
                            >
                              <h3>Sustrato 3</h3>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <FormControl fullWidth>
                                <TextField
                                  label="Nombre"
                                  value={system.nameSubstrate3SideA}
                                  name="nameSubstrate3SideA"
                                  autoComplete="off"
                                  onChange={handleChange}
                                  disabled={system.disableParameters}
                                />
                              </FormControl>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.substrate3CompositionSideA}
                                name="substrate3CompositionSideA"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate3SideA === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.totalSolidsSubstrate3SideA}
                                name="totalSolidsSubstrate3SideA"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate3SideA === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.volatileSolidsSubstrate3SideA}
                                name="volatileSolidsSubstrate3SideA"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate3SideA === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.densitySubstrate3SideA}
                                name="densitySubstrate3SideA"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate3SideA === ''
                                }
                              ></CustomNumberField>
                            </Grid>
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
                                variable={system.carbonContentSubstrate3SideA}
                                name="carbonContentSubstrate3SideA"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate3SideA === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.hydrogenContentSubstrate3SideA}
                                name="hydrogenContentSubstrate3SideA"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate3SideA === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.oxygenContentSubstrate3SideA}
                                name="oxygenContentSubstrate3SideA"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate3SideA === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.nitrogenContentSubstrate3SideA}
                                name="nitrogenContentSubstrate3SideA"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate3SideA === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.sulfurContentSubstrate3SideA}
                                name="sulfurContentSubstrate3SideA"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate3SideA === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                          </Grid>
                        </Grid>
                      )}
                      {system.amountOfSubstratesSideA.value >= 4 && (
                        <Grid item xs={12} md={6} xl={3}>
                          <Grid container spacing={2}>
                            <Grid
                              item
                              xs={12}
                              md={12}
                              xl={12}
                              sx={{ height: '72px' }}
                            >
                              <h3>Sustrato 4</h3>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <FormControl fullWidth>
                                <TextField
                                  label="Nombre"
                                  value={system.nameSubstrate4SideA}
                                  name="nameSubstrate4SideA"
                                  autoComplete="off"
                                  onChange={handleChange}
                                  disabled={system.disableParameters}
                                />
                              </FormControl>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.substrate4CompositionSideA}
                                name="substrate4CompositionSideA"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate4SideA === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.totalSolidsSubstrate4SideA}
                                name="totalSolidsSubstrate4SideA"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate4SideA === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.volatileSolidsSubstrate4SIdeA}
                                name="volatileSolidsSubstrate4SIdeA"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate4SideA === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.densitySubstrate4SideA}
                                name="densitySubstrate4SideA"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate4SideA === ''
                                }
                              ></CustomNumberField>
                            </Grid>
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
                                variable={system.carbonContentSubstrate4SideA}
                                name="carbonContentSubstrate4SideA"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate4SideA === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.hydrogenContentSubstrate4SideA}
                                name="hydrogenContentSubstrate4SideA"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate4SideA === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.oxygenContentSubstrate4SideA}
                                name="oxygenContentSubstrate4SideA"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate4SideA === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.nitrogenContentSubstrate4SideA}
                                name="nitrogenContentSubstrate4SideA"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate4SideA === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.sulfurContentSubstrate4SideA}
                                name="sulfurContentSubstrate4SideA"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate4SideA === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                          </Grid>
                        </Grid>
                      )}
                    </Grid>
                  </Grid>
                )}
                {system.plantOperation === PlantOperationType.SideB && (
                  <Grid item xs={12} md={12} xl={6}>
                    <Grid container spacing={2}>
                      <Grid
                        item
                        xs={12}
                        md={12}
                        xl={12}
                        sx={{ height: '72px' }}
                      >
                        <h3>Condiciones del sustrato</h3>
                      </Grid>
                      <Grid item xs={12} md={6} xl={4}>
                        <CustomNumberField
                          variable={system.amountOfSubstratesSideB}
                          name="amountOfSubstratesSideB"
                          handleChange={handleChange}
                          disabled={system.disableParameters}
                          isInteger
                          disableKeyDown
                        ></CustomNumberField>
                      </Grid>
                      <Grid item xs={12} md={6} xl={4}>
                        <FormControl fullWidth>
                          <InputLabel>Regla de mezcla</InputLabel>
                          <Select
                            label="Regla de mezcla"
                            value={system.mixRuleSideB}
                            name="mixRuleSideB"
                            disabled={system.disableParameters}
                            onChange={(e: any) => handleChange(e)}
                          >
                            {Object.values(MixRuleType).map((key) => (
                              <MenuItem key={key} value={key}>
                                {getValueByKey(MixRuleText, key)}
                              </MenuItem>
                            ))}
                          </Select>
                        </FormControl>
                      </Grid>
                      <Grid item xs={12} md={6} xl={4}>
                        <CustomNumberField
                          variable={system.waterCompositionSideB}
                          name="waterCompositionSideB"
                          handleChange={handleChange}
                          disabled={system.disableParameters}
                          isInteger
                        ></CustomNumberField>
                      </Grid>
                      {system.amountOfSubstratesSideB.value >= 1 && (
                        <Grid item xs={12} md={6} xl={3}>
                          <Grid container spacing={2}>
                            <Grid
                              item
                              xs={12}
                              md={12}
                              xl={12}
                              sx={{ height: '72px' }}
                            >
                              <h3>Sustrato 1</h3>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <FormControl fullWidth>
                                <TextField
                                  label="Nombre"
                                  value={system.nameSubstrate1SideB}
                                  name="nameSubstrate1SideB"
                                  autoComplete="off"
                                  onChange={handleChange}
                                  disabled={system.disableParameters}
                                />
                              </FormControl>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.substrate1CompositionSideB}
                                name="substrate1CompositionSideB"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate1SideB === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.totalSolidsSubstrate1SideB}
                                name="totalSolidsSubstrate1SideB"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate1SideB === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.volatileSolidsSubstrate1SideB}
                                name="volatileSolidsSubstrate1SideB"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate1SideB === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.densitySubstrate1SideB}
                                name="densitySubstrate1SideB"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate1SideB === ''
                                }
                              ></CustomNumberField>
                            </Grid>
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
                                variable={system.carbonContentSubstrate1SideB}
                                name="carbonContentSubstrate1SideB"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate1SideB === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.hydrogenContentSubstrate1SideB}
                                name="hydrogenContentSubstrate1SideB"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate1SideB === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.oxygenContentSubstrate1SideB}
                                name="oxygenContentSubstrate1SideB"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate1SideB === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.nitrogenContentSubstrate1SideB}
                                name="nitrogenContentSubstrate1SideB"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate1SideB === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.sulfurContentSubstrate1SideB}
                                name="sulfurContentSubstrate1SideB"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate1SideB === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                          </Grid>
                        </Grid>
                      )}
                      {system.amountOfSubstratesSideB.value >= 2 && (
                        <Grid item xs={12} md={6} xl={3}>
                          <Grid container spacing={2}>
                            <Grid
                              item
                              xs={12}
                              md={12}
                              xl={12}
                              sx={{ height: '72px' }}
                            >
                              <h3>Sustrato 2</h3>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <FormControl fullWidth>
                                <TextField
                                  label="Nombre"
                                  value={system.nameSubstrate2SideB}
                                  name="nameSubstrate2SideB"
                                  autoComplete="off"
                                  onChange={handleChange}
                                  disabled={system.disableParameters}
                                />
                              </FormControl>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.substrate2CompositionSideB}
                                name="substrate2CompositionSideB"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate2SideB === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.totalSolidsSubstrate2SideB}
                                name="totalSolidsSubstrate2SideB"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate2SideB === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.volatileSolidsSubstrate2SideB}
                                name="volatileSolidsSubstrate2SideB"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate2SideB === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.densitySubstrate2SideB}
                                name="densitySubstrate2SideB"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate2SideB === ''
                                }
                              ></CustomNumberField>
                            </Grid>
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
                                variable={system.carbonContentSubstrate2SideB}
                                name="carbonContentSubstrate2SideB"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate2SideB === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.hydrogenContentSubstrate2SideB}
                                name="hydrogenContentSubstrate2SideB"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate2SideB === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.oxygenContentSubstrate2SideB}
                                name="oxygenContentSubstrate2SideB"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate2SideB === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.nitrogenContentSubstrate2SideB}
                                name="nitrogenContentSubstrate2SideB"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate2SideB === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.sulfurContentSubstrate2SideB}
                                name="sulfurContentSubstrate2SideB"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate2SideB === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                          </Grid>
                        </Grid>
                      )}
                      {system.amountOfSubstratesSideB.value >= 3 && (
                        <Grid item xs={12} md={6} xl={3}>
                          <Grid container spacing={2}>
                            <Grid
                              item
                              xs={12}
                              md={12}
                              xl={12}
                              sx={{ height: '72px' }}
                            >
                              <h3>Sustrato 3</h3>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <FormControl fullWidth>
                                <TextField
                                  label="Nombre"
                                  value={system.nameSubstrate3SideB}
                                  name="nameSubstrate3SideB"
                                  autoComplete="off"
                                  onChange={handleChange}
                                  disabled={system.disableParameters}
                                />
                              </FormControl>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.substrate3CompositionSideB}
                                name="substrate3CompositionSideB"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate3SideB === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.totalSolidsSubstrate3SideB}
                                name="totalSolidsSubstrate3SideB"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate3SideB === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.volatileSolidsSubstrate3SideB}
                                name="volatileSolidsSubstrate3SideB"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate3SideB === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.densitySubstrate3SideB}
                                name="densitySubstrate3SideB"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate3SideB === ''
                                }
                              ></CustomNumberField>
                            </Grid>
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
                                variable={system.carbonContentSubstrate3SideB}
                                name="carbonContentSubstrate3SideB"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate3SideB === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.hydrogenContentSubstrate3SideB}
                                name="hydrogenContentSubstrate3SideB"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate3SideB === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.oxygenContentSubstrate3SideB}
                                name="oxygenContentSubstrate3SideB"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate3SideB === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.nitrogenContentSubstrate3SideB}
                                name="nitrogenContentSubstrate3SideB"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate3SideB === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.sulfurContentSubstrate3SideB}
                                name="sulfurContentSubstrate3SideB"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate3SideB === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                          </Grid>
                        </Grid>
                      )}
                      {system.amountOfSubstratesSideB.value >= 4 && (
                        <Grid item xs={12} md={6} xl={3}>
                          <Grid container spacing={2}>
                            <Grid
                              item
                              xs={12}
                              md={12}
                              xl={12}
                              sx={{ height: '72px' }}
                            >
                              <h3>Sustrato 4</h3>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <FormControl fullWidth>
                                <TextField
                                  label="Nombre"
                                  value={system.nameSubstrate4SideB}
                                  name="nameSubstrate4SideB"
                                  autoComplete="off"
                                  onChange={handleChange}
                                  disabled={system.disableParameters}
                                />
                              </FormControl>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.substrate4CompositionSideB}
                                name="substrate4CompositionSideB"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate4SideB === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.totalSolidsSubstrate4SideB}
                                name="totalSolidsSubstrate4SideB"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate4SideB === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.volatileSolidsSubstrate4SideB}
                                name="volatileSolidsSubstrate4SideB"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate4SideB === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.densitySubstrate4SideB}
                                name="densitySubstrate4SideB"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate4SideB === ''
                                }
                              ></CustomNumberField>
                            </Grid>
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
                                variable={system.carbonContentSubstrate4SideB}
                                name="carbonContentSubstrate4SideB"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate4SideB === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.hydrogenContentSubstrate4SideB}
                                name="hydrogenContentSubstrate4SideB"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate4SideB === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.oxygenContentSubstrate4SideB}
                                name="oxygenContentSubstrate4SideB"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate4SideB === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.nitrogenContentSubstrate4SideB}
                                name="nitrogenContentSubstrate4SideB"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate4SideB === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                            <Grid item xs={12} md={12} xl={12}>
                              <CustomNumberField
                                variable={system.sulfurContentSubstrate4SideB}
                                name="sulfurContentSubstrate4SideB"
                                handleChange={handleChange}
                                disabled={
                                  system.disableParameters ||
                                  system.nameSubstrate4SideB === ''
                                }
                              ></CustomNumberField>
                            </Grid>
                          </Grid>
                        </Grid>
                      )}
                    </Grid>
                  </Grid>
                )}
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
              {system.plantOperation === PlantOperationType.SideA && (
                <Grid container spacing={2}>
                  <Grid item xs={12} md={12} xl={12}>
                    <h2>Operación planta</h2>
                  </Grid>
                  <Grid item xs={12} md={12} xl={12}>
                    <ToggleCustomNumberField
                      variable={system.testDurationSideA}
                      name="testDurationSideA"
                      handleChange={handleChange}
                      disabled={system.stateSelectionSideA}
                    ></ToggleCustomNumberField>
                  </Grid>
                  <Grid item xs={12} md={12} xl={12}>
                    <ToggleCustomNumberField
                      variable={system.TemperatureSideA}
                      name="TemperatureSideA"
                      handleChange={handleChange}
                      disabled={system.stateSelectionSideA}
                    ></ToggleCustomNumberField>
                  </Grid>
                  <Grid item xs={12} md={12} xl={12}>
                    <ToggleCustomNumberField
                      variable={system.pHSideA}
                      name="pHSideA"
                      handleChange={handleChange}
                      disabled={system.stateSelectionSideA}
                    ></ToggleCustomNumberField>
                  </Grid>
                  <Grid item xs={12} md={6} xl={6}>
                    <h4>Agitación</h4>
                  </Grid>
                  <Grid
                    item
                    xs={12}
                    md={6}
                    xl={6}
                    sx={{ alignContent: 'center' }}
                  >
                    <CustomToggle
                      value={system.mixManualSideA}
                      name="mixManualSideA"
                      handleChange={handleChange}
                      disabled={system.stateSelectionSideA}
                    ></CustomToggle>
                  </Grid>
                  <Grid item xs={12} md={12} xl={12}>
                    <CustomNumberField
                      variable={system.mixVelocitySideA}
                      name="mixVelocitySideA"
                      handleChange={handleChange}
                      disabled={!system.mixManualSideA}
                    ></CustomNumberField>
                  </Grid>
                  <Grid item xs={12} md={12} xl={12}>
                    <CustomNumberField
                      variable={system.mixTimeSideA}
                      name="mixTimeSideA"
                      handleChange={handleChange}
                      disabled={!system.mixManualSideA}
                    ></CustomNumberField>
                  </Grid>
                  <Grid item xs={12} md={12} xl={12}>
                    <CustomNumberField
                      variable={system.mixDailySideA}
                      name="mixDailySideA"
                      handleChange={handleChange}
                      isInteger
                      disabled={!system.mixManualSideA}
                    ></CustomNumberField>
                  </Grid>
                  <Grid item xs={12} md={6} xl={6}>
                    <h4>Alimentación</h4>
                  </Grid>
                  <Grid
                    item
                    xs={12}
                    md={6}
                    xl={6}
                    sx={{ alignContent: 'center' }}
                  >
                    <CustomToggle
                      value={system.feefManualSideA}
                      name="feefManualSideA"
                      handleChange={handleChange}
                      disabled={system.stateSelectionSideA}
                    ></CustomToggle>
                  </Grid>
                  <Grid item xs={12} md={6} xl={12}>
                    <FormControl fullWidth>
                      <InputLabel>Modo de operación</InputLabel>
                      <Select
                        label="Modo de operación"
                        value={system.dosificationTypeSideA}
                        name="dosificationTypeSideA"
                        disabled={!system.feefManualSideA}
                        onChange={(e: any) => handleChange(e)}
                      >
                        {Object.values(DosageType).map((key) => (
                          <MenuItem key={key} value={key}>
                            {getValueByKey(DosageText, key)}
                          </MenuItem>
                        ))}
                      </Select>
                    </FormControl>
                  </Grid>
                  <Grid item xs={12} md={12} xl={12}>
                    <CustomNumberField
                      variable={system.dosificationVolumeSideA}
                      name="dosificationVolumeSideA"
                      handleChange={handleChange}
                      disabled={!system.feefManualSideA}
                    ></CustomNumberField>
                  </Grid>
                  {system.dosificationTypeSideA === DosageType.Time && (
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={system.dailyInyectionsByTimeSideA}
                        name="dailyInyectionsByTimeSideA"
                        handleChange={handleChange}
                        isInteger
                        disabled={!system.feefManualSideA}
                      ></CustomNumberField>
                    </Grid>
                  )}
                  {system.dosificationTypeSideA === DosageType.Injection && (
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={system.dailyInyectionsSideA}
                        name="dailyInyectionsSideA"
                        handleChange={handleChange}
                        isInteger
                        disabled={!system.feefManualSideA}
                      ></CustomNumberField>
                    </Grid>
                  )}
                </Grid>
              )}
              {system.plantOperation === PlantOperationType.SideB && (
                <Grid container spacing={2}>
                  <Grid item xs={12} md={12} xl={12}>
                    <h2>Operación planta</h2>
                  </Grid>
                  <Grid item xs={12} md={12} xl={12}>
                    <ToggleCustomNumberField
                      variable={system.testDurationSideB}
                      name="testDurationSideB"
                      handleChange={handleChange}
                      disabled={system.stateSelectionSideB}
                    ></ToggleCustomNumberField>
                  </Grid>
                  <Grid item xs={12} md={12} xl={12}>
                    <ToggleCustomNumberField
                      variable={system.TemperatureSideB}
                      name="TemperatureSideB"
                      handleChange={handleChange}
                      disabled={system.stateSelectionSideB}
                    ></ToggleCustomNumberField>
                  </Grid>
                  <Grid item xs={12} md={12} xl={12}>
                    <ToggleCustomNumberField
                      variable={system.pHSideB}
                      name="pHSideB"
                      handleChange={handleChange}
                      disabled={system.stateSelectionSideB}
                    ></ToggleCustomNumberField>
                  </Grid>
                  <Grid item xs={12} md={6} xl={6}>
                    <h4>Agitación</h4>
                  </Grid>
                  <Grid
                    item
                    xs={12}
                    md={6}
                    xl={6}
                    sx={{ alignContent: 'center' }}
                  >
                    <CustomToggle
                      value={system.mixManualSideB}
                      name="mixManualSideB"
                      handleChange={handleChange}
                      disabled={system.stateSelectionSideB}
                    ></CustomToggle>
                  </Grid>
                  <Grid item xs={12} md={12} xl={12}>
                    <CustomNumberField
                      variable={system.mixVelocitySideB}
                      name="mixVelocitySideB"
                      handleChange={handleChange}
                      disabled={!system.mixManualSideB}
                    ></CustomNumberField>
                  </Grid>
                  <Grid item xs={12} md={12} xl={12}>
                    <CustomNumberField
                      variable={system.mixTimeSideB}
                      name="mixTimeSideB"
                      handleChange={handleChange}
                      disabled={!system.mixManualSideB}
                    ></CustomNumberField>
                  </Grid>
                  <Grid item xs={12} md={12} xl={12}>
                    <CustomNumberField
                      variable={system.mixDailySideB}
                      name="mixDailySideB"
                      handleChange={handleChange}
                      isInteger
                      disabled={!system.mixManualSideB}
                    ></CustomNumberField>
                  </Grid>
                  <Grid item xs={12} md={6} xl={6}>
                    <h4>Alimentación</h4>
                  </Grid>
                  <Grid
                    item
                    xs={12}
                    md={6}
                    xl={6}
                    sx={{ alignContent: 'center' }}
                  >
                    <CustomToggle
                      value={system.feefManualSideB}
                      name="feefManualSideB"
                      handleChange={handleChange}
                    ></CustomToggle>
                  </Grid>
                  <Grid item xs={12} md={6} xl={12}>
                    <FormControl fullWidth>
                      <InputLabel>Modo de operación</InputLabel>
                      <Select
                        label="Modo de operación"
                        value={system.dosificationTypeSideB}
                        name="dosificationTypeSideB"
                        disabled={!system.feefManualSideB}
                        onChange={(e: any) => handleChange(e)}
                      >
                        {Object.values(DosageType).map((key) => (
                          <MenuItem key={key} value={key}>
                            {getValueByKey(DosageText, key)}
                          </MenuItem>
                        ))}
                      </Select>
                    </FormControl>
                  </Grid>
                  <Grid item xs={12} md={12} xl={12}>
                    <CustomNumberField
                      variable={system.dosificationVolumeSideB}
                      name="dosificationVolumeSideB"
                      handleChange={handleChange}
                      disabled={!system.feefManualSideB}
                    ></CustomNumberField>
                  </Grid>
                  {system.dosificationTypeSideB === DosageType.Time && (
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={system.dailyInyectionsByTimeSideB}
                        name="dailyInyectionsByTimeSideB"
                        handleChange={handleChange}
                        isInteger
                        disabled={!system.feefManualSideB}
                      ></CustomNumberField>
                    </Grid>
                  )}
                  {system.dosificationTypeSideB === DosageType.Injection && (
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={system.dailyInyectionsSideB}
                        name="dailyInyectionsSideB"
                        handleChange={handleChange}
                        isInteger
                        disabled={!system.feefManualSideB}
                      ></CustomNumberField>
                    </Grid>
                  )}
                </Grid>
              )}
            </Grid>
            <Grid item xs={12} md={9.5} xl={9.5}>
              <Grid container spacing={2}>
                <Grid item xs={12} md={12} xl={12}>
                  {playerControl}
                </Grid>
                {system.plantOperation === PlantOperationType.SideA && (
                  <Grid item xs={12} md={12} xl={12}>
                    <Grid container spacing={2}>
                      {system.measurementMethodSideA ===
                        DiagramBiogasMeasurementMethodType.Pressure && (
                        <>
                          <Grid item xs={12} md={6} xl={3}>
                            <FormControl fullWidth>
                              <InputLabel>Biogás</InputLabel>
                              <Select
                                label="Biogás"
                                value={system.biogasVisualizationSideA}
                                name="biogasVisualizationSideA"
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
                                value={system.biogasVisualizationUnitsSideA}
                                name="biogasVisualizationUnitsSideA"
                                onChange={(e: any) => handleChange(e)}
                              >
                                {Object.keys(DiagramBiogasUnitType).map(
                                  (key) => (
                                    <MenuItem key={key} value={key}>
                                      {getValueByKey(
                                        DiagramBiogasUnitText,
                                        key
                                      )}
                                    </MenuItem>
                                  )
                                )}
                              </Select>
                            </FormControl>
                          </Grid>
                          <Grid item xs={12} md={6} xl={3}>
                            <FormControl fullWidth>
                              <InputLabel>Energía</InputLabel>
                              <Select
                                label="Energía"
                                value={system.measurementMethodSideA}
                                name="measurementMethodSideA"
                                onChange={(e: any) => handleChange(e)}
                              >
                                {Object.keys(
                                  DiagramBiogasMeasurementMethodType
                                ).map((key) => (
                                  <MenuItem key={key} value={key}>
                                    {getValueByKey(
                                      DiagramBiogasMeasurementMethodText,
                                      key
                                    )}
                                  </MenuItem>
                                ))}
                              </Select>
                            </FormControl>
                          </Grid>
                        </>
                      )}
                      <Grid item xs={12} md={6} xl={3}>
                        <FormControl fullWidth>
                          <InputLabel>Componentes</InputLabel>
                          <Select
                            label="Componentes"
                            value={system.biogasCompoundsSideA}
                            name="biogasCompoundsSideA"
                            onChange={(e: any) => handleChange(e)}
                          >
                            {Object.keys(DiagramCompoundUnitType).map((key) => (
                              <MenuItem key={key} value={key}>
                                {getValueByKey(DiagramCompoundUnitText, key)}
                              </MenuItem>
                            ))}
                          </Select>
                        </FormControl>
                      </Grid>
                    </Grid>
                  </Grid>
                )}
                {system.plantOperation === PlantOperationType.SideB && (
                  <Grid item xs={12} md={12} xl={12}>
                    <Grid container spacing={2}>
                      {system.measurementMethodSideB ===
                        DiagramBiogasMeasurementMethodType.Pressure && (
                        <>
                          <Grid item xs={12} md={6} xl={3}>
                            <FormControl fullWidth>
                              <InputLabel>Biogás</InputLabel>
                              <Select
                                label="Biogás"
                                value={system.biogasVisualizationSideB}
                                name="biogasVisualizationSideB"
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
                                value={system.biogasVisualizationUnitsSideB}
                                name="biogasVisualizationUnitsSideB"
                                onChange={(e: any) => handleChange(e)}
                              >
                                {Object.keys(DiagramBiogasUnitType).map(
                                  (key) => (
                                    <MenuItem key={key} value={key}>
                                      {getValueByKey(
                                        DiagramBiogasUnitText,
                                        key
                                      )}
                                    </MenuItem>
                                  )
                                )}
                              </Select>
                            </FormControl>
                          </Grid>
                          <Grid item xs={12} md={6} xl={3}>
                            <FormControl fullWidth>
                              <InputLabel>Energía</InputLabel>
                              <Select
                                label="Energía"
                                value={system.measurementMethodSideB}
                                name="measurementMethodSideB"
                                onChange={(e: any) => handleChange(e)}
                              >
                                {Object.keys(
                                  DiagramBiogasMeasurementMethodType
                                ).map((key) => (
                                  <MenuItem key={key} value={key}>
                                    {getValueByKey(
                                      DiagramBiogasMeasurementMethodText,
                                      key
                                    )}
                                  </MenuItem>
                                ))}
                              </Select>
                            </FormControl>
                          </Grid>
                        </>
                      )}
                      <Grid item xs={12} md={6} xl={3}>
                        <FormControl fullWidth>
                          <InputLabel>Componentes</InputLabel>
                          <Select
                            label="Componentes"
                            value={system.biogasCompoundsSideB}
                            name="biogasCompoundsSideB"
                            onChange={(e: any) => handleChange(e)}
                          >
                            {Object.keys(DiagramCompoundUnitType).map((key) => (
                              <MenuItem key={key} value={key}>
                                {getValueByKey(DiagramCompoundUnitText, key)}
                              </MenuItem>
                            ))}
                          </Select>
                        </FormControl>
                      </Grid>
                    </Grid>
                  </Grid>
                )}
                <Grid item xs={12} md={12} xl={12}>
                  <BiochemicalMethanePotentialDiagram
                    bmp={system}
                    data={data}
                    isPlaying={isPlaying}
                  ></BiochemicalMethanePotentialDiagram>
                </Grid>
              </Grid>
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
                variables={BMP_VARIABLES}
                playerControl={playerControl}
                isPlaying={isPlaying}
                timeMultiplierAdditionalCondition={system.steps.value !== 1}
              ></TimeGraphs>
            </Grid>
          </>
        )}
      </Grid>
    </>
  );
};

export default BiochemicalMethanePotential;
