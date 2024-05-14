import { FormControl, Tooltip, TextField, InputAdornment } from '@mui/material';
import { CustomTextFieldType } from '../../types/customTextField';

const CustomNumberField = (props: CustomTextFieldType) => {
  const {
    variable,
    name,
    handleChange,
    disabled: disabledProp,
    isInteger,
    disableKeyDown,
  } = props;
  const { disabled, value, tooltip, unit, variableString, variableSubString } =
    variable;

  const onWheel = (e: any) => {
    e.target.blur();
  };

  const onBlur = (e: any) => {
    if (e.target.value !== '') {
      let newValue = parseFloat(e.target.value);
      if (isInteger) {
        e.target.value = Math.round(newValue);
      }
      if (variable.min !== undefined && newValue < variable.min) {
        e.target.value = variable.min;
      }
      if (variable.max !== undefined && newValue > variable.max) {
        e.target.value = variable.max;
      }
    } else {
      e.target.value = variable.min;
    }
    if (handleChange) {
      handleChange(e);
    }
  };

  return (
    <FormControl fullWidth>
      <Tooltip
        title={`${tooltip}. ${
          variable.min !== undefined ? `Mínimo: ${variable.min}.` : ''
        } ${variable.max !== undefined ? `Máximo: ${variable.max}.` : ''}`}
        placement="right"
        arrow
      >
        <TextField
          label={
            <>
              {variableString}
              <sub>{variableSubString}</sub>
            </>
          }
          disabled={disabled || disabledProp}
          value={value}
          name={name}
          onChange={handleChange}
          onWheel={onWheel}
          onBlur={(event) => (!disableKeyDown ? onBlur(event) : undefined)}
          onKeyDown={(event) =>
            disableKeyDown ? event.preventDefault() : undefined
          }
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
