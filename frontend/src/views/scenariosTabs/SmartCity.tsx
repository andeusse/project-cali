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
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import React, { useState } from 'react';
import CustomNumberField from '../../components/UI/CustomNumberField';
import {
  SMART_CITY,
  SMART_CITY_TABS,
  SmartCityParameters,
} from '../../types/models/smartCity';
import { getValueByKey } from '../../utils/getValueByKey';
import { setFormState } from '../../utils/setFormState';
import ErrorDialog from '../../components/UI/ErrorDialog';

import smartCityIllustration from '../../assets/illustrations/smartCity.png';
import {
  ScenariosModesType,
  ScenariosStepUnitType,
  ScenariosStepUnitText,
  ScenariosModesText,
} from '../../types/models/common';
import CustomTab from '../../components/UI/CustomTab';
import { TabType } from '../../types/tab';

type Props = {};

const SmartCity = (props: Props) => {
  const [system, setSystem] = useState(SMART_CITY);
  const [isOpen, setIsOpen] = useState(false);
  const [isImageExpanded, setIsImageExpanded] = useState(true);
  const [isParametersExpanded, setIsParametersExpanded] = useState(true);

  const [tabs, setTabs] = useState<TabType[]>(SMART_CITY_TABS);

  const error = '';

  const handleChange = (e: any, variableName?: string) => {
    const newState = setFormState<SmartCityParameters>(e, system, variableName);
    if (newState) {
      setSystem(newState as SmartCityParameters);
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
                  height: '500px',
                  display: 'block',
                  marginLeft: 'auto',
                  marginRight: 'auto',
                }}
                src={smartCityIllustration}
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
                  ></CustomNumberField>
                </Grid>
                <Grid item xs={12} md={4} xl={4}>
                  <CustomNumberField
                    variable={system.hydraulicSystemNumber}
                    name="hydraulicSystemNumber"
                    handleChange={handleChange}
                  ></CustomNumberField>
                </Grid>
                <Grid item xs={12} md={4} xl={4}>
                  <CustomNumberField
                    variable={system.windSystemNumber}
                    name="windSystemNumber"
                    handleChange={handleChange}
                  ></CustomNumberField>
                </Grid>
                <Grid item xs={12} md={4} xl={4}>
                  <CustomNumberField
                    variable={system.biogasSystemNumber}
                    name="biogasSystemNumber"
                    handleChange={handleChange}
                  ></CustomNumberField>
                </Grid>
                <Grid item xs={12} md={4} xl={4}>
                  <CustomNumberField
                    variable={system.batterySystemNumber}
                    name="batterySystemNumber"
                    handleChange={handleChange}
                  ></CustomNumberField>
                </Grid>
                <Grid item xs={12} md={4} xl={4}>
                  <CustomNumberField
                    variable={system.loadSystemNumber}
                    name="loadSystemNumber"
                    handleChange={handleChange}
                  ></CustomNumberField>
                </Grid>
              </Grid>
            </AccordionDetails>
          </Accordion>
        </Grid>
        <Grid item xs={12} md={12} xl={12}>
          <CustomTab tabs={tabs}></CustomTab>
        </Grid>
      </Grid>
    </>
  );
};

export default SmartCity;
