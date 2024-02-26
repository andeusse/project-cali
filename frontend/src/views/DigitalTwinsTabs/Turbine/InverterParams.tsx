import { Grid } from '@mui/material';
import CustomNumberField from '../../../components/UI/CustomNumberField';
import { turbine } from '../../../types/models/turbine';

type Props = {
  turbine: turbine;
  handleChange: (e: any) => void;
};

const InverterParams = (props: Props) => {
  const { turbine, handleChange } = props;

  return (
    <>
      <h3>Inversor</h3>
      <Grid container spacing={2} margin={'normal'}>
        <Grid item xs={12} md={12} xl={12}>
          <CustomNumberField
            variable={turbine.inverterEfficiency}
            name="inverterEfficiency"
            handleChange={handleChange}
          ></CustomNumberField>
        </Grid>
        <Grid item xs={12} md={12} xl={12}>
          <CustomNumberField
            variable={turbine.inverterNominalPower}
            name="inverterNominalPower"
            handleChange={handleChange}
          ></CustomNumberField>
        </Grid>
      </Grid>
    </>
  );
};

export default InverterParams;
