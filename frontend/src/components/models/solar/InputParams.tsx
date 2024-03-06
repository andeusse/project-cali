import React from 'react';
import { SolarParamsType } from '../../../types/models/solar';
import { Grid, FormControlLabel, Switch } from '@mui/material';
import ToggleCustomNumberField from '../../UI/ToggleCustomNumberField';

const InputParams = (props: SolarParamsType) => {
  const { solarModule, handleChange } = props;

  return (
    <>
      <Grid container spacing={2}>
        <Grid item xs={12} md={12} xl={12}>
          <h2>Operación planta</h2>
        </Grid>
        <Grid item xs={12} md={12} xl={12}>
          <FormControlLabel
            control={
              <Switch
                checked={solarModule.inputOfflineOperation}
                name="inputOfflineOperation"
                onChange={handleChange}
                color="default"
              />
            }
            label="Operación offline"
          />
        </Grid>
        <Grid item xs={12} md={12} xl={12}>
          <h3>Entradas</h3>
        </Grid>
        <Grid item xs={12} md={12} xl={12}>
          <h3>Parámetros turbina</h3>
        </Grid>
        <Grid item xs={12} md={12} xl={12}>
          <ToggleCustomNumberField
            variable={solarModule.inputIrradiation}
            name="inputIrradiation"
            handleChange={handleChange}
            offlineOperation={solarModule.inputOfflineOperation}
          ></ToggleCustomNumberField>
        </Grid>
        <Grid item xs={12} md={12} xl={12}>
          <ToggleCustomNumberField
            variable={solarModule.inputTemperature}
            name="inputTemperature"
            handleChange={handleChange}
            offlineOperation={solarModule.inputOfflineOperation}
          ></ToggleCustomNumberField>
        </Grid>
      </Grid>
    </>
  );
};

export default InputParams;
