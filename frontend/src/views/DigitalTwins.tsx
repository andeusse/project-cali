import { Box, Container } from '@mui/material';
import CustomTab from '../components/UI/CustomTab';
import { TabType } from '../types/tab';
import Turbine from './digitalTwinsTabs/Turbine';
import Solar from './digitalTwinsTabs/Solar';
import Biogas from './digitalTwinsTabs/Biogas';
import CoolingTower from './digitalTwinsTabs/CoolingTower';

type Props = {};

const DigitalTwins = (props: Props) => {
  const tabs: TabType[] = [
    {
      title: 'Turbinas',
      children: <Turbine></Turbine>,
    },
    {
      title: 'Solar - Eólico',
      children: <Solar></Solar>,
    },
    {
      title: 'Planta de Biogás',
      children: <Biogas></Biogas>,
    },
    {
      title: 'Celda de Hidrógeno',
      children: <></>,
    },
    {
      title: 'Torre de enfriamiento',
      children: <CoolingTower></CoolingTower>,
    },
    {
      title: 'Potencial Bioquímico (Metano)',
      children: <></>,
    },
  ];

  return (
    <Container disableGutters maxWidth={false}>
      <Box display="flex" justifyContent="center" alignItems="center">
        <h1>Gemelos digitales</h1>
      </Box>
      <CustomTab tabs={tabs}></CustomTab>
    </Container>
  );
};

export default DigitalTwins;
