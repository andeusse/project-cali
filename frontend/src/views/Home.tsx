import { Box, Container, Grid } from '@mui/material';
import MonitorIcon from '@mui/icons-material/Monitor';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import StackedLineChartIcon from '@mui/icons-material/StackedLineChart';

import LinkButton from '../components/UI/LinkButton';
import { Link } from 'react-router-dom';

import homeMonitoring from '../assets/home/homeMonitoring.png';
import homeDigitalTwins from '../assets/home/homeDigitalTwins.png';
import homeScenario from '../assets/home/homeScenario.png';

import logoDida from '../assets/home/logoDida.png';
import logoUSC from '../assets/home/logoUSC.png';

type Props = {};

const Home = (props: Props) => {
  const style = {
    marginRight: 2,
    mb: 2,
  };

  return (
    <Container maxWidth={'xl'}>
      <Box display="flex" justifyContent="center" alignItems="center">
        <h1>Plataforma Smartgrid - Laboratorio de Energías</h1>
      </Box>
      <Box display="flex" justifyContent="center" alignItems="center">
        <h1>Universidad Santiago de Cali</h1>
      </Box>
      <Grid container spacing={3} marginTop = {5}>
        <Grid item xs={12} md={4} xl={4}>
          <Link to={`/monitoring`}>
            <img
              style={{ width: '100%' }}
              src={homeMonitoring}
              alt="Monitoring"
            ></img>
          </Link>
          <Box
            sx={{ display: { xs: 'grid', md: 'flex' } }}
            justifyContent="center"
            alignItems="center"
          >
          </Box>
        </Grid>
        <Grid item xs={12} md={4} xl={4}>
          <Link to={`/digitaltwins`}>
            <img
              style={{ width: '100%' }}
              src={homeDigitalTwins}
              alt="DigitalTwins"
            ></img>
          </Link>
          <Box
            sx={{ display: { xs: 'grid', md: 'flex' } }}
            justifyContent="center"
            alignItems="center"
          >
          </Box>
        </Grid>
        <Grid item xs={12} md={4} xl={4}>
          <Link to={`/scenarios`}>
            <img
              style={{ width: '100%' }}
              src={homeScenario}
              alt="Scenarios"
            ></img>
          </Link>
          <Box
            sx={{ display: { xs: 'grid', md: 'flex' } }}
            justifyContent="center"
            alignItems="center"
          >
          </Box>
        </Grid>
        <Grid item xs={12} md={6} xl={6} marginTop={2.5}>
          <Box
            sx={{ display: { xs: 'grid', md: 'flex' } }}
            justifyContent="center"
            alignItems="center"
          >
            <img style={{ width: '25%' }} src={logoDida} alt="logoDida"></img>
          </Box>
        </Grid>
        <Grid item xs={12} md={6} xl={6} marginTop={2.5}>
          <Box
            sx={{ display: { xs: 'grid', md: 'flex' } }}
            justifyContent="center"
            alignItems="center"
          >
            <img style={{ width: '25%' }} src={logoUSC} alt="logoUSC"></img>
          </Box>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Home;
