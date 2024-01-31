import { Button, SxProps, Theme } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';

type Props = {
  icon: React.ReactNode | undefined;
  sx: SxProps<Theme> | undefined;
  to: string;
  text: string;
};

const LinkButton = (props: Props) => {
  const { icon, sx, to, text } = props;
  return (
    <Button startIcon={icon} sx={sx} component={RouterLink} to={to}>
      {text}
    </Button>
  );
};

export default LinkButton;
