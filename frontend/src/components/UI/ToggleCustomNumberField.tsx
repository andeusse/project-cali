import React from 'react';
import {
  CustomTextFieldType,
  ToggleCustomTextFieldType,
} from '../../types/customTextField';
import { FormControlLabel, Grid, Switch } from '@mui/material';
import CustomNumberField from './CustomNumberField';

const ToggleCustomNumberField = (
  props: CustomTextFieldType & ToggleCustomTextFieldType
) => {
  const { variable, name, handleChange } = props;

  return (
    <Grid container spacing={2}>
      <Grid item xs={8} md={10} xl={10}>
        <CustomNumberField {...props}></CustomNumberField>
      </Grid>
      <Grid item xs={4} md={2} xl={2} sx={{ marginTop: '10px' }}>
        <FormControlLabel
          control={
            <Switch
              checked={!variable.disabled}
              name="variableCustomize"
              onChange={(e) => {
                if (handleChange) {
                  handleChange(e, name);
                }
              }}
              color="default"
            />
          }
          label="Manual"
        />
      </Grid>
    </Grid>
  );
};

export default ToggleCustomNumberField;
