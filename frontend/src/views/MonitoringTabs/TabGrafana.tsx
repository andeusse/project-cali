import { TabType } from '../../types/tab';
import { Box } from '@mui/material';
import CustomTab from '../../components/UI/CustomTab';
import Config from '../../config/config';
import Iframe from 'react-iframe';
import IframeFull from '../../components/UI/IframeFull';

type Props = {};

const TabGrafana = (props: Props) => {
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
      title: 'Celda de Hidrógeno',
      children: (
        <IframeFull
          url={Config.getInstance().params.grafanaUrls[2]}
        ></IframeFull>
      ),
    },
    {
      title: 'Planta de Biogás',
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
      title: 'Túnel de viento',
      children: (
        <IframeFull
          url={Config.getInstance().params.grafanaUrls[5]}
        ></IframeFull>
      ),
    },
    {
      title: 'Potencial Bioquímico (Metano)',
      children: (
        <IframeFull
          url={Config.getInstance().params.grafanaUrls[6]}
        ></IframeFull>
      ),
    },
  ];

  return (
    <Box display="flex">
      <CustomTab tabs={tabs}></CustomTab>
    </Box>
  );
};

export default TabGrafana;
