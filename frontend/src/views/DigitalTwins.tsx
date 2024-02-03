import { Box, Container } from '@mui/material';
import CustomTab from '../components/UI/CustomTab';
import { TabType } from '../types/tab';

type Props = {};

const DigitalTwins = (props: Props) => {
  const tabs: TabType[] = [
    {
      title: 'Gen. Solar',
      children: <></>,
    },
    {
      title: 'Gen. Eólico',
      children: <></>,
    },
    {
      title: 'Gen. Hidráulico',
      children: <></>,
    },
    {
      title: 'Gen. Biogás',
      children: <></>,
    },
    {
      title: 'Baterías',
      children: <></>,
    },
  ];
  return (
    <Container maxWidth="xl">
      <Box display="flex" justifyContent="center" alignItems="center">
        <h1>DigitalTwins</h1>
      </Box>
      <CustomTab tabs={tabs}></CustomTab>
    </Container>
  );
};

export default DigitalTwins;
