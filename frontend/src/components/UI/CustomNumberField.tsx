import { FormControl, Tooltip, TextField, InputAdornment } from '@mui/material';
import { CustomTextFieldType } from '../../types/customTextField';

const CustomNumberField = (props: CustomTextFieldType) => {
  const { variable, name, handleChange } = props;
  const { disabled, value, tooltip, unit, variableString, variableSubString } =
    variable;

  const onWheel = (e: any) => {
    e.target.blur();
  };

  const onBlur = (e: any) => {
    const newValue = parseFloat(e.target.value);
    if (variable.min !== undefined && newValue < variable.min) {
      e.target.value = variable.min;
    }
    if (variable.max !== undefined && newValue > variable.max) {
      e.target.value = variable.max;
    }
    if (handleChange) {
      handleChange(e);
    }
  };

  return (
    <FormControl fullWidth>
      <Tooltip title={tooltip} placement="right" arrow>
        <TextField
          label={
            <>
              {variableString}
              <sub>{variableSubString}</sub>
            </>
          }
          disabled={disabled}
          value={value}
          name={name}
          onChange={handleChange}
          onWheel={onWheel}
          onBlur={onBlur}
          InputProps={{
            type: 'number',
            inputProps: {
              min: variable.min,
              max: variable.max,
              step: variable.step,
            },
            endAdornment: (
              <InputAdornment position="end">{unit}</InputAdornment>
            ),
          }}
        />
      </Tooltip>
    </FormControl>
  );
};

export default CustomNumberField;
