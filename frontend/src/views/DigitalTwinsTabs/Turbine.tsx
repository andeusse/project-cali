import {
  Box,
  Container,
  FormControl,
  Grid,
  InputAdornment,
  InputLabel,
  MenuItem,
  Select,
  TextField,
  Tooltip,
} from '@mui/material';
import CustomTextField from '../../components/UI/CustomTextField';

type Props = {};

const Turbine = (props: Props) => {
  return (
    <Container maxWidth="xl">
      <Box display="flex" justifyContent="center" alignItems="center">
        <h2>Parámetros del sistema</h2>
      </Box>
      <Grid container spacing={2}>
        <Grid item xs={12} md={6} xl={3}>
          <h3>Turbinas:</h3>
          <Grid container spacing={2} margin={'normal'}>
            <Grid item xs={12} md={12} xl={12}>
              <FormControl fullWidth>
                <InputLabel>Tipo de turbina</InputLabel>
                <Tooltip title="Tipo de turbina" placement="right" arrow>
                  <Select label="Tipo de turbina">
                    <MenuItem value={'Pelton'}>Pelton</MenuItem>
                    <MenuItem value={'Pelton'}>Turgo</MenuItem>
                  </Select>
                </Tooltip>
              </FormControl>
            </Grid>
            <CustomTextField
              disabled={true}
              initialValue={12.5}
              tooltip="tooltip"
              unit="kW"
              variableName="Variable Name"
            ></CustomTextField>
            <CustomTextField
              disabled={true}
              initialValue={12.5}
              tooltip="tooltip"
              unit="kW"
              variableName="Variable Name"
            ></CustomTextField>
            <CustomTextField
              disabled={true}
              initialValue={12.5}
              tooltip="tooltip"
              unit="kW"
              variableName="Variable Name"
            ></CustomTextField>
            <CustomTextField
              disabled={true}
              initialValue={12.5}
              tooltip="tooltip"
              unit="kW"
              variableName="Variable Name"
            ></CustomTextField>
          </Grid>
        </Grid>
        <Grid item xs={12} md={6} xl={3}>
          <h3>Turbinas</h3>
        </Grid>
        <Grid item xs={12} md={6} xl={3}>
          <h3>Turbinas</h3>
        </Grid>
        <Grid item xs={12} md={6} xl={3}>
          <h3>Turbinas</h3>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Turbine;
