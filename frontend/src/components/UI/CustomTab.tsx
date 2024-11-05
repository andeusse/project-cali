import { TabContext, TabList, TabPanel } from '@mui/lab';
import { Box, Tab } from '@mui/material';
import { useState } from 'react';
import { TabType } from '../../types/tab';

type Props = {
  tabs: TabType[];
};

const CustomTab = (props: Props) => {
  const { tabs } = props;

  const [selectedTab, setSelectedTab] = useState<string>(tabs[0].title);

  const handleChange = (event: React.SyntheticEvent, newValue: string) => {
    setSelectedTab(newValue);
  };

  return (
    <Box sx={{ width: '100%', typography: 'body1' }}>
      <TabContext value={selectedTab}>
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <TabList
            onChange={handleChange}
            aria-label="Monitoring tabs"
            variant="scrollable"
            allowScrollButtonsMobile
          >
            {tabs.map((tab) => (
              <Tab key={tab.title} label={tab.title} value={tab.title} />
            ))}
          </TabList>
        </Box>
        {tabs.map((tab) => (
          <TabPanel key={tab.title} value={tab.title}>
            {tab.children}
          </TabPanel>
        ))}
      </TabContext>
    </Box>
  );
};

export default CustomTab;
