import { Grid } from '@mui/material';
import CustomNumberField from '../../UI/CustomNumberField';
import { TurbineParamsType } from '../../../types/models/common';

const BatteryParams = (props: TurbineParamsType) => {
  const { turbine, handleChange } = props;

  return (
    <>
      <h3>Baterías</h3>
      <Grid container spacing={2} margin={'normal'}>
        <Grid item xs={6} md={6} xl={6}>
          <CustomNumberField
            variable={turbine.batteryStateOfCharge}
            name="batteryStateOfCharge"
            min={0}
            max={100}
            handleChange={handleChange}
          ></CustomNumberField>
        </Grid>
        <Grid item xs={6} md={6} xl={6}>
          <CustomNumberField
            variable={turbine.batteryTemperatureCoefficient}
            name="batteryTemperatureCoefficient"
          ></CustomNumberField>
        </Grid>
        <Grid item xs={6} md={6} xl={6}>
          <CustomNumberField
            variable={turbine.batteryCapacity}
            name="batteryCapacity"
          ></CustomNumberField>
        </Grid>
        <Grid item xs={6} md={6} xl={6}>
          <CustomNumberField
            variable={turbine.batterySelfDischargeCoefficient}
            name="batterySelfDischargeCoefficient"
          ></CustomNumberField>
        </Grid>
        <Grid item xs={6} md={6} xl={6}>
          <CustomNumberField
            variable={turbine.batteryChargeDischargeEfficiency}
            name="batteryChargeDischargeEfficiency"
          ></CustomNumberField>
        </Grid>
        <Grid item xs={6} md={6} xl={6}>
          <CustomNumberField
            variable={turbine.batteryTemperatureCompensationCoefficient}
            name="batteryTemperatureCompensationCoefficient"
          ></CustomNumberField>
        </Grid>
      </Grid>
    </>
  );
};

export default BatteryParams;
