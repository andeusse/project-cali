import { Button, SxProps, Theme } from '@mui/material';
import { FunctionComponent } from 'react';
import { Link as RouterLink } from 'react-router-dom';

type Props = {
  icon?: React.ReactNode;
  sx: SxProps<Theme> | undefined;
  to: string;
  text: string;
  variant?: 'text' | 'contained' | 'outlined' | undefined;
  color?:
    | 'success'
    | 'inherit'
    | 'primary'
    | 'secondary'
    | 'error'
    | 'info'
    | 'warning'
    | undefined;
};

const LinkButton: FunctionComponent<Props> = (props) => {
  const { icon, sx, to, text, variant, color } = props;
  return (
    <Button
      startIcon={icon}
      sx={sx}
      component={RouterLink}
      to={to}
      variant={variant}
      color={color}
    >
      {text}
    </Button>
  );
};

LinkButton.defaultProps = {
  variant: 'text',
  color: 'primary',
};

export default LinkButton;
