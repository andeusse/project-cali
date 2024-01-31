import { Box, Container } from '@mui/material';
import React from 'react';

type Props = {};

const AboutUs = (props: Props) => {
  return (
    <Container maxWidth="xl">
      <Box display="flex" justifyContent="center" alignItems="center">
        <h1>About Us</h1>
      </Box>
    </Container>
  );
};

export default AboutUs;
