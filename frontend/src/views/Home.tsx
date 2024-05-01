import { Box, Container, Grid } from '@mui/material';
import MonitorIcon from '@mui/icons-material/Monitor';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import StackedLineChartIcon from '@mui/icons-material/StackedLineChart';

import LinkButton from '../components/UI/LinkButton';
import { Link } from 'react-router-dom';

import homeMonitoring from '../assets/home/homeMonitoring.jpg';
import homeDigitalTwins from '../assets/home/homeDigitalTwins.jpg';
import homeScenario from '../assets/home/homeScenario.jpg';

type Props = {};

const Home = (props: Props) => {
  const style = {
    marginRight: 2,
    mb: 2,
  };

  return (
    <Container maxWidth={'xl'}>
      <Box display="flex" justifyContent="center" alignItems="center">
        <h1>Home</h1>
      </Box>
      <Box display="flex" justifyContent="start" alignItems="start">
        <p>Add some text about the project ...</p>
      </Box>
      <Grid container spacing={2}>
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
            <LinkButton
              startIcon={<MonitorIcon></MonitorIcon>}
              sx={style}
              to={`/monitoring`}
              variant="contained"
              color="inherit"
            >
              Monitoreo
            </LinkButton>
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
            <LinkButton
              startIcon={<ContentCopyIcon></ContentCopyIcon>}
              sx={style}
              to={`/digitaltwins`}
              variant="contained"
              color="inherit"
            >
              Gemelos digitales
            </LinkButton>
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
            <LinkButton
              startIcon={<StackedLineChartIcon></StackedLineChartIcon>}
              sx={style}
              to={`/scenarios`}
              variant="contained"
              color="inherit"
            >
              Escenarios
            </LinkButton>
          </Box>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Home;
