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
      <Grid item xs={10} md={10} xl={10}>
        <CustomNumberField {...props}></CustomNumberField>
      </Grid>
      <Grid item xs={2} md={2} xl={2}>
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
              sx={{ marginTop: '10px' }}
            />
          }
          label=""
        />
      </Grid>
    </Grid>
  );
};

export default ToggleCustomNumberField;
