import { Box, Container } from '@mui/material';

import CustomTab from '../components/UI/CustomTab';
import { TabType } from '../types/tab';
import SmartHome from './scenariosTabs/SmartHome';
import SmartCity from './scenariosTabs/SmartCity';
import SmartFactory from './scenariosTabs/SmartFactory';

type Props = {};

const Scenarios = (props: Props) => {
  const tabs: TabType[] = [
    {
      title: 'Smart City',
      children: <SmartCity></SmartCity>,
    },
    {
      title: 'Smart Factory',
      children: <SmartFactory></SmartFactory>,
    },
    {
      title: 'Smart Home',
      children: <SmartHome></SmartHome>,
    },
  ];
  return (
    <Container disableGutters maxWidth={false}>
      <Box display="flex" justifyContent="center" alignItems="center">
        <h1>Escenarios</h1>
      </Box>
      <CustomTab tabs={tabs}></CustomTab>
    </Container>
  );
};

export default Scenarios;
