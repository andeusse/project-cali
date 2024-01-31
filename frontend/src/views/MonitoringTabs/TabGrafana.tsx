import React from 'react';
import { TabType } from '../../types/tab';
import { Box } from '@mui/material';
import CustomTab from '../../components/UI/CustomTab';
import Config from '../../config/config';
import Iframe from 'react-iframe';

type Props = {};

const TabGrafana = (props: Props) => {
  const tabs: TabType[] = [
    {
      title: 'Turbinas',
      children: (
        <Iframe
          url={Config.getInstance().params.grafanaUrls[0]}
          styles={{ width: '100%', height: '550px' }}
        ></Iframe>
      ),
    },
    {
      title: 'Solar - Eólico',
      children: (
        <Iframe
          url={Config.getInstance().params.grafanaUrls[1]}
          styles={{ width: '100%', height: '550px' }}
        ></Iframe>
      ),
    },
    {
      title: 'Celda de Hidrógeno',
      children: (
        <Iframe
          url={Config.getInstance().params.grafanaUrls[2]}
          styles={{ width: '100%', height: '550px' }}
        ></Iframe>
      ),
    },
    {
      title: 'Planta de Biogás',
      children: (
        <Iframe
          url={Config.getInstance().params.grafanaUrls[3]}
          styles={{ width: '100%', height: '550px' }}
        ></Iframe>
      ),
    },
    {
      title: 'Torre de refrigeración',
      children: (
        <Iframe
          url={Config.getInstance().params.grafanaUrls[4]}
          styles={{ width: '100%', height: '550px' }}
        ></Iframe>
      ),
    },
    {
      title: 'Túnel de viento',
      children: (
        <Iframe
          url={Config.getInstance().params.grafanaUrls[5]}
          styles={{ width: '100%', height: '550px' }}
        ></Iframe>
      ),
    },
    {
      title: 'Potencial Bioquímico (Metano)',
      children: (
        <Iframe
          url={Config.getInstance().params.grafanaUrls[6]}
          styles={{ width: '100%', height: '550px' }}
        ></Iframe>
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
