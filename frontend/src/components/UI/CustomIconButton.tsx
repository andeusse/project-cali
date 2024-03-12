import {
  IconButton,
  IconButtonPropsColorOverrides,
  Tooltip,
} from '@mui/material';
import { OverridableStringUnion } from '@mui/types';
import React from 'react';

type Props = {
  tooltip: string;
  color?:
    | OverridableStringUnion<
        | 'info'
        | 'inherit'
        | 'default'
        | 'primary'
        | 'secondary'
        | 'error'
        | 'success'
        | 'warning',
        IconButtonPropsColorOverrides
      >
    | undefined;
  icon: React.ReactNode;
  handleClick: () => void;
};

export const CustomIconButton = (props: Props) => {
  const { tooltip, color = 'info', icon, handleClick } = props;

  return (
    <Tooltip title={tooltip} placement="top" arrow>
      <IconButton color={color} size="large" onClick={handleClick}>
        {icon}
      </IconButton>
    </Tooltip>
  );
};
