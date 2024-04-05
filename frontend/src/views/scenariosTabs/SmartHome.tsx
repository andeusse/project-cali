import {
  Alert,
  Box,
  FormControl,
  Grid,
  InputLabel,
  MenuItem,
  Select,
} from '@mui/material';
import React, { useState } from 'react';
import {
  SMART_CITY,
  SmartCityOperationModesType,
  SmartCityParameters,
  StepUnitType,
} from '../../types/models/smartCity';
import { setFormState } from '../../utils/setFormState';
import CustomNumberField from '../../components/UI/CustomNumberField';
import { getValueByKey } from '../../utils/getValueByKey';

type Props = {};

const SmartHome = (props: Props) => {
  const [smartHome, setSmartHome] = useState(SMART_CITY);

  const error = '';

  const handleChange = (e: any, variableName?: string) => {
    const newState = setFormState<SmartCityParameters>(
      e,
      smartHome,
      variableName
    );
    if (newState) {
      setSmartHome(newState as SmartCityParameters);
    }
  };

  return (
    <>
      {error !== '' && (
        <Alert severity="error" variant="filled">
          {error}
        </Alert>
      )}
      <Box display="flex" justifyContent="center" alignItems="center">
        <h2>Parámetros del sistema</h2>
      </Box>
      <Grid container spacing={2}>
        <Grid item xs={3} md={3} xl={3}>
          <FormControl fullWidth>
            <InputLabel id="operation-mode-type">Modo de operación</InputLabel>
            <Select
              labelId="operation-mode-type"
              label="Modo de operación"
              value={smartHome.operationMode}
              name="operationMode"
              onChange={(e: any) => handleChange(e)}
            >
              {Object.keys(SmartCityOperationModesType).map((key) => (
                <MenuItem key={key} value={key}>
                  {getValueByKey(SmartCityOperationModesType, key)}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>
        <Grid item xs={3} md={3} xl={3}>
          <CustomNumberField
            variable={smartHome.steps}
            name="steps"
            handleChange={handleChange}
          ></CustomNumberField>
        </Grid>
        <Grid item xs={3} md={3} xl={3}>
          <CustomNumberField
            variable={smartHome.stepTime}
            name="stepTime"
            handleChange={handleChange}
          ></CustomNumberField>
        </Grid>
        <Grid item xs={3} md={3} xl={3}>
          <FormControl fullWidth>
            <InputLabel id="step-unit-type">Unidad</InputLabel>
            <Select
              labelId="step-unit-type"
              label="Unidad"
              value={smartHome.stepUnit}
              name="stepUnit"
              onChange={(e: any) => handleChange(e)}
            >
              {Object.keys(StepUnitType).map((key) => (
                <MenuItem key={key} value={key}>
                  {getValueByKey(StepUnitType, key)}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>
        <Grid item xs={3} md={3} xl={3}></Grid>
        <Grid item xs={3} md={3} xl={3}></Grid>
        <Grid item xs={3} md={3} xl={3}></Grid>
        <Grid item xs={3} md={3} xl={3}></Grid>
      </Grid>
    </>
  );
};

export default SmartHome;
