import { FormControl, Grid, InputLabel, MenuItem, Select } from '@mui/material';
import React from 'react';
import {
  SmartCityOperationModesType,
  SmartCityParameters,
  StepUnitType,
} from '../../../types/models/smartCity';
import { getValueByKey } from '../../../utils/getValueByKey';
import CustomNumberField from '../../UI/CustomNumberField';

type Props = { smartHome: SmartCityParameters; handleChange: (e: any) => void };

const InputParams = (props: Props) => {
  const { smartHome, handleChange } = props;
  return (
    <>
      <Grid container spacing={2}>
        <Grid item xs={3} md={3} xl={3}>
          <FormControl fullWidth>
            <InputLabel id="operation-mode-type">Modo de operación</InputLabel>
            <Select
              labelId="operation-mode-type"
              label="Modo de operación"
              value={smartHome.operationMode}
              name="operationMode"
              onChange={handleChange}
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
              onChange={handleChange}
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

export default InputParams;
