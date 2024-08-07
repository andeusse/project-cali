import { Box, Button, Container, Tab } from '@mui/material';
import CustomTab from '../components/UI/CustomTab';
import { TabType } from '../types/tab';
import IframeFull from '../components/UI/IframeFull';
import Config from '../config/config';
import { TabContext, TabList, TabPanel } from '@mui/lab';
import { useState } from 'react';

type Props = {};

const ElectricalTabs = () => {
  const electricalTabs = [
    'Unifilar',
    'Eventos transitorios',
    'Totalizador',
    'Sistema PBM',
    'Analizador Biogás',
    'Planta de Biogás',
    'Tunel de viento - Potencia',
    'Ventilador sistema eolico',
    'Torre de enfriamiento',
    'Banco de trabajo turbinas',
    'Tablero Paneles',
    'Iluminación Biogás',
    'Video Wall Smart Grid',
    'Iluminación Fotovoltaico',
    'Video Controller Smart Grid',
    'Iluminación Smartgrid',
    'Mesa Biogás Fotovoltaico',
    'Nevera Biogás',
    'Mesón Sala Biogás',
    'Tunel de viento - control',
    'Modulo fotovoltaico eolico',
    'Modulo control turbinas',
  ];

  const [selectedTab, setSelectedTab] = useState<string>(electricalTabs[0]);

  const handleChange = (event: React.SyntheticEvent, newValue: string) => {
    setSelectedTab(newValue);
  };

  return (
    <Box sx={{ width: '100%', typography: 'body1' }}>
      <Button
        target="_blank"
        href={Config.getInstance().params.webServerDmg9000Url}
      >
        Web server DMG9000
      </Button>
      <TabContext value={selectedTab}>
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <TabList
            onChange={handleChange}
            aria-label="Monitoring tabs"
            variant="scrollable"
            allowScrollButtonsMobile
          >
            {electricalTabs.map((tab) => (
              <Tab key={tab} label={tab} value={tab} />
            ))}
          </TabList>
        </Box>
        {electricalTabs.map((tab, index) => (
          <TabPanel key={tab} value={tab}>
            <IframeFull
              url={Config.getInstance().params.electricalUrls[index]}
            ></IframeFull>
          </TabPanel>
        ))}
      </TabContext>
    </Box>
  );
};

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
      children: <ElectricalTabs></ElectricalTabs>,
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
