import {
  Grid,
  FormControl,
  Tooltip,
  TextField,
  InputAdornment,
} from '@mui/material';
import { useState } from 'react';

type Props = {
  tooltip: string;
  variableName: string;
  disabled: boolean;
  initialValue: number;
  unit: string;
};

const CustomTextField = (props: Props) => {
  const {
    tooltip,
    variableName,
    disabled: enabled,
    initialValue,
    unit,
  } = props;
  const [value, setValue] = useState<number>(initialValue);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setValue(parseFloat(e.target.value));
  };

  return (
    <Grid item xs={6} md={6} xl={6}>
      <FormControl fullWidth>
        <Tooltip title={tooltip} placement="right" arrow>
          <TextField
            label={variableName}
            disabled={enabled}
            value={value}
            onChange={handleChange}
            InputProps={{
              type: 'number',
              endAdornment: (
                <InputAdornment position="end">{unit}</InputAdornment>
              ),
            }}
          />
        </Tooltip>
      </FormControl>
    </Grid>
  );
};

export default CustomTextField;
