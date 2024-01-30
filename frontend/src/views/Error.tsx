import { Box, Button } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import HomeIcon from '@mui/icons-material/Home';

const Error = () => {
  return (
    <>
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        marginTop={'50px'}
      >
        <img
          src="https://64.media.tumblr.com/tumblr_lz2ufhclZj1r4mh0bo1_r1_400.gifv"
          alt="Not Found"
        ></img>
      </Box>
      <Box display="flex" justifyContent="center" alignItems="center">
        <Button
          startIcon={<HomeIcon></HomeIcon>}
          sx={{ marginRight: 2, color: 'white' }}
          component={RouterLink}
          to={`/`}
        >
          Home
        </Button>
      </Box>
    </>
  );
};

export default Error;
