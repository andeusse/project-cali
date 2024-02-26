import {
  Grid,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  SelectChangeEvent,
} from '@mui/material';
import CustomNumberField from '../../../components/UI/CustomNumberField';
import {
  turbineType,
  PELTON_TURBINE,
  TURGO_TURBINE,
} from '../../../types/models/turbine';

type Props = {
  selectedTurbine: turbineType;
  handleChange: (e: SelectChangeEvent<turbineType>) => void;
};

const TurbineParams = (props: Props) => {
  const { selectedTurbine, handleChange } = props;

  return (
    <>
      <h3>Turbinas</h3>
      <Grid container spacing={2} margin={'normal'}>
        <Grid item xs={12} md={12} xl={12}>
          <FormControl fullWidth>
            <InputLabel>Tipo de turbina</InputLabel>
            <Select
              label="Tipo de turbina"
              value={selectedTurbine}
              name="turbineType"
              onChange={handleChange}
            >
              {Object.keys(turbineType).map((key) => (
                <MenuItem key={key} value={key}>
                  {key}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>
        {selectedTurbine === turbineType.Pelton &&
          PELTON_TURBINE.map((variable) => (
            <Grid
              key={variable.variableName + variable.subIndex}
              item
              xs={6}
              md={6}
              xl={6}
            >
              <CustomNumberField variable={variable}></CustomNumberField>
            </Grid>
          ))}
        {selectedTurbine === turbineType.Turgo &&
          TURGO_TURBINE.map((variable) => (
            <Grid
              key={variable.variableName + variable.subIndex}
              item
              xs={6}
              md={6}
              xl={6}
            >
              <CustomNumberField variable={variable}></CustomNumberField>
            </Grid>
          ))}
      </Grid>
    </>
  );
};

export default TurbineParams;
