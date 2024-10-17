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
import CalculateIcon from '@mui/icons-material/Calculate';
import { useCallback, useEffect, useState } from 'react';
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
  SinkLoadModeType,
} from '../../types/models/turbine';
import TimeGraphs from '../../components/models/common/TimeGraphs';
import PlayerControls from '../../components/UI/PlayerControls';
import { setFormState } from '../../utils/setFormState';
import { useControlPlayer } from '../../hooks/useControlPlayer';
import CustomNumberField from '../../components/UI/CustomNumberField';
import Battery from '../../components/models/Battery';
import CustomToggle from '../../components/UI/CustomToggle';

import singleDiagramLight from '../../assets/singleDiagram/singleDiagramTurbineLight.png';
import singleDiagramDark from '../../assets/singleDiagram/singleDiagramTurbineDark.png';
import turbineIllustration from '../../assets/illustrations/turbine.png';
import TurbineDiagram from '../../components/models/diagram/TurbineDiagram';
import ErrorDialog from '../../components/UI/ErrorDialog';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import FileUploadIcon from '@mui/icons-material/FileUpload';
import saveAs from 'file-saver';
import { StepUnitText, StepUnitType } from '../../types/common';
import { getValueByKey } from '../../utils/getValueByKey';
import ToggleArrayCustomNumberField from '../../components/UI/ToggleArrayCustomNumberField';
import { useAppSelector } from '../../redux/reduxHooks';
import { ThemeType } from '../../types/theme';
import {
  CellChange,
  Column,
  DefaultCellTypes,
  ReactGrid,
  Row,
} from '@silevis/reactgrid';
import { setTurbineTable } from '../../utils/models/setTurbine';
import Config from '../../config/config';

const Turbine = () => {
  const userTheme = useAppSelector((state) => state.theme.value);

  const [system, setSystem] = useState<TurbineParameters>({ ...TURBINE });
  const [isImageExpanded, setIsImageExpanded] = useState(true);
  const [isSingleDiagramExpanded, setIsSingleDiagramExpanded] = useState(true);
  const [isParametersExpanded, setIsParametersExpanded] = useState(true);
  const [isOpen, setIsOpen] = useState(false);

  const [data, charts, isPlaying, error, onPlay, onPause, onStop, setError] =
    useControlPlayer<TurbineParameters, TurbineOutput>('turbine', system);

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

      if (system.inputPressure.arrayEnabled)
        arr.push({
          rowId: '0',
          cells: [
            { type: 'header', text: 'Presión [mH₂O]', nonEditable: true },
            ...system.inputPressureArray.map((v) => {
              const col: DefaultCellTypes = {
                type: 'number',
                value: v,
              };
              return col;
            }),
          ],
        });

      if (system.inputFlow.arrayEnabled)
        arr.push({
          rowId: '1',
          cells: [
            { type: 'header', text: 'Flujo [L / s]', nonEditable: true },
            ...system.inputFlowArray.map((v) => {
              const col: DefaultCellTypes = {
                type: 'number',
                value: v,
              };
              return col;
            }),
          ],
        });

      if (system.inputActivePower.arrayEnabled)
        arr.push({
          rowId: '2',
          cells: [
            { type: 'header', text: 'Potencia [W]', nonEditable: true },
            ...system.inputActivePowerArray.map((v) => {
              const col: DefaultCellTypes = {
                type: 'number',
                value: v,
              };
              return col;
            }),
          ],
        });

      if (system.inputPowerFactor.arrayEnabled)
        arr.push({
          rowId: '3',
          cells: [
            { type: 'header', text: 'Factor de potencia', nonEditable: true },
            ...system.inputPowerFactorArray.map((v) => {
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
    system.inputActivePower.arrayEnabled,
    system.inputActivePowerArray,
    system.inputFlow.arrayEnabled,
    system.inputFlowArray,
    system.inputPowerFactor.arrayEnabled,
    system.inputPowerFactorArray,
    system.inputPressure.arrayEnabled,
    system.inputPressureArray,
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
    setSystem(setTurbineTable(e, system));
  };

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
        simulatedChargeCycleInitialSOC: data.chargeCycleInitialSOC,
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
        const jsonData: TurbineParameters = JSON.parse(
          e.target.result
        ) as TurbineParameters;
        if ('turbineType' in jsonData) {
          setSystem(jsonData);
        } else {
          setError('El archivo no corresponde a un gemelo digital de turbinas');
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
                src={turbineIllustration}
                alt="turbineIllustration"
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
                        variable={system.controller.chargingMinimumVoltage}
                        name="controller.chargingMinimumVoltage"
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
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={system.inverterMinimumVoltage}
                        name="inverterMinimumVoltage"
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
          <Button
            target="_blank"
            href={Config.getInstance().params.powerSpoutUrl}
            variant="contained"
            color="info"
            startIcon={<CalculateIcon />}
            sx={{ margin: '5px' }}
          >
            Calculadora PowerSpout
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
                  <h3>Parámetros turbina</h3>
                </Grid>
                <Grid item xs={12} md={12} xl={12}>
                  <ToggleArrayCustomNumberField
                    variable={system.inputPressure}
                    name="inputPressure"
                    handleChange={handleChange}
                    disabled={system.inputOfflineOperation}
                    variableName="Presión"
                    arrayDisabled={!system.inputOfflineOperation}
                    steps={system.steps.value}
                  ></ToggleArrayCustomNumberField>
                </Grid>
                <Grid item xs={12} md={12} xl={12}>
                  <ToggleArrayCustomNumberField
                    variable={system.inputFlow}
                    name="inputFlow"
                    handleChange={handleChange}
                    disabled={system.inputOfflineOperation}
                    variableName="Flujo"
                    arrayDisabled={!system.inputOfflineOperation}
                    steps={system.steps.value}
                  ></ToggleArrayCustomNumberField>
                </Grid>
                {system.turbineType === TurbineType.Turgo && (
                  <>
                    <Grid item xs={12} md={12} xl={12}>
                      <h3>Parámetros carga CC</h3>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12} alignContent={'center'}>
                      <CustomToggle
                        name="inputDirectCurrentPower"
                        value={system.inputDirectCurrentPower}
                        handleChange={handleChange}
                        trueString="Conectado: 3.6 W"
                        falseString="Desconectado: 0.0 W"
                      ></CustomToggle>
                    </Grid>
                  </>
                )}
                <Grid item xs={12} md={12} xl={12}>
                  <h3>Parámetros carga CA</h3>
                </Grid>
                <Grid item xs={12} md={12} xl={12}>
                  <ToggleArrayCustomNumberField
                    variable={system.inputActivePower}
                    name="inputActivePower"
                    handleChange={handleChange}
                    disabled={system.inputOfflineOperation}
                    variableName="Potencia activa"
                    arrayDisabled={!system.inputOfflineOperation}
                    steps={system.steps.value}
                  ></ToggleArrayCustomNumberField>
                </Grid>
                <Grid item xs={12} md={12} xl={12}>
                  <ToggleArrayCustomNumberField
                    variable={system.inputPowerFactor}
                    name="inputPowerFactor"
                    handleChange={handleChange}
                    disabled={system.inputOfflineOperation}
                    variableName="Factor de potencia"
                    arrayDisabled={!system.inputOfflineOperation}
                    steps={system.steps.value}
                  ></ToggleArrayCustomNumberField>
                </Grid>
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
                <Grid item xs={12} md={12} xl={12}>
                  <h3>Conexión carga disipadora</h3>
                </Grid>
                <Grid item xs={12} md={12} xl={7}>
                  <FormControl fullWidth>
                    <InputLabel id="sink-load-mode-type">
                      Modo carga disipadora
                    </InputLabel>
                    <Select
                      labelId="sink-load-mode-type"
                      label="Modo carga disipadora"
                      value={system.sinkLoadMode}
                      name="sinkLoadMode"
                      onChange={(e: any) => handleChange(e)}
                    >
                      {Object.keys(SinkLoadModeType).map((key) => (
                        <MenuItem key={key} value={key}>
                          {key}
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                </Grid>
              </Grid>
            </Grid>
            <Grid item xs={12} md={9.5} xl={9.5}>
              <Grid container spacing={2}>
                <Grid item xs={12} md={12} xl={12}>
                  {playerControl}
                </Grid>
                <Grid item xs={12} md={12} xl={12}>
                  <TurbineDiagram
                    turbine={system}
                    data={data}
                    isPlaying={isPlaying}
                  ></TurbineDiagram>
                </Grid>
                {(system.inputPressure.arrayEnabled ||
                  system.inputFlow.arrayEnabled ||
                  system.inputActivePower.arrayEnabled ||
                  system.inputPowerFactor.arrayEnabled) &&
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
                variables={
                  system.turbineType === TurbineType.Pelton
                    ? PELTON_TURBINE_DIAGRAM_VARIABLES
                    : TURGO_TURBINE_DIAGRAM_VARIABLES
                }
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

export default Turbine;
