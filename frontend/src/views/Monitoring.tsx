import { Box, Container } from '@mui/material';
import CustomTab from '../components/UI/CustomTab';
import { TabType } from '../types/tab';
import TabGrafana from './MonitoringTabs/TabGrafana';
import TabRealTime from './MonitoringTabs/TabRealTime';

type Props = {};

const Monitoring = (props: Props) => {
  const tabs: TabType[] = [
    {
      title: 'Históricos - Grafana',
      children: <TabGrafana></TabGrafana>,
    },
    {
      title: 'Tiempo real - Node-RED',
      children: <TabRealTime></TabRealTime>,
    },
  ];
  return (
    <Container maxWidth="xl">
      <Box display="flex" justifyContent="center" alignItems="center">
        <h1>Monitoreo</h1>
      </Box>
      <CustomTab tabs={tabs}></CustomTab>
    </Container>
  );
};

export default Monitoring;
