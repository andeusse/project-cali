import {
  FormControl,
  FormControlLabel,
  Grid,
  InputLabel,
  MenuItem,
  Select,
  Switch,
} from '@mui/material';
import CustomNumberField from '../../UI/CustomNumberField';
import { ControllerStateType } from '../../../types/models/turbine';
import { TurbineParamsType } from '../../../types/models/common';

const ControllerParams = (props: TurbineParamsType) => {
  const { turbine, handleChange } = props;

  return (
    <>
      <h3>Controlador de carga</h3>
      <Grid container spacing={2} margin={'normal'}>
        <Grid item xs={6} md={6} xl={6}>
          <FormControl fullWidth>
            <InputLabel>Estado inicial disipación</InputLabel>
            <Select
              label="Estado inicial disipación"
              value={turbine.sinkLoadInitialState}
              name="controllerInitialState"
              onChange={handleChange}
            >
              {Object.keys(ControllerStateType).map((key) => (
                <MenuItem key={key} value={key}>
                  {key}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>
        <Grid item xs={6} md={6} xl={6}>
          <FormControlLabel
            control={
              <Switch
                checked={turbine.controllerCustomize}
                name="controllerCustomize"
                onChange={handleChange}
                color="default"
              />
            }
            label={turbine.controllerCustomize ? 'Manual' : 'Auto'}
          />
        </Grid>
        <Grid item xs={6} md={6} xl={6}>
          <CustomNumberField
            variable={turbine.controllerEfficiency}
            name="controllerEfficiency"
          ></CustomNumberField>
        </Grid>
        <Grid item xs={6} md={6} xl={6}>
          <CustomNumberField
            variable={turbine.controllerChargeVoltageBulk}
            name="controllerChargeVoltageBulk"
            handleChange={handleChange}
          ></CustomNumberField>
        </Grid>
        <Grid item xs={6} md={6} xl={6}>
          <CustomNumberField
            variable={turbine.controllerChargeVoltageFloat}
            name="controllerChargeVoltageFloat"
            handleChange={handleChange}
          ></CustomNumberField>
        </Grid>
        <Grid item xs={6} md={6} xl={6}>
          <CustomNumberField
            variable={turbine.controllerChargingMinimunVoltage}
            name="controllerChargingMinimunVoltage"
            handleChange={handleChange}
          ></CustomNumberField>
        </Grid>
        <Grid item xs={6} md={6} xl={6}>
          <CustomNumberField
            variable={turbine.controllerSinkOffVoltage}
            name="controllerDissipatorOffVoltage"
            handleChange={handleChange}
          ></CustomNumberField>
        </Grid>
        <Grid item xs={6} md={6} xl={6}>
          <CustomNumberField
            variable={turbine.controllerSinkOnVoltage}
            name="controllerDissipatorOnVoltage"
            handleChange={handleChange}
          ></CustomNumberField>
        </Grid>
      </Grid>
    </>
  );
};

export default ControllerParams;
