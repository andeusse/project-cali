import { FormControl, Tooltip, TextField, InputAdornment } from '@mui/material';
import { CustomTextFieldType } from '../../types/customTextField';

const CustomStringField = (props: CustomTextFieldType) => {
  const { variable, name, handleChange, disabled: disabledProp } = props;
  const {
    disabled,
    stringValue,
    tooltip,
    unit,
    variableString,
    variableSubString,
  } = variable;

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
          value={stringValue}
          name={name}
          onChange={handleChange}
          InputProps={{
            endAdornment: (
              <InputAdornment position="end">{unit}</InputAdornment>
            ),
          }}
        />
      </Tooltip>
    </FormControl>
  );
};

export default CustomStringField;
