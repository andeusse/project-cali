import { Typography } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import ElectricBoltIcon from '@mui/icons-material/ElectricBolt';

type Props = {};

const Logo = (props: Props) => {
  return (
    <Typography
      variant="h6"
      noWrap
      component={RouterLink}
      to={`/`}
      sx={{
        mr: 2,
        display: { xs: 'none', md: 'flex' },
        fontFamily: 'monospace',
        fontWeight: 700,
        fontSize: '1rem',
        letterSpacing: '.3rem',
        color: 'inherit',
        textDecoration: 'none',
      }}
    >
      <ElectricBoltIcon sx={{ display: { xs: 'none', md: 'flex' }, mr: 1 }} />
      SMARTGRID
    </Typography>
  );
};

export default Logo;
