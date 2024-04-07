import { Grid } from '@mui/material';
import React from 'react';
import CustomNumberField from '../UI/CustomNumberField';
import { SolarPanel as Panel } from '../../types/models/common';
import CustomToggle from '../UI/CustomToggle';

type Props = {
  name: string;
  propertyName: string;
  panel: Panel;
  handleChange: (e: any) => void;
};

const SolarPanel = (props: Props) => {
  const { name, propertyName, panel, handleChange } = props;

  return (
    <>
      <h3>Panel {name}</h3>
      <Grid container spacing={2}>
        <Grid
          item
          xs={12}
          md={12}
          xl={12}
          alignContent={'center'}
          height={'72px'}
        >
          <CustomToggle
            name={`${propertyName}.isConnected`}
            value={panel.isConnected}
            handleChange={handleChange}
            trueString="Conectado"
            falseString="Desconectado"
          ></CustomToggle>
        </Grid>
        <Grid item xs={12} md={12} xl={12}>
          <CustomNumberField variable={panel.peakPower}></CustomNumberField>
        </Grid>
        <Grid item xs={12} md={12} xl={6}>
          <CustomNumberField
            variable={panel.deratingFactor}
            name={`${propertyName}.deratingFactor`}
            handleChange={handleChange}
          ></CustomNumberField>
        </Grid>
        <Grid item xs={12} md={12} xl={6}>
          <CustomNumberField variable={panel.efficiency}></CustomNumberField>
        </Grid>
        <Grid item xs={12} md={12} xl={6}>
          <CustomNumberField
            variable={panel.nominalIrradiance}
          ></CustomNumberField>
        </Grid>
        <Grid item xs={12} md={12} xl={6}>
          <CustomNumberField
            variable={panel.nominalTemperature}
          ></CustomNumberField>
        </Grid>
        <Grid item xs={12} md={12} xl={6}>
          <CustomNumberField
            variable={panel.testIrradiance}
          ></CustomNumberField>
        </Grid>
        <Grid item xs={12} md={12} xl={6}>
          <CustomNumberField
            variable={panel.testTemperature}
          ></CustomNumberField>
        </Grid>
        <Grid item xs={12} md={12} xl={6}>
          <CustomNumberField
            variable={panel.operatingTemperature}
          ></CustomNumberField>
        </Grid>
        <Grid item xs={12} md={12} xl={6}>
          <CustomNumberField
            variable={panel.temperatureVariationCoefficient}
          ></CustomNumberField>
        </Grid>
      </Grid>
    </>
  );
};

export default SolarPanel;
