import React from 'react';
import { BarChart } from '@mui/x-charts/BarChart';
import { Box } from '@mui/material';

type Props = {};

const TabRealTime = (props: Props) => {
  return (
    <Box display="flex">
      <BarChart
        xAxis={[{ scaleType: 'band', data: ['group A', 'group B', 'group C'] }]}
        series={[{ data: [4, 3, 5] }, { data: [1, 6, 3] }, { data: [2, 5, 6] }]}
        sx={{ width: '100%' }}
        height={550}
      />
    </Box>
  );
};

export default TabRealTime;
