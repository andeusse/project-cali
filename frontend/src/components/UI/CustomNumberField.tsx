import { FormControl, Tooltip, TextField, InputAdornment } from '@mui/material';
import { CustomTextFieldType } from '../../types/customTextField';

const CustomNumberField = (props: CustomTextFieldType) => {
  const { variable, name, min, max, step, handleChange } = props;
  const { disabled, value, tooltip, unit, variableName, subIndex } = variable;

  return (
    <FormControl fullWidth>
      <Tooltip title={tooltip} placement="right" arrow>
        <TextField
          label={
            <>
              {variableName}
              <sub>{subIndex}</sub>
            </>
          }
          disabled={disabled}
          value={value}
          name={name}
          onChange={handleChange}
          InputProps={{
            type: 'number',
            inputProps: { min: min, max: max, step: step },
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
