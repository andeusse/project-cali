import React from 'react';
import { Grid } from '@mui/material';
import { TurbineParamsType } from '../../../types/models/common';
import ToggleCustomNumberField from '../../UI/ToggleCustomNumberField';

const InputParams = (props: TurbineParamsType) => {
  const { turbine, handleChange } = props;

  return (
    <>
      <Grid container spacing={2}>
        <Grid item xs={12} md={12} xl={12}>
          <h2>Entradas</h2>
        </Grid>
        <Grid item xs={12} md={12} xl={12}>
          <h3>Parámetros turbina</h3>
        </Grid>
        <Grid item xs={12} md={12} xl={12}>
          <ToggleCustomNumberField
            variable={turbine.inputPressure}
            name="inputPressure"
            handleChange={handleChange}
          ></ToggleCustomNumberField>
        </Grid>
        <Grid item xs={12} md={12} xl={12}>
          <ToggleCustomNumberField
            variable={turbine.inputFlow}
            name="inputFlow"
            handleChange={handleChange}
          ></ToggleCustomNumberField>
        </Grid>
        <Grid item xs={12} md={12} xl={12}>
          <h3>Parámetros carga CA</h3>
        </Grid>
        <Grid item xs={12} md={12} xl={12}>
          <ToggleCustomNumberField
            variable={turbine.inputActivePower}
            name="inputActivePower"
            handleChange={handleChange}
          ></ToggleCustomNumberField>
        </Grid>
        <Grid item xs={12} md={12} xl={12}>
          <ToggleCustomNumberField
            variable={turbine.inputPowerFactor}
            name="inputPowerFactor"
            step={0.1}
            handleChange={handleChange}
          ></ToggleCustomNumberField>
        </Grid>
      </Grid>
    </>
  );
};

export default InputParams;
