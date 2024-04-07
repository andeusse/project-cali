import { Grid } from '@mui/material';
import React from 'react';
import CustomNumberField from '../UI/CustomNumberField';
import { Battery as Bat, IsConnected } from '../../types/models/common';
import CustomToggle from '../UI/CustomToggle';

type Props = {
  propertyName: string;
  battery: (IsConnected & Bat) | Bat;
  handleChange: (e: any) => void;
};

const Battery = (props: Props) => {
  const { propertyName, battery, handleChange } = props;
  return (
    <>
      <Grid container spacing={2}>
        {'isConnected' in battery && (
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
              value={battery.isConnected}
              handleChange={handleChange}
              trueString="Conectado"
              falseString="Desconectado"
            ></CustomToggle>
          </Grid>
        )}
        <Grid item xs={6} md={6} xl={6}>
          <CustomNumberField
            variable={battery.stateOfCharge}
            name={`${propertyName}.stateOfCharge`}
            handleChange={handleChange}
          ></CustomNumberField>
        </Grid>
        <Grid item xs={6} md={6} xl={6}>
          <CustomNumberField
            variable={battery.temperatureCoefficient}
          ></CustomNumberField>
        </Grid>
        <Grid item xs={6} md={6} xl={6}>
          <CustomNumberField variable={battery.capacity}></CustomNumberField>
        </Grid>
        <Grid item xs={6} md={6} xl={6}>
          <CustomNumberField
            variable={battery.selfDischargeCoefficient}
          ></CustomNumberField>
        </Grid>
        <Grid item xs={6} md={6} xl={6}>
          <CustomNumberField
            variable={battery.chargeDischargeEfficiency}
          ></CustomNumberField>
        </Grid>
        <Grid item xs={6} md={6} xl={6}>
          <CustomNumberField
            variable={battery.temperatureCompensationCoefficient}
          ></CustomNumberField>
        </Grid>
      </Grid>
    </>
  );
};

export default Battery;
