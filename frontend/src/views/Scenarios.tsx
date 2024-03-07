import { Box, Container } from '@mui/material';

import CustomTab from '../components/UI/CustomTab';
import { TabType } from '../types/tab';
import SmartHome from './scenariosTabs/SmartHome';

type Props = {};

const Scenarios = (props: Props) => {
  const tabs: TabType[] = [
    {
      title: 'Smart Home',
      children: <SmartHome></SmartHome>,
    },
    {
      title: 'Smart Factory',
      children: <></>,
    },
    {
      title: 'Smart City',
      children: <></>,
    },
  ];
  return (
    <Container maxWidth="xl">
      <Box display="flex" justifyContent="center" alignItems="center">
        <h1>Escenarios</h1>
      </Box>
      <CustomTab tabs={tabs}></CustomTab>
    </Container>
  );
};

export default Scenarios;
