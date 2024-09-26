import React, { useCallback, useEffect, useState } from 'react';
import { useAppSelector } from '../../redux/reduxHooks';
import {
  ElectronicLoadModeText,
  ElectronicLoadModeType,
  HYDROGEN_CELL,
  HYDROGEN_CELL_DIAGRAM_VARIABLES,
  HydrogenCellOutput,
  HydrogencellParameters,
  LightsModeText,
  LightsModeType,
} from '../../types/models/hydrogenCell';
import { useControlPlayer } from '../../hooks/useControlPlayer';
import {
  Column,
  Row,
  DefaultCellTypes,
  CellChange,
  ReactGrid,
} from '@silevis/reactgrid';
import { setHydrogenCellTable } from '../../utils/models/setHydrogenCell';
import saveAs from 'file-saver';
import PlayerControls from '../../components/UI/PlayerControls';
import hydrogenCellIllustration from '../../assets/illustrations/hydrogen.png';
import singleDiagramLight from '../../assets/singleDiagram/singleDiagramHydrogenLight.png';
import singleDiagramDark from '../../assets/singleDiagram/singleDiagramHydrogenDark.png';
import { setFormState } from '../../utils/setFormState';
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
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import FileUploadIcon from '@mui/icons-material/FileUpload';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { ThemeType } from '../../types/theme';
import CustomNumberField from '../../components/UI/CustomNumberField';
import { StepUnitType, StepUnitText } from '../../types/common';
import { getValueByKey } from '../../utils/getValueByKey';
import CustomStringField from '../../components/UI/CustomStringField';
import CustomToggle from '../../components/UI/CustomToggle';
import ToggleArrayCustomNumberField from '../../components/UI/ToggleArrayCustomNumberField';
import HydrogenCellDiagram from '../../components/models/diagram/HydrogenCellDiagram';
import TimeGraphs from '../../components/models/common/TimeGraphs';

type Props = {};

const HydrogenCell = (props: Props) => {
  const userTheme = useAppSelector((state) => state.theme.value);

  const [system, setSystem] = useState<HydrogencellParameters>({
    ...HYDROGEN_CELL,
  });
  const [isImageExpanded, setIsImageExpanded] = useState(true);
  const [isSingleDiagramExpanded, setIsSingleDiagramExpanded] = useState(true);
  const [isParametersExpanded, setIsParametersExpanded] = useState(true);
  const [isOpen, setIsOpen] = useState(false);

  const [data, charts, isPlaying, error, onPlay, onPause, onStop, setError] =
    useControlPlayer<HydrogencellParameters, HydrogenCellOutput>(
      'hydrogenCell',
      system
    );

  const getColumns = useCallback((): Column[] => {
    if (system.steps.value > 1) {
      let arr: Column[] = [
        { columnId: `variables`, width: 250 },
        ...Array(system.steps.value)
          .fill(0)
          .map((_, i) => ({
            columnId: `${i}`,
            width: 100,
          })),
      ];
      return arr;
    }
    return [];
  }, [system.steps.value]);

  const getRows = useCallback((): Row[] => {
    if (system.steps.value > 1) {
      let arr: Row[] = [];
      arr.push({
        rowId: 'header',
        cells: [
          { type: 'header', text: '', nonEditable: true },
          ...Array(system.steps.value)
            .fill(0)
            .map((_, i) => {
              const col: DefaultCellTypes = {
                type: 'header',
                text: `P ${i + 1}`,
                nonEditable: true,
              };
              return col;
            }),
        ],
      });

      if (system.inputHydrogenFlow.arrayEnabled)
        arr.push({
          rowId: '0',
          cells: [
            { type: 'header', text: 'Flujo [L/min]', nonEditable: true },
            ...system.inputHydrogenFlowArray.map((v) => {
              const col: DefaultCellTypes = {
                type: 'number',
                value: v,
              };
              return col;
            }),
          ],
        });

      if (system.inputHydrogenPressure.arrayEnabled)
        arr.push({
          rowId: '1',
          cells: [
            { type: 'header', text: 'Presión [psi]', nonEditable: true },
            ...system.inputHydrogenPressureArray.map((v) => {
              const col: DefaultCellTypes = {
                type: 'number',
                value: v,
              };
              return col;
            }),
          ],
        });

      if (system.inputCellTemperature.arrayEnabled)
        arr.push({
          rowId: '2',
          cells: [
            { type: 'header', text: 'Temperatura [°C]', nonEditable: true },
            ...system.inputCellTemperatureArray.map((v) => {
              const col: DefaultCellTypes = {
                type: 'number',
                value: v,
              };
              return col;
            }),
          ],
        });

      if (
        system.inputElectronicLoadCurrent.arrayEnabled &&
        system.electronicLoadMode === ElectronicLoadModeType.Current
      )
        arr.push({
          rowId: '3',
          cells: [
            { type: 'header', text: 'Corriente [A]', nonEditable: true },
            ...system.inputElectronicLoadCurrentArray.map((v) => {
              const col: DefaultCellTypes = {
                type: 'number',
                value: v,
              };
              return col;
            }),
          ],
        });

      if (
        system.inputElectronicLoadPower.arrayEnabled &&
        system.electronicLoadMode === ElectronicLoadModeType.Power
      )
        arr.push({
          rowId: '4',
          cells: [
            { type: 'header', text: 'Potencia [W]', nonEditable: true },
            ...system.inputElectronicLoadPowerArray.map((v) => {
              const col: DefaultCellTypes = {
                type: 'number',
                value: v,
              };
              return col;
            }),
          ],
        });

      if (
        system.inputElectronicLoadResistance.arrayEnabled &&
        system.electronicLoadMode === ElectronicLoadModeType.Resistance
      )
        arr.push({
          rowId: '5',
          cells: [
            { type: 'header', text: 'Resistencia [Ω]', nonEditable: true },
            ...system.inputElectronicLoadResistanceArray.map((v) => {
              const col: DefaultCellTypes = {
                type: 'number',
                value: v,
              };
              return col;
            }),
          ],
        });
      return arr;
    }
    return [];
  }, [
    system.electronicLoadMode,
    system.inputCellTemperature.arrayEnabled,
    system.inputCellTemperatureArray,
    system.inputElectronicLoadCurrent.arrayEnabled,
    system.inputElectronicLoadCurrentArray,
    system.inputElectronicLoadPower.arrayEnabled,
    system.inputElectronicLoadPowerArray,
    system.inputElectronicLoadResistance.arrayEnabled,
    system.inputElectronicLoadResistanceArray,
    system.inputHydrogenFlow.arrayEnabled,
    system.inputHydrogenFlowArray,
    system.inputHydrogenPressure.arrayEnabled,
    system.inputHydrogenPressureArray,
    system.steps.value,
  ]);

  const [rows, setRows] = useState<Row[]>(getRows());

  const [columns, setColumns] = useState<Column[]>(getColumns());

  useEffect(() => {
    if (system.steps.value > 1) {
      setRows(getRows());
      setColumns(getColumns());
    }
  }, [getColumns, getRows, system]);

  const handleCellsChange = (e: CellChange[]) => {
    setSystem(setHydrogenCellTable(e, system));
  };

  useEffect(() => {
    if (data !== undefined) {
      setSystem((o) => ({
        ...o,
        inputHydrogenFlow: {
          ...o.inputHydrogenFlow,
          value: data.hydrogenFlow
            ? data.hydrogenFlow
            : o.inputHydrogenFlow.value,
        },
        inputHydrogenPressure: {
          ...o.inputHydrogenPressure,
          value: data.hydrogenPressure
            ? data.hydrogenPressure
            : o.inputHydrogenPressure.value,
        },
        inputCellTemperature: {
          ...o.inputCellTemperature,
          value: data.cellTemperature
            ? data.cellTemperature
            : o.inputCellTemperature.value,
        },
        inputElectronicLoadCurrent: {
          ...o.inputElectronicLoadCurrent,
          value: data.inputElectronicLoadCurrent
            ? data.inputElectronicLoadCurrent
            : o.inputElectronicLoadCurrent.value,
        },
        inputElectronicLoadPower: {
          ...o.inputElectronicLoadPower,
          value: data.inputElectronicLoadPower
            ? data.inputElectronicLoadPower
            : o.inputElectronicLoadPower.value,
        },
        inputElectronicLoadResistance: {
          ...o.inputElectronicLoadResistance,
          value: data.inputElectronicLoadResistance
            ? data.inputElectronicLoadResistance
            : o.inputElectronicLoadResistance.value,
        },
        simulatedCellVoltage: data.cellVoltage,
        simulatedGeneratedEnergy: data.cellGeneratedEnergy,
      }));
    } else {
      setSystem((o) => ({
        ...o,
        simulatedCellVoltage: undefined,
        simulatedGeneratedEnergy: undefined,
      }));
    }
  }, [data]);

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

  const handleChange = (e: any, variableName?: string) => {
    const newState = setFormState<HydrogencellParameters>(
      e,
      system,
      variableName
    );
    if (newState) {
      setSystem(newState as HydrogencellParameters);
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
        const jsonData: HydrogencellParameters = JSON.parse(
          e.target.result
        ) as HydrogencellParameters;
        if ('electronicLoadMode' in jsonData) {
          setSystem(jsonData);
        } else {
          setError(
            'El archivo no corresponde a un gemelo digital de celdas de hidrógeno'
          );
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
                src={hydrogenCellIllustration}
                alt="hydrogenCellIllustration"
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
              <img
                style={{
                  height: '500px',
                  display: 'block',
                  marginLeft: 'auto',
                  marginRight: 'auto',
                }}
                src={
                  userTheme === ThemeType.Light
                    ? singleDiagramLight
                    : singleDiagramDark
                }
                alt="singleDiagram"
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
                <Grid item xs={12} md={12} xl={3}>
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
                <Grid item xs={12} md={12} xl={4.5}>
                  <h3>Celda de hidrógeno</h3>
                  <Grid container spacing={2}>
                    <Grid item xs={12} md={6} xl={6}>
                      <CustomNumberField
                        variable={system.cellMaximumPower}
                        name="cellMaximumPower"
                        handleChange={handleChange}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={6} xl={6}>
                      <CustomNumberField
                        variable={system.cellMaximumCurrent}
                        name="cellMaximumCurrent"
                        handleChange={handleChange}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={6} xl={6}>
                      <CustomStringField
                        variable={system.cellRatedVoltage}
                        name="cellRatedVoltage"
                        handleChange={handleChange}
                      ></CustomStringField>
                    </Grid>
                    <Grid item xs={12} md={6} xl={6}>
                      <CustomNumberField
                        variable={system.cellRatedEfficiency}
                        name="cellRatedEfficiency"
                        handleChange={handleChange}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={6} xl={6}>
                      <CustomStringField
                        variable={system.cellRatedHydrogenPressure}
                        name="cellRatedHydrogenPressure"
                        handleChange={handleChange}
                      ></CustomStringField>
                    </Grid>
                    <Grid item xs={12} md={6} xl={6}>
                      <CustomNumberField
                        variable={system.cellRatedHydrogenFlow}
                        name="cellRatedHydrogenFlow"
                        handleChange={handleChange}
                      ></CustomNumberField>
                    </Grid>
                  </Grid>
                </Grid>
                <Grid item xs={12} md={12} xl={2.5}>
                  <h3>Convertidor DC/DC</h3>
                  <Grid container spacing={2}>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={system.converterMinimumVoltage}
                        name="converterMinimumVoltage"
                        handleChange={handleChange}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={system.converterRatedPower}
                        name="converterRatedPower"
                        handleChange={handleChange}
                      ></CustomNumberField>
                    </Grid>
                  </Grid>
                </Grid>
                <Grid item xs={12} md={12} xl={2.5}>
                  <h3>Carga electrónica</h3>
                  <Grid container spacing={2}>
                    <Grid item xs={12} md={12} xl={12}>
                      <FormControl fullWidth>
                        <InputLabel id="load-mode-type">
                          Modo de operación
                        </InputLabel>
                        <Select
                          labelId="load-mode-type"
                          label="Modo de operación"
                          value={system.electronicLoadMode}
                          name="electronicLoadMode"
                          onChange={(e: any) => handleChange(e)}
                          disabled={isPlaying}
                        >
                          {Object.keys(ElectronicLoadModeType).map((key) => (
                            <MenuItem key={key} value={key}>
                              {getValueByKey(ElectronicLoadModeText, key)}
                            </MenuItem>
                          ))}
                        </Select>
                      </FormControl>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={system.electronicLoadMaximumCurent}
                        name="electronicLoadMaximumCurent"
                        handleChange={handleChange}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={system.electronicLoadMaximumPower}
                        name="electronicLoadMaximumPower"
                        handleChange={handleChange}
                      ></CustomNumberField>
                    </Grid>
                  </Grid>
                </Grid>
                <Grid item xs={12} md={12} xl={2.5}>
                  <h3>Semáforo</h3>
                  <Grid container spacing={2}>
                    <Grid item xs={12} md={12} xl={12}>
                      <FormControl fullWidth>
                        <InputLabel id="lights-type">
                          Modo de operación
                        </InputLabel>
                        <Select
                          labelId="lights-type"
                          label="Modo de operación"
                          value={system.lightsMode}
                          name="lightsMode"
                          onChange={(e: any) => handleChange(e)}
                          disabled={isPlaying}
                        >
                          {Object.keys(LightsModeType).map((key) => (
                            <MenuItem key={key} value={key}>
                              {getValueByKey(LightsModeText, key)}
                            </MenuItem>
                          ))}
                        </Select>
                      </FormControl>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={system.lightsIndividualPower}
                        name="lightsIndividualPower"
                        handleChange={handleChange}
                      ></CustomNumberField>
                    </Grid>
                  </Grid>
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
                  <h2>Parámetros celda hidrógeno</h2>
                </Grid>
                {/* <Grid item xs={12} md={12} xl={12}>
                  <ToggleArrayCustomNumberField
                    variable={system.inputHydrogenFlow}
                    name="inputHydrogenFlow"
                    handleChange={handleChange}
                    disabled={system.inputOfflineOperation}
                    variableName="Flujo"
                    arrayDisabled={!system.inputOfflineOperation}
                    steps={system.steps.value}
                  ></ToggleArrayCustomNumberField>
                </Grid>
                <Grid item xs={12} md={12} xl={12}>
                  <ToggleArrayCustomNumberField
                    variable={system.inputHydrogenPressure}
                    name="inputHydrogenPressure"
                    handleChange={handleChange}
                    disabled={system.inputOfflineOperation}
                    variableName="Presión"
                    arrayDisabled={!system.inputOfflineOperation}
                    steps={system.steps.value}
                  ></ToggleArrayCustomNumberField>
                </Grid> */}
                <Grid item xs={12} md={12} xl={12}>
                  <ToggleArrayCustomNumberField
                    variable={system.inputCellTemperature}
                    name="inputCellTemperature"
                    handleChange={handleChange}
                    disabled={system.inputOfflineOperation}
                    variableName="Temperatura"
                    arrayDisabled={!system.inputOfflineOperation}
                    steps={system.steps.value}
                  ></ToggleArrayCustomNumberField>
                </Grid>
                <Grid item xs={12} md={12} xl={7}>
                  <h4>Autoalimentación eléctrica</h4>
                </Grid>
                <Grid item xs={12} md={12} xl={5} alignContent={'center'}>
                  <CustomToggle
                    value={system.cellSelfFeeding}
                    name="cellSelfFeeding"
                    handleChange={handleChange}
                    trueString="On"
                    falseString="Off"
                  ></CustomToggle>
                </Grid>
                <Grid item xs={12} md={12} xl={12}>
                  <h2>Parámetros carga electrónica</h2>
                </Grid>
                {system.electronicLoadMode ===
                  ElectronicLoadModeType.Current && (
                  <Grid item xs={12} md={12} xl={12}>
                    <ToggleArrayCustomNumberField
                      variable={system.inputElectronicLoadCurrent}
                      name="inputElectronicLoadCurrent"
                      handleChange={handleChange}
                      disabled={system.inputOfflineOperation}
                      variableName="Corriente"
                      arrayDisabled={!system.inputOfflineOperation}
                      steps={system.steps.value}
                    ></ToggleArrayCustomNumberField>
                  </Grid>
                )}
                {system.electronicLoadMode === ElectronicLoadModeType.Power && (
                  <Grid item xs={12} md={12} xl={12}>
                    <ToggleArrayCustomNumberField
                      variable={system.inputElectronicLoadPower}
                      name="inputElectronicLoadPower"
                      handleChange={handleChange}
                      disabled={system.inputOfflineOperation}
                      variableName="Potencia"
                      arrayDisabled={!system.inputOfflineOperation}
                      steps={system.steps.value}
                    ></ToggleArrayCustomNumberField>
                  </Grid>
                )}
                {system.electronicLoadMode ===
                  ElectronicLoadModeType.Resistance && (
                  <Grid item xs={12} md={12} xl={12}>
                    <ToggleArrayCustomNumberField
                      variable={system.inputElectronicLoadResistance}
                      name="inputElectronicLoadResistance"
                      handleChange={handleChange}
                      disabled={system.inputOfflineOperation}
                      variableName="Resistencia"
                      arrayDisabled={!system.inputOfflineOperation}
                      steps={system.steps.value}
                    ></ToggleArrayCustomNumberField>
                  </Grid>
                )}
                <Grid item xs={12} md={12} xl={12}>
                  <h2>Parámetros semáforo</h2>
                </Grid>
                <Grid item xs={12} md={12} xl={12} alignContent={'center'}>
                  <CustomToggle
                    value={system.lightsConnected}
                    name="lightsConnected"
                    handleChange={handleChange}
                    trueString="Conectado"
                    falseString="Desconectado"
                  ></CustomToggle>
                </Grid>
              </Grid>
            </Grid>
            <Grid item xs={12} md={9.5} xl={9.5}>
              <Grid container spacing={2}>
                <Grid item xs={12} md={12} xl={12}>
                  {playerControl}
                </Grid>
                <Grid item xs={12} md={12} xl={12}>
                  <HydrogenCellDiagram
                    hydrogenCell={system}
                    data={data}
                    isPlaying={isPlaying}
                  ></HydrogenCellDiagram>
                </Grid>
                {(system.inputHydrogenFlow.arrayEnabled ||
                  system.inputHydrogenPressure.arrayEnabled ||
                  system.inputCellTemperature.arrayEnabled ||
                  (system.inputElectronicLoadCurrent.arrayEnabled &&
                    system.electronicLoadMode ===
                      ElectronicLoadModeType.Current) ||
                  (system.inputElectronicLoadPower.arrayEnabled &&
                    system.electronicLoadMode ===
                      ElectronicLoadModeType.Power) ||
                  (system.inputElectronicLoadResistance.arrayEnabled &&
                    system.electronicLoadMode ===
                      ElectronicLoadModeType.Resistance)) &&
                  system.steps.value > 1 && (
                    <Grid item xs={12} md={12} xl={12}>
                      <div
                        id={
                          userTheme === ThemeType.Dark
                            ? 'reactgrid-dark-mode'
                            : 'reactgrid-light-mode'
                        }
                        style={{
                          maxWidth: '100%',
                          overflow: 'auto',
                        }}
                      >
                        <ReactGrid
                          rows={rows}
                          columns={columns}
                          onCellsChanged={(e: CellChange[]) => {
                            handleCellsChange(e);
                          }}
                        />
                      </div>
                    </Grid>
                  )}
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
                variables={HYDROGEN_CELL_DIAGRAM_VARIABLES}
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

export default HydrogenCell;
