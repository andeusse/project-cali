import { Grid } from '@mui/material';
import React from 'react';
import { SmartSystemOutput } from '../../../types/scenarios/common';

type Props = {
  data: SmartSystemOutput;
};

const ResultTab = (props: Props) => {
  const { data } = props;
  return (
    <Grid container spacing={2}>
      Resultados
      <Grid item xs={12} md={12} xl={12}></Grid>
    </Grid>
  );
};

export default ResultTab;
