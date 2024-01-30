import { Box, Button } from '@mui/material';
import { Link } from 'react-router-dom';
import { Link as LinkBase } from '@mui/material';
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
        <LinkBase
          component={Link}
          to={'/'}
          style={{
            textDecoration: 'none',
          }}
        >
          <Button startIcon={<HomeIcon></HomeIcon>}>Go home</Button>
        </LinkBase>
      </Box>
    </>
  );
};

export default Error;
