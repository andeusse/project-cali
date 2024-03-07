import { Container, Alert, Box, Grid } from '@mui/material';
import React, { useState } from 'react';
import InputParams from '../../components/scenarios/smartHome/InputParams';
import { SMART_CITY, SmartCityParameters } from '../../types/models/smartCity';
import { setFormState } from '../../utils/setFormState';

type Props = {};

const SmartHome = (props: Props) => {
  const [smartHome, setSmartHome] = useState(SMART_CITY);
  const [error, setError] = useState('');

  const handleChange = (e: any, variableName?: string) => {
    const newState = setFormState<SmartCityParameters>(
      e,
      smartHome,
      variableName
    );
    if (newState) {
      setSmartHome(newState);
    }
  };

  return (
    <Container maxWidth="xl">
      {error !== '' && (
        <Alert severity="error" variant="filled">
          {error}
        </Alert>
      )}
      <Box display="flex" justifyContent="center" alignItems="center">
        <h2>Parámetros del sistema</h2>
      </Box>
      <Grid container spacing={2}>
        <InputParams
          smartHome={smartHome}
          handleChange={handleChange}
        ></InputParams>
      </Grid>
    </Container>
  );
};

export default SmartHome;
