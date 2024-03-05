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
  const { variable, name, handleChange, offlineOperation } = props;

  return (
    <Grid container spacing={2}>
      <Grid item xs={7} md={7} xl={7}>
        <CustomNumberField {...props}></CustomNumberField>
      </Grid>
      <Grid item xs={5} md={5} xl={5} sx={{ marginTop: '10px' }}>
        <FormControlLabel
          control={
            <Switch
              checked={!variable.disabled}
              name="variableCustomize"
              disabled={!offlineOperation}
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
