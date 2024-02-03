import { Box, Container } from '@mui/material';
import MonitorIcon from '@mui/icons-material/Monitor';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import StackedLineChartIcon from '@mui/icons-material/StackedLineChart';

import LinkButton from '../components/UI/LinkButton';

type Props = {};

const Home = (props: Props) => {
  const style = {
    marginRight: 2,
    mb: 2,
  };

  return (
    <Container maxWidth="xl">
      <Box display="flex" justifyContent="center" alignItems="center">
        <h1>Home</h1>
      </Box>
      <Box display="flex" justifyContent="start" alignItems="start">
        <p>Add some text about the project ...</p>
      </Box>
      <Box
        sx={{ display: { xs: 'grid', md: 'flex' } }}
        justifyContent="center"
        alignItems="center"
      >
        <LinkButton
          startIcon={<MonitorIcon></MonitorIcon>}
          sx={style}
          to={`monitoring`}
          variant="contained"
          color="inherit"
        >
          Monitoring
        </LinkButton>
        <LinkButton
          startIcon={<ContentCopyIcon></ContentCopyIcon>}
          sx={style}
          to={`digitaltwins`}
          variant="contained"
          color="inherit"
        >
          Digital Twins
        </LinkButton>
        <LinkButton
          startIcon={<StackedLineChartIcon></StackedLineChartIcon>}
          sx={style}
          to={`scenarios`}
          variant="contained"
          color="inherit"
        >
          Scenarios
        </LinkButton>
      </Box>
    </Container>
  );
};

export default Home;
