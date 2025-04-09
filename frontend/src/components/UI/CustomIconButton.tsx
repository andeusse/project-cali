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
  disabled?: boolean;
};

export const CustomIconButton = (props: Props) => {
  const {
    tooltip,
    color = 'info',
    icon,
    handleClick,
    disabled = false,
  } = props;

  return (
    <Tooltip title={tooltip} placement="top" arrow>
      <span>
        <IconButton
          color={color}
          size="large"
          onClick={handleClick}
          disabled={disabled}
        >
          {icon}
        </IconButton>
      </span>
    </Tooltip>
  );
};
