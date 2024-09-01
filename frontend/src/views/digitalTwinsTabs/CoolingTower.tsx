import { useCallback, useEffect, useState } from 'react';
import ErrorDialog from '../../components/UI/ErrorDialog';
import { useControlPlayer } from '../../hooks/useControlPlayer';
import {
  COOLING_TOWER,
  COOLING_TOWER_DIAGRAM_VARIABLES,
  CoolingTowerOutput,
  CoolingTowerParameters,
  FillType,
  FillTypeText,
} from '../../types/models/coolingTower';
import {
  Grid,
  Accordion,
  AccordionSummary,
  Typography,
  AccordionDetails,
  FormControl,
  TextField,
  InputLabel,
  MenuItem,
  Select,
  Button,
} from '@mui/material';

import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import FileUploadIcon from '@mui/icons-material/FileUpload';
import saveAs from 'file-saver';
import PlayerControls from '../../components/UI/PlayerControls';
import { setFormState } from '../../utils/setFormState';
import CustomNumberField from '../../components/UI/CustomNumberField';
import { getValueByKey } from '../../utils/getValueByKey';
import CustomToggle from '../../components/UI/CustomToggle';
import CoolingTowerDiagram from '../../components/models/diagram/CoolingTowerDiagram';
import TimeGraphs from '../../components/models/common/TimeGraphs';
import coolingTower from '../../assets/illustrations/tower.png';
import { StepUnitType, StepUnitText } from '../../types/common';
import ToggleArrayCustomNumberField from '../../components/UI/ToggleArrayCustomNumberField';
import {
  CellChange,
  Column,
  DefaultCellTypes,
  ReactGrid,
  Row,
} from '@silevis/reactgrid';
import { useAppSelector } from '../../redux/reduxHooks';
import { ThemeType } from '../../types/theme';
import { setCoolingTowerTable } from '../../utils/models/setCoolingTower';

const CoolingTower = () => {
  const userTheme = useAppSelector((state) => state.theme.value);

  const [system, setSystem] = useState<CoolingTowerParameters>({
    ...COOLING_TOWER,
  });
  const [isImageExpanded, setIsImageExpanded] = useState(true);
  const [isParametersExpanded, setIsParametersExpanded] = useState(true);
  const [isOpen, setIsOpen] = useState(false);

  const [data, charts, isPlaying, error, onPlay, onPause, onStop, setError] =
    useControlPlayer<CoolingTowerParameters, CoolingTowerOutput>(
      'coolingTower',
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

      if (system.topWaterFlow.arrayEnabled)
        arr.push({
          rowId: '0',
          cells: [
            { type: 'header', text: 'Flujo agua [L / min]', nonEditable: true },
            ...system.topWaterFlowArray.map((v) => {
              const col: DefaultCellTypes = {
                type: 'number',
                value: v,
              };
              return col;
            }),
          ],
        });

      if (system.topWaterTemperature.arrayEnabled)
        arr.push({
          rowId: '1',
          cells: [
            {
              type: 'header',
              text: 'Temperatura agua [°C]',
              nonEditable: true,
            },
            ...system.topWaterTemperatureArray.map((v) => {
              const col: DefaultCellTypes = {
                type: 'number',
                value: v,
              };
              return col;
            }),
          ],
        });

      if (system.bottomAirFlow.arrayEnabled)
        arr.push({
          rowId: '2',
          cells: [
            {
              type: 'header',
              text: 'Flujo aire [m³ / min]',
              nonEditable: true,
            },
            ...system.bottomAirFlowArray.map((v) => {
              const col: DefaultCellTypes = {
                type: 'number',
                value: v,
              };
              return col;
            }),
          ],
        });

      if (system.bottomAirTemperature.arrayEnabled)
        arr.push({
          rowId: '3',
          cells: [
            {
              type: 'header',
              text: 'Temperatura aire [°C]',
              nonEditable: true,
            },
            ...system.bottomAirTemperatureArray.map((v) => {
              const col: DefaultCellTypes = {
                type: 'number',
                value: v,
              };
              return col;
            }),
          ],
        });

      if (system.bottomAirHumidity.arrayEnabled)
        arr.push({
          rowId: '4',
          cells: [
            { type: 'header', text: 'Humedad [%]', nonEditable: true },
            ...system.bottomAirHumidityArray.map((v) => {
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
    system.bottomAirFlow.arrayEnabled,
    system.bottomAirFlowArray,
    system.bottomAirHumidity.arrayEnabled,
    system.bottomAirHumidityArray,
    system.bottomAirTemperature.arrayEnabled,
    system.bottomAirTemperatureArray,
    system.steps.value,
    system.topWaterFlow.arrayEnabled,
    system.topWaterFlowArray,
    system.topWaterTemperature.arrayEnabled,
    system.topWaterTemperatureArray,
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
    setSystem(setCoolingTowerTable(e, system));
  };

  useEffect(() => {
    if (data !== undefined) {
      setSystem((o) => ({
        ...o,
        topWaterFlow: {
          ...o.topWaterFlow,
          value: data.topWaterFlow ? data.topWaterFlow : o.topWaterFlow.value,
        },
        topWaterTemperature: {
          ...o.topWaterTemperature,
          value: data.topWaterTemperature
            ? data.topWaterTemperature
            : o.topWaterTemperature.value,
        },
        bottomAirFlow: {
          ...o.bottomAirFlow,
          value: data.bottomAirFlow
            ? data.bottomAirFlow
            : o.bottomAirFlow.value,
        },
        bottomAirTemperature: {
          ...o.bottomAirTemperature,
          value: data.bottomAirTemperature
            ? data.bottomAirTemperature
            : o.bottomAirTemperature.value,
        },
        bottomAirHumidity: {
          ...o.bottomAirHumidity,
          value: data.bottomAirHumidity
            ? data.bottomAirHumidity
            : o.bottomAirHumidity.value,
        },
        atmosphericPressure: {
          ...o.atmosphericPressure,
          value: data.atmosphericPressure
            ? data.atmosphericPressure
            : o.atmosphericPressure.value,
        },
        simulatedBottomWaterTemperature: data.bottomAirTemperature,
        simulatedTopAirTemperature: data.topAirTemperature,
        simulatedEnergyAppliedToWater: data.energyAppliedToWater,
      }));
    } else {
      setSystem((o) => ({
        ...o,
        simulatedBottomWaterTemperature: undefined,
        simulatedTopAirTemperature: undefined,
        simulatedEnergyAppliedToWater: undefined,
      }));
    }
  }, [data]);

  const handleChange = (e: any, variableName?: string) => {
    const newState = setFormState<CoolingTowerParameters>(
      e,
      system,
      variableName
    );
    if (newState) {
      setSystem(newState as CoolingTowerParameters);
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
        const jsonData: CoolingTowerParameters = JSON.parse(
          e.target.result
        ) as CoolingTowerParameters;
        if ('topWaterFlow' in jsonData) {
          setSystem(jsonData);
        } else {
          setError(
            'El archivo no corresponde a un gemelo digital de torre de enfriamiento'
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
                  height: '600px',
                  display: 'block',
                  marginLeft: 'auto',
                  marginRight: 'auto',
                }}
                src={coolingTower}
                alt="coolingTowerllustration"
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
                <Grid item xs={12} md={12} xl={4}>
                  <h3>Torre</h3>
                  <Grid container spacing={2}>
                    <Grid item xs={12} md={12} xl={12}>
                      <FormControl fullWidth>
                        <InputLabel id="step-fill-type">
                          Tipo de empaque
                        </InputLabel>
                        <Select
                          labelId="step-fill-type"
                          label="Tipo de empaque"
                          value={system.fillType}
                          name="fillType"
                          onChange={(e: any) => handleChange(e)}
                        >
                          {Object.keys(FillType).map((key) => (
                            <MenuItem key={key} value={key}>
                              {getValueByKey(FillTypeText, key)}
                            </MenuItem>
                          ))}
                        </Select>
                      </FormControl>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={system.towerArea}
                        name="towerArea"
                        handleChange={handleChange}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={system.towerHeight}
                        name="towerHeight"
                        handleChange={handleChange}
                      ></CustomNumberField>
                    </Grid>
                  </Grid>
                </Grid>
                <Grid item xs={12} md={12} xl={4}>
                  <h3>Soplador de aire</h3>
                  <Grid container spacing={2}>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={system.nominalAirFlow}
                        name="nominalAirFlow"
                        handleChange={handleChange}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={system.maximumAirPressure}
                        name="maximumAirPressure"
                        handleChange={handleChange}
                      ></CustomNumberField>
                    </Grid>
                  </Grid>
                </Grid>
                <Grid item xs={12} md={12} xl={4}>
                  <h3>Bomba de alimentación</h3>
                  <Grid container spacing={2}>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={system.nominalWaterFlow}
                        name="nominalWaterFlow"
                        handleChange={handleChange}
                      ></CustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <CustomNumberField
                        variable={system.maximumWaterPressure}
                        name="maximumWaterPressure"
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
                  <h3>Parámetros agua de entrada</h3>
                </Grid>
                <Grid item xs={12} md={12} xl={12}>
                  <ToggleArrayCustomNumberField
                    variable={system.topWaterFlow}
                    name="topWaterFlow"
                    handleChange={handleChange}
                    disabled={system.inputOfflineOperation}
                    variableName="Flujo"
                    arrayDisabled={!system.inputOfflineOperation}
                    steps={system.steps.value}
                  ></ToggleArrayCustomNumberField>
                </Grid>
                <Grid item xs={12} md={12} xl={12}>
                  <ToggleArrayCustomNumberField
                    variable={system.topWaterTemperature}
                    name="topWaterTemperature"
                    handleChange={handleChange}
                    disabled={system.inputOfflineOperation}
                    variableName="Temperatura"
                    arrayDisabled={!system.inputOfflineOperation}
                    steps={system.steps.value}
                  ></ToggleArrayCustomNumberField>
                </Grid>
                <Grid item xs={12} md={12} xl={12}>
                  <h3>Parámetros aire de entrada</h3>
                </Grid>
                <Grid item xs={12} md={12} xl={12}>
                  <ToggleArrayCustomNumberField
                    variable={system.bottomAirFlow}
                    name="bottomAirFlow"
                    handleChange={handleChange}
                    disabled={system.inputOfflineOperation}
                    variableName="Flujo"
                    arrayDisabled={!system.inputOfflineOperation}
                    steps={system.steps.value}
                  ></ToggleArrayCustomNumberField>
                </Grid>
                <Grid item xs={12} md={12} xl={12}>
                  <ToggleArrayCustomNumberField
                    variable={system.bottomAirTemperature}
                    name="bottomAirTemperature"
                    handleChange={handleChange}
                    disabled={system.inputOfflineOperation}
                    variableName="Temperatura"
                    arrayDisabled={!system.inputOfflineOperation}
                    steps={system.steps.value}
                  ></ToggleArrayCustomNumberField>
                </Grid>
                <Grid item xs={12} md={12} xl={12}>
                  <ToggleArrayCustomNumberField
                    variable={system.bottomAirHumidity}
                    name="bottomAirHumidity"
                    handleChange={handleChange}
                    disabled={system.inputOfflineOperation}
                    variableName="Humedad"
                    arrayDisabled={!system.inputOfflineOperation}
                    steps={system.steps.value}
                  ></ToggleArrayCustomNumberField>
                </Grid>
                <Grid item xs={12} md={12} xl={12}>
                  <h3>Parámetros ambientales</h3>
                </Grid>
                <Grid item xs={12} md={12} xl={12}>
                  <CustomNumberField
                    variable={system.atmosphericPressure}
                    name="atmosphericPressure"
                    handleChange={handleChange}
                    disabled={!system.inputOfflineOperation}
                  ></CustomNumberField>
                </Grid>
              </Grid>
            </Grid>
            <Grid item xs={12} md={9.5} xl={9.5}>
              <Grid container spacing={2}>
                <Grid item xs={12} md={12} xl={12}>
                  {playerControl}
                </Grid>
                <Grid item xs={12} md={12} xl={12}>
                  <CoolingTowerDiagram
                    coolingTower={system}
                    data={data}
                    isPlaying={isPlaying}
                  ></CoolingTowerDiagram>
                </Grid>
                {(system.topWaterFlow.arrayEnabled ||
                  system.topWaterTemperature.arrayEnabled ||
                  system.bottomAirFlow.arrayEnabled ||
                  system.bottomAirTemperature.arrayEnabled ||
                  system.bottomAirHumidity.arrayEnabled) &&
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
                timeMultiplierAdditionalCondition={system.steps.value !== 1}
                handleChange={handleChange}
                charts={charts}
                variables={COOLING_TOWER_DIAGRAM_VARIABLES}
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

export default CoolingTower;
