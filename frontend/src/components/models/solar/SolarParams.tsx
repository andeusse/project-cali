import { FormControl, Grid, InputLabel, MenuItem, Select } from '@mui/material';
import React from 'react';
import CustomNumberField from '../../UI/CustomNumberField';
import {
  SolarPanelModulesType,
  SolarParamsType,
} from '../../../types/models/solar';
import { getValueByKey } from '../../../utils/getValueByKey';

const SolarParams = (props: SolarParamsType) => {
  const { solarModule, handleChange } = props;

  return (
    <>
      <Grid container spacing={2} margin={'normal'}>
        <Grid item xs={12} md={6} xl={6}>
          <FormControl fullWidth>
            <InputLabel id="solar-type">Tipo de módulo</InputLabel>
            <Select
              labelId="solar-type"
              label="Tipo de módulo"
              value={solarModule.panelType}
              name="panelType"
              onChange={handleChange}
            >
              {Object.keys(SolarPanelModulesType).map((key) => (
                <MenuItem key={key} value={key}>
                  {getValueByKey(SolarPanelModulesType, key)}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>
        <Grid item xs={6} md={3} xl={3}>
          <CustomNumberField
            variable={solarModule.moduleNumber}
            name="moduleNumber"
            handleChange={handleChange}
          ></CustomNumberField>
        </Grid>
        <Grid item xs={6} md={3} xl={3}>
          <CustomNumberField
            variable={solarModule.modulePeakPower}
            name="modulePeakPower"
            step={10}
            handleChange={handleChange}
          ></CustomNumberField>
        </Grid>
        <Grid item xs={6} md={3} xl={3}>
          <CustomNumberField
            variable={solarModule.moduleReductionPowerFactor}
            name="moduleReductionPowerFactor"
            step={0.01}
            handleChange={handleChange}
          ></CustomNumberField>
        </Grid>
        <Grid item xs={6} md={3} xl={3}>
          <CustomNumberField
            variable={solarModule.moduleEfficiency}
            name="moduleEfficiency"
            step={0.01}
            handleChange={handleChange}
          ></CustomNumberField>
        </Grid>
        <Grid item xs={6} md={3} xl={3}>
          <CustomNumberField
            variable={solarModule.moduleStandardTestIrradiation}
            name="moduleStandardTestIrradiation"
            step={10}
            handleChange={handleChange}
          ></CustomNumberField>
        </Grid>
        <Grid item xs={6} md={3} xl={3}>
          <CustomNumberField
            variable={solarModule.moduleStantardTestTemperature}
            name="moduleStantardTestTemperature"
            step={0.01}
            handleChange={handleChange}
          ></CustomNumberField>
        </Grid>
        <Grid item xs={6} md={3} xl={3}>
          <CustomNumberField
            variable={solarModule.moduleStandardIrradiation}
            name="moduleStandardIrradiation"
            step={10}
            handleChange={handleChange}
          ></CustomNumberField>
        </Grid>
        <Grid item xs={6} md={3} xl={3}>
          <CustomNumberField
            variable={solarModule.moduleStandardTemperature}
            name="moduleStandardTemperature"
            step={0.01}
            handleChange={handleChange}
          ></CustomNumberField>
        </Grid>
        <Grid item xs={6} md={3} xl={3}>
          <CustomNumberField
            variable={solarModule.moduleEnvironmentTemperature}
            name="moduleEnvironmentTemperature"
            step={0.01}
            handleChange={handleChange}
          ></CustomNumberField>
        </Grid>
        <Grid item xs={6} md={3} xl={3}>
          <CustomNumberField
            variable={solarModule.moduleCoefficientPowerVariation}
            name="moduleCoefficientPowerVariation"
            step={0.01}
            handleChange={handleChange}
          ></CustomNumberField>
        </Grid>
      </Grid>
    </>
  );
};

export default SolarParams;
