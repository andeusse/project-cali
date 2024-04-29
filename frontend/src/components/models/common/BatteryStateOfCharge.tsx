import React from 'react';
import { useTheme } from '@mui/material';

type Props = {
  batteryStateOfCharge: number;
};

const BatteryStateOfCharge = (props: Props) => {
  const { batteryStateOfCharge } = props;
  const theme = useTheme();

  return (
    <svg
      version="1.1"
      id="Layer_1"
      xmlns="http://www.w3.org/2000/svg"
      x="0px"
      y="0px"
      width="512px"
      height="512px"
      viewBox="0 0 512 512"
    >
      <rect
        width="220"
        height={4 * batteryStateOfCharge}
        x="146"
        y={-4 * batteryStateOfCharge + 475}
        rx="20"
        ry="20"
        fill="green"
      />
      <path
        fill="none"
        stroke={theme.palette.text.primary}
        strokeWidth="15.5193"
        strokeMiterlimit="10"
        d="M365.772,449.932
 c0,17.158-13.909,31.067-31.067,31.067H177.295c-17.158,0-31.068-13.909-31.068-31.067V101.974c0-17.159,13.91-31.068,31.068-31.068
 h157.409c17.158,0,31.067,13.909,31.067,31.068V449.932z"
      />
      <rect
        x="206.117"
        y="30.999"
        width="99.767"
        height="15.52"
        fill={theme.palette.text.primary}
      />
    </svg>
  );
};

export default BatteryStateOfCharge;
