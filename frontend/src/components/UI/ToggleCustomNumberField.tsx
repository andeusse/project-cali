import React from 'react';
import { ToggleCustomTextFieldType } from '../../types/customTextField';
import { FormControlLabel, Grid, Switch } from '@mui/material';
import CustomNumberField from './CustomNumberField';

const ToggleCustomNumberField = (props: ToggleCustomTextFieldType) => {
  const {
    variable,
    name,
    handleChange,
    falseText = 'Auto',
    trueText = 'Manual',
    disabled,
  } = props;

  const { disabled: _, ...otherProps } = props;

  return (
    <Grid container spacing={2}>
      <Grid item xs={7} md={7} xl={7}>
        <CustomNumberField {...otherProps}></CustomNumberField>
      </Grid>
      <Grid item xs={5} md={5} xl={5} sx={{ alignContent: 'center' }}>
        <FormControlLabel
          control={
            <Switch
              checked={!variable.disabled}
              name="variableCustomize"
              disabled={disabled}
              onChange={(e) => {
                if (handleChange) {
                  handleChange(e, name);
                }
              }}
              color="default"
            />
          }
          label={variable.disabled ? falseText : trueText}
        />
      </Grid>
    </Grid>
  );
};

export default ToggleCustomNumberField;
