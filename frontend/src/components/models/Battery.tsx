import { Grid } from '@mui/material';
import CustomNumberField from '../UI/CustomNumberField';
import { Battery as Bat, IsConnected } from '../../types/models/common';

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
