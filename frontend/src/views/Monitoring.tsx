import { Box, Container } from '@mui/material';
import CustomTab from '../components/UI/CustomTab';
import { TabType } from '../types/tab';
import IframeFull from '../components/UI/IframeFull';
import Config from '../config/config';

type Props = {};

const Monitoring = (props: Props) => {
  const tabs: TabType[] = [
    {
      title: 'Turbinas',
      children: (
        <IframeFull
          url={Config.getInstance().params.grafanaUrls[0]}
        ></IframeFull>
      ),
    },
    {
      title: 'Solar - Eólico',
      children: (
        <IframeFull
          url={Config.getInstance().params.grafanaUrls[1]}
        ></IframeFull>
      ),
    },
    {
      title: 'Planta de Biogás',
      children: (
        <IframeFull
          url={Config.getInstance().params.grafanaUrls[2]}
        ></IframeFull>
      ),
    },
    {
      title: 'Celda de Hidrógeno',
      children: (
        <IframeFull
          url={Config.getInstance().params.grafanaUrls[3]}
        ></IframeFull>
      ),
    },
    {
      title: 'Torre de refrigeración',
      children: (
        <IframeFull
          url={Config.getInstance().params.grafanaUrls[4]}
        ></IframeFull>
      ),
    },
    {
      title: 'Potencial Bioquímico (Metano)',
      children: (
        <IframeFull
          url={Config.getInstance().params.grafanaUrls[5]}
        ></IframeFull>
      ),
    },
    {
      title: 'Tablero Eléctrico',
      children: (
        <IframeFull
          url={Config.getInstance().params.grafanaUrls[6]}
        ></IframeFull>
      ),
    },
  ];

  return (
    <Container disableGutters maxWidth={false}>
      <Box display="flex" justifyContent="center" alignItems="center">
        <h1>Monitoreo</h1>
      </Box>
      <CustomTab tabs={tabs}></CustomTab>
    </Container>
  );
};

export default Monitoring;
