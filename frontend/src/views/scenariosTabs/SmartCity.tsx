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
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import React, { useState } from 'react';
import CustomNumberField from '../../components/UI/CustomNumberField';
import {
  SMART_CITY,
  SmartSystemParameters,
} from '../../types/scenarios/common';
import { getValueByKey } from '../../utils/getValueByKey';
import { setFormState } from '../../utils/setFormState';
import ErrorDialog from '../../components/UI/ErrorDialog';

import illustration from '../../assets/illustrations/smartCity.png';
import {
  ScenariosModesType,
  ScenariosModesText,
  ScenariosStepUnitType,
  ScenariosStepUnitText,
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
import {
  setBiogasSystemArraysById,
  setBiogasSystemById,
} from '../../utils/scenarios/setBiogasSystem';
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

type Props = {};

const SmartCity = (props: Props) => {
  const [system, setSystem] = useState({ ...SMART_CITY });
  const [isOpen, setIsOpen] = useState(false);
  const [isImageExpanded, setIsImageExpanded] = useState(false);
  const [isParametersExpanded, setIsParametersExpanded] = useState(true);
  const [selectedTab, setSelectedTab] = useState<string>('solar');

  const error = '';

  const handleChange = (e: any, variableName?: string) => {
    const newState = setFormState<SmartSystemParameters>(
      e,
      system,
      variableName
    );
    if (newState) {
      setSystem(newState as SmartSystemParameters);
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
    if (type === SmartSystemType.Biogas) {
      newState = setBiogasSystemArraysById({ e, oldState: system, id });
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
              <Typography variant="h4">Parámametros</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <Grid container spacing={2}>
                <Grid item xs={12} md={12} xl={12}>
                  <Typography variant="h6">Parámametros del sistema</Typography>
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
                      onChange={(e: any) => handleChange(e)}
                    >
                      {Object.keys(ScenariosStepUnitType).map((key) => (
                        <MenuItem key={key} value={key}>
                          {getValueByKey(ScenariosStepUnitText, key)}
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                </Grid>
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
                  <Tab key={'hidro'} label={'Hidro'} value={'hidro'} />
                )}
                {system.windSystemNumber.value !== 0 && (
                  <Tab key={'wind'} label={'Eólico'} value={'wind'} />
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
            <TabPanel key={'hidro'} value={'hidro'}>
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
          </TabContext>
        </Grid>
      </Grid>
    </>
  );
};

export default SmartCity;
