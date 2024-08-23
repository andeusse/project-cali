import {
  Grid,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Accordion,
  AccordionDetails,
  AccordionSummary,
  Typography,
  TextField,
  Box,
  Tab,
  Button,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import React, { useState } from 'react';
import CustomNumberField from '../../components/UI/CustomNumberField';
import {
  SMART_CITY,
  SmartSystemOutput,
  SmartSystemParameters,
  SortableItemParameter,
} from '../../types/scenarios/common';
import { getValueByKey } from '../../utils/getValueByKey';
import { setFormState } from '../../utils/setFormState';
import ErrorDialog from '../../components/UI/ErrorDialog';

import illustration from '../../assets/illustrations/smartCity.png';
import {
  ScenariosModesType,
  ScenariosModesText,
  SmartSystemType,
} from '../../types/scenarios/common';
import SolarTab from '../../components/scenarios/system/SolarTab';
import { TabContext, TabList, TabPanel } from '@mui/lab';
import {
  setSolarSystemArraysById,
  setSolarSystemById,
} from '../../utils/scenarios/setSolarSystem';
import BatteryTab from '../../components/scenarios/system/BatteryTab';
import {
  setBatterySystemArraysById,
  setBatterySystemById,
} from '../../utils/scenarios/setBatterySystem';
import { setBiogasSystemById } from '../../utils/scenarios/setBiogasSystem';
import {
  setLoadSystemArraysById,
  setLoadSystemById,
} from '../../utils/scenarios/setLoadSystem';
import {
  setHydraulicSystemArraysById,
  setHydraulicSystemById,
} from '../../utils/scenarios/setHydraulicSystem';
import {
  setWindSystemArraysById,
  setWindSystemById,
} from '../../utils/scenarios/setWindSystem';
import { CellChange } from '@silevis/reactgrid';
import HydraulicTab from '../../components/scenarios/system/HydraulicTab';
import WindTab from '../../components/scenarios/system/WindTab';
import BiogasTab from '../../components/scenarios/system/BiogasTab';
import LoadTab from '../../components/scenarios/system/LoadTab';
import ResultTab from '../../components/scenarios/common/ResultTab';

import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import RestartAltIcon from '@mui/icons-material/RestartAlt';
import { updateScenario } from '../../api/scenario';
import { AxiosError } from 'axios';
import { errorResp } from '../../types/api';
import SortableList from '../../components/UI/SortableList';
import { useAppDispatch } from '../../redux/reduxHooks';
import { setIsLoading } from '../../redux/slices/isLoadingSlice';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import FileUploadIcon from '@mui/icons-material/FileUpload';
import saveAs from 'file-saver';
import { StepUnitText, StepUnitType } from '../../types/common';

const tabs = [
  'solar',
  'battery',
  'hydraulic',
  'wind',
  'biogas',
  'load',
  'result',
];

const SmartCity = () => {
  const [system, setSystem] = useState({ ...SMART_CITY });
  const [isOpen, setIsOpen] = useState(false);
  const [isImageExpanded, setIsImageExpanded] = useState(true);
  const [isParametersExpanded, setIsParametersExpanded] = useState(true);
  const [selectedTab, setSelectedTab] = useState<string>('solar');

  const [sortableList, setSortableList] = useState(system.priorityList);

  const [data, setData] = useState<SmartSystemOutput | undefined>(undefined);
  const [error, setError] = useState('');

  const dispatch = useAppDispatch();

  const handleChange = (e: any, variableName?: string) => {
    chooseTab(e.target.name, parseInt(e.target.value));
    const newState = setFormState<SmartSystemParameters>(
      e,
      system,
      variableName
    );
    if (newState) {
      setSystem(newState as SmartSystemParameters);
      setSortableList((newState as SmartSystemParameters).priorityList);
    }
  };

  const handleSystemChange = (e: any, id: string, type: SmartSystemType) => {
    let newState: SmartSystemParameters = { ...SMART_CITY };
    if (type === SmartSystemType.Solar) {
      newState = setSolarSystemById(e, system, id);
    }
    if (type === SmartSystemType.Battery) {
      newState = setBatterySystemById(e, system, id);
    }
    if (type === SmartSystemType.Biogas) {
      newState = setBiogasSystemById(e, system, id);
    }
    if (type === SmartSystemType.Load) {
      newState = setLoadSystemById(e, system, id);
    }
    if (type === SmartSystemType.Hydraulic) {
      newState = setHydraulicSystemById(e, system, id);
    }
    if (type === SmartSystemType.Wind) {
      newState = setWindSystemById(e, system, id);
    }
    setSystem(newState as SmartSystemParameters);
    setSortableList((newState as SmartSystemParameters).priorityList);
  };

  const handleTableChange = (
    e: CellChange[],
    id: string,
    type: SmartSystemType
  ) => {
    let newState: SmartSystemParameters = { ...SMART_CITY };
    if (type === SmartSystemType.Solar) {
      newState = setSolarSystemArraysById({ e, oldState: system, id });
    }
    if (type === SmartSystemType.Battery) {
      newState = setBatterySystemArraysById({ e, oldState: system, id });
    }
    if (type === SmartSystemType.Hydraulic) {
      newState = setHydraulicSystemArraysById({ e, oldState: system, id });
    }
    if (type === SmartSystemType.Load) {
      newState = setLoadSystemArraysById({ e, oldState: system, id });
    }
    if (type === SmartSystemType.Wind) {
      newState = setWindSystemArraysById({ e, oldState: system, id });
    }
    setSystem(newState as SmartSystemParameters);
  };

  const handleTabChange = (event: React.SyntheticEvent, newValue: string) => {
    setSelectedTab(newValue);
  };

  const handleQueryScenario = () => {
    dispatch(setIsLoading(true));
    updateScenario('smartcity', system)
      .then((resp) => {
        setData(() => {
          const newData = JSON.parse(resp.data);
          return newData;
        });
        setSelectedTab('result');
      })
      .catch((err: AxiosError<errorResp>) => {
        setData(undefined);
        setError(err.message);
        setIsOpen(true);
      })
      .finally(() => {
        dispatch(setIsLoading(false));
      });
  };

  const handleResetScenario = () => {
    chooseTab('solarSystemNumber', system.solarSystemNumber.value, true);
    setData(undefined);
    setError('');
  };

  const reorder = (
    list: SortableItemParameter[],
    startIndex: number,
    endIndex: number
  ) => {
    const result = [...list];
    const [removed] = result.splice(startIndex, 1);
    result.splice(endIndex, 0, removed);
    setSystem({
      ...system,
      priorityList: result,
    });
    return result;
  };

  const chooseTab = (name: string, value: number, removeResult?: boolean) => {
    const currentTab = selectedTab;
    if (name.includes('SystemNumber')) {
      let tempTabs = [...tabs];
      if (removeResult) {
        tempTabs = tempTabs.filter((f) => f !== 'result');
      }
      if (
        (name.includes('solar') && value === 0) ||
        system.solarSystemNumber.value === 0
      ) {
        tempTabs = tempTabs.filter((f) => f !== 'solar');
      }
      if (
        (name.includes('battery') && value === 0) ||
        system.batterySystemNumber.value === 0
      ) {
        tempTabs = tempTabs.filter((f) => f !== 'battery');
      }
      if (
        (name.includes('hydraulic') && value === 0) ||
        system.hydraulicSystemNumber.value === 0
      ) {
        tempTabs = tempTabs.filter((f) => f !== 'hydraulic');
      }
      if (
        (name.includes('wind') && value === 0) ||
        system.windSystemNumber.value === 0
      ) {
        tempTabs = tempTabs.filter((f) => f !== 'wind');
      }
      if (
        (name.includes('biogas') && value === 0) ||
        system.biogasSystemNumber.value === 0
      ) {
        tempTabs = tempTabs.filter((f) => f !== 'biogas');
      }
      if (
        (name.includes('load') && value === 0) ||
        system.loadSystemNumber.value === 0
      ) {
        tempTabs = tempTabs.filter((f) => f !== 'load');
      }
      if (!tempTabs.includes(currentTab)) {
        setSelectedTab(tempTabs[0]);
      }
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
        const jsonData: SmartSystemParameters = JSON.parse(
          e.target.result
        ) as SmartSystemParameters;
        if ('solarSystemNumber' in jsonData) {
          setSystem(jsonData);
        } else {
          setError('El archivo no corresponde a un escenario');
          setIsOpen(true);
        }
        event.target.value = '';
      };
      reader.readAsText(selectedFile);
    }
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
                src={illustration}
                alt="smartCityIllustration"
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
              aria-controls="panel1-content"
              id="panel1-header"
              sx={{ margin: 0 }}
            >
              <Typography variant="h4">Parámetros</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <Grid container spacing={2}>
                <Grid item xs={12} md={12} xl={12}>
                  <Typography variant="h6">Parámetros del sistema</Typography>
                </Grid>
                <Grid item xs={12} md={12} xl={12}>
                  <FormControl fullWidth>
                    <TextField
                      label="Nombre"
                      value={system.name}
                      name="name"
                      autoComplete="off"
                      onChange={handleChange}
                    />
                  </FormControl>
                </Grid>
                <Grid item xs={12} md={3} xl={3}>
                  <FormControl fullWidth>
                    <InputLabel id="operation-mode-type">
                      Modo de operación
                    </InputLabel>
                    <Select
                      labelId="operation-mode-type"
                      label="Modo de operación"
                      value={system.operationMode}
                      name="operationMode"
                      onChange={(e: any) => handleChange(e)}
                    >
                      {Object.keys(ScenariosModesType).map((key) => (
                        <MenuItem key={key} value={key}>
                          {getValueByKey(ScenariosModesText, key)}
                        </MenuItem>
                      ))}
                    </Select>
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
                      disabled={
                        system.operationMode === ScenariosModesType.Automatic &&
                        system.batterySystemNumber.value !== 0
                      }
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
                {system.operationMode === ScenariosModesType.Manual && (
                  <Grid item xs={12} md={12} xl={12}>
                    <Typography variant="subtitle1">
                      Modo manual: Las potencias de los generadores, sistemas de
                      almacenamiento y cargas de la red se determinan por los
                      parámetros y condiciones operativas que configure el
                      usuario.
                    </Typography>
                  </Grid>
                )}
                {system.operationMode === ScenariosModesType.Automatic && (
                  <Grid item xs={12} md={12} xl={12}>
                    <Typography variant="subtitle1">
                      Modo automático: La herramienta realiza el cálculo óptimo
                      de generación y consumo de potencia de los recursos,
                      basado en la solución óptima de un problema de balance de
                      energía sujeto a restricciones, considerando el orden de
                      prioridad de los generadores.
                    </Typography>
                  </Grid>
                )}
                {system.priorityList.length !== 0 &&
                  system.operationMode === ScenariosModesType.Automatic && (
                    <>
                      <Grid item xs={12} md={12} xl={12}>
                        <Typography variant="h6">
                          Orden de prioridad de recursos
                        </Typography>
                      </Grid>
                      <Grid item xs={12} md={12} xl={12}>
                        <div style={{ maxHeight: '470px', overflow: 'auto' }}>
                          <SortableList
                            list={sortableList}
                            setList={setSortableList}
                            reorder={reorder}
                          ></SortableList>
                        </div>
                      </Grid>
                    </>
                  )}
                <Grid item xs={12} md={12} xl={12}>
                  <Typography variant="h6">
                    Configuración de escenario
                  </Typography>
                </Grid>
                <Grid item xs={12} md={4} xl={4}>
                  <CustomNumberField
                    variable={system.solarSystemNumber}
                    name="solarSystemNumber"
                    handleChange={handleChange}
                    isInteger={true}
                    disableKeyDown={true}
                  ></CustomNumberField>
                </Grid>
                <Grid item xs={12} md={4} xl={4}>
                  <CustomNumberField
                    variable={system.hydraulicSystemNumber}
                    name="hydraulicSystemNumber"
                    handleChange={handleChange}
                    isInteger={true}
                    disableKeyDown={true}
                  ></CustomNumberField>
                </Grid>
                <Grid item xs={12} md={4} xl={4}>
                  <CustomNumberField
                    variable={system.windSystemNumber}
                    name="windSystemNumber"
                    handleChange={handleChange}
                    isInteger={true}
                    disableKeyDown={true}
                  ></CustomNumberField>
                </Grid>
                <Grid item xs={12} md={4} xl={4}>
                  <CustomNumberField
                    variable={system.biogasSystemNumber}
                    name="biogasSystemNumber"
                    handleChange={handleChange}
                    isInteger={true}
                    disableKeyDown={true}
                  ></CustomNumberField>
                </Grid>
                <Grid item xs={12} md={4} xl={4}>
                  <CustomNumberField
                    variable={system.batterySystemNumber}
                    name="batterySystemNumber"
                    handleChange={handleChange}
                    isInteger={true}
                    disableKeyDown={true}
                  ></CustomNumberField>
                </Grid>
                <Grid item xs={12} md={4} xl={4}>
                  <CustomNumberField
                    variable={system.loadSystemNumber}
                    name="loadSystemNumber"
                    handleChange={handleChange}
                    isInteger={true}
                    disableKeyDown={true}
                  ></CustomNumberField>
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
        <Grid
          item
          xs={12}
          md={12}
          xl={12}
          sx={{ paddingTop: '0px', textAlign: 'center' }}
        >
          <Button
            variant="contained"
            color="success"
            onClick={handleQueryScenario}
            startIcon={<PlayArrowIcon />}
            sx={{ width: '120px', margin: '5px' }}
          >
            Simular
          </Button>
          <Button
            variant="contained"
            color="error"
            disabled={data === undefined}
            onClick={handleResetScenario}
            startIcon={<RestartAltIcon />}
            sx={{ width: '120px', margin: '5px' }}
          >
            Reiniciar
          </Button>
        </Grid>
        <Grid item xs={12} md={12} xl={12}>
          <TabContext value={selectedTab}>
            <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
              <TabList
                onChange={handleTabChange}
                aria-label="Monitoring tabs"
                variant="scrollable"
                allowScrollButtonsMobile
              >
                {system.solarSystemNumber.value !== 0 && (
                  <Tab key={'solar'} label={'Solar'} value={'solar'} />
                )}
                {system.batterySystemNumber.value !== 0 && (
                  <Tab key={'battery'} label={'BESS'} value={'battery'} />
                )}
                {system.hydraulicSystemNumber.value !== 0 && (
                  <Tab
                    key={'hydraulic'}
                    label={'Hidráulico'}
                    value={'hydraulic'}
                  />
                )}
                {system.windSystemNumber.value !== 0 && (
                  <Tab key={'wind'} label={'Eólico'} value={'wind'} />
                )}
                {system.biogasSystemNumber.value !== 0 && (
                  <Tab key={'biogas'} label={'Biogás'} value={'biogas'} />
                )}
                {system.loadSystemNumber.value !== 0 && (
                  <Tab key={'load'} label={'Carga'} value={'load'} />
                )}
                {data !== undefined && (
                  <Tab key={'result'} label={'Resultados'} value={'result'} />
                )}
              </TabList>
            </Box>
            <TabPanel key={'solar'} value={'solar'}>
              {system.solarSystemNumber.value !== 0 && (
                <SolarTab
                  system={system}
                  handleSystemChange={handleSystemChange}
                  handleTableChange={handleTableChange}
                ></SolarTab>
              )}
            </TabPanel>
            <TabPanel key={'battery'} value={'battery'}>
              {system.batterySystemNumber.value !== 0 && (
                <BatteryTab
                  system={system}
                  handleSystemChange={handleSystemChange}
                  handleTableChange={handleTableChange}
                ></BatteryTab>
              )}
            </TabPanel>
            <TabPanel key={'hydraulic'} value={'hydraulic'}>
              {system.hydraulicSystemNumber.value !== 0 && (
                <HydraulicTab
                  system={system}
                  handleSystemChange={handleSystemChange}
                  handleTableChange={handleTableChange}
                ></HydraulicTab>
              )}
            </TabPanel>
            <TabPanel key={'wind'} value={'wind'}>
              {system.windSystemNumber.value !== 0 && (
                <WindTab
                  system={system}
                  handleSystemChange={handleSystemChange}
                  handleTableChange={handleTableChange}
                ></WindTab>
              )}
            </TabPanel>
            <TabPanel key={'biogas'} value={'biogas'}>
              {system.biogasSystemNumber.value !== 0 && (
                <BiogasTab
                  system={system}
                  handleSystemChange={handleSystemChange}
                  handleTableChange={handleTableChange}
                ></BiogasTab>
              )}
            </TabPanel>
            <TabPanel key={'load'} value={'load'}>
              {system.loadSystemNumber.value !== 0 && (
                <LoadTab
                  system={system}
                  handleSystemChange={handleSystemChange}
                  handleTableChange={handleTableChange}
                ></LoadTab>
              )}
            </TabPanel>
            <TabPanel key={'result'} value={'result'}>
              {data !== undefined && <ResultTab data={data}></ResultTab>}
            </TabPanel>
          </TabContext>
        </Grid>
      </Grid>
    </>
  );
};

export default SmartCity;
