import { FormControl, Tooltip, TextField, InputAdornment } from '@mui/material';
import { inputType } from '../../types/models/common';

type Props = {
  variable: inputType;
  name?: string;
  min?: number;
  max?: number;
  handleChange?: (e: any) => void;
};

const CustomNumberField = (props: Props) => {
  const { variable, name, min, max, handleChange } = props;
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
            inputProps: { min: min, max: max },
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
