import {
  Grid,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  SelectChangeEvent,
} from '@mui/material';
import CustomNumberField from '../../UI/CustomNumberField';
import {
  TurbineType,
  PELTON_TURBINE,
  TURGO_TURBINE,
} from '../../../types/models/turbine';

type Props = {
  selectedTurbine: TurbineType;
  handleChange: (e: SelectChangeEvent<TurbineType>) => void;
};

const TurbineParams = (props: Props) => {
  const { selectedTurbine, handleChange } = props;

  return (
    <>
      <h3>Turbinas</h3>
      <Grid container spacing={2} margin={'normal'}>
        <Grid item xs={12} md={12} xl={12}>
          <FormControl fullWidth>
            <InputLabel id="turbine-type">Tipo de turbina</InputLabel>
            <Select
              labelId="turbine-type"
              label="Tipo de turbina"
              value={selectedTurbine}
              name="turbineType"
              onChange={handleChange}
            >
              {Object.keys(TurbineType).map((key) => (
                <MenuItem key={key} value={key}>
                  {key}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>
        {selectedTurbine === TurbineType.Pelton &&
          PELTON_TURBINE.map((variable) => (
            <Grid
              key={variable.variableString + variable.variableSubString}
              item
              xs={6}
              md={6}
              xl={6}
            >
              <CustomNumberField variable={variable}></CustomNumberField>
            </Grid>
          ))}
        {selectedTurbine === TurbineType.Turgo &&
          TURGO_TURBINE.map((variable) => (
            <Grid
              key={variable.variableString + variable.variableSubString}
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
