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
          icon={<MonitorIcon></MonitorIcon>}
          sx={style}
          to={`monitoring`}
          text={'Monitoring'}
          variant="contained"
          color="inherit"
        ></LinkButton>
        <LinkButton
          icon={<ContentCopyIcon></ContentCopyIcon>}
          sx={style}
          to={`digitaltwins`}
          text={'Digital Twins'}
          variant="contained"
          color="inherit"
        ></LinkButton>
        <LinkButton
          icon={<StackedLineChartIcon></StackedLineChartIcon>}
          sx={style}
          to={`scenarios`}
          text={'Scenarios'}
          variant="contained"
          color="inherit"
        ></LinkButton>
      </Box>
    </Container>
  );
};

export default Home;
