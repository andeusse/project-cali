import React from 'react';
import { FormControlLabel, Grid, Switch } from '@mui/material';
import { TurbineParamsType } from '../../../types/models/common';
import ToggleCustomNumberField from '../../UI/ToggleCustomNumberField';
import { TurbineType } from '../../../types/models/turbine';

const InputParams = (props: TurbineParamsType) => {
  const { turbine, handleChange } = props;

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
                checked={turbine.inputOfflineOperation}
                name="inputOfflineOperation"
                onChange={handleChange}
                color="default"
              />
            }
            label={turbine.inputOfflineOperation ? 'Offline' : 'Online'}
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
            variable={turbine.inputPressure}
            name="inputPressure"
            handleChange={handleChange}
            offlineOperation={turbine.inputOfflineOperation}
          ></ToggleCustomNumberField>
        </Grid>
        <Grid item xs={12} md={12} xl={12}>
          <ToggleCustomNumberField
            variable={turbine.inputFlow}
            name="inputFlow"
            handleChange={handleChange}
            offlineOperation={turbine.inputOfflineOperation}
          ></ToggleCustomNumberField>
        </Grid>
        {turbine.turbineType === TurbineType.Turgo && (
          <>
            <Grid item xs={12} md={12} xl={12}>
              <h3>Parámetros carga CD</h3>
            </Grid>
            <FormControlLabel
              control={
                <Switch
                  checked={turbine.inputDirectCurrentPower}
                  name="inputDirectCurrentPower"
                  onChange={(e) => {
                    if (handleChange) {
                      handleChange(e);
                    }
                  }}
                  color="default"
                />
              }
              label={
                turbine.inputDirectCurrentPower
                  ? 'Conectado: 2.4 W'
                  : 'Desconectado: 0.0 W'
              }
            />
          </>
        )}
        <Grid item xs={12} md={12} xl={12}>
          <h3>Parámetros carga CA</h3>
        </Grid>
        <Grid item xs={12} md={12} xl={12}>
          <ToggleCustomNumberField
            variable={turbine.inputActivePower}
            name="inputActivePower"
            handleChange={handleChange}
            offlineOperation={turbine.inputOfflineOperation}
          ></ToggleCustomNumberField>
        </Grid>
        <Grid item xs={12} md={12} xl={12}>
          <ToggleCustomNumberField
            variable={turbine.inputPowerFactor}
            name="inputPowerFactor"
            step={0.1}
            handleChange={handleChange}
            offlineOperation={turbine.inputOfflineOperation}
          ></ToggleCustomNumberField>
        </Grid>
      </Grid>
    </>
  );
};

export default InputParams;
