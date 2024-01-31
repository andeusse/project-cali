import { TabContext, TabList, TabPanel } from '@mui/lab';
import { Box, Tab } from '@mui/material';
import { useState } from 'react';
import { TabType } from '../../types/tab';

type Props = {
  tabs: TabType[];
};

const CustomTab = (props: Props) => {
  const { tabs } = props;

  const [value, setValue] = useState('1');

  const handleChange = (event: React.SyntheticEvent, newValue: string) => {
    setValue(newValue);
  };

  return (
    <Box sx={{ width: '100%', typography: 'body1' }}>
      <TabContext value={value}>
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <TabList
            onChange={handleChange}
            aria-label="Monitoring tabs"
            variant="scrollable"
            allowScrollButtonsMobile
          >
            {tabs.map((tab, index) => {
              return (
                <Tab key={tab.title} label={tab.title} value={`${index + 1}`} />
              );
            })}
          </TabList>
        </Box>
        {tabs.map((tab, index) => {
          return (
            <TabPanel key={tab.title} value={`${index + 1}`}>
              {tab.children}
            </TabPanel>
          );
        })}
      </TabContext>
    </Box>
  );
};

export default CustomTab;
