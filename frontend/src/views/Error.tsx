import { Box } from '@mui/material';
import HomeIcon from '@mui/icons-material/Home';
import LinkButton from '../components/UI/LinkButton';

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
        <LinkButton
          icon={<HomeIcon></HomeIcon>}
          sx={{ marginRight: 2, color: 'white' }}
          to={`/`}
          text={'Home'}
        ></LinkButton>
      </Box>
    </>
  );
};

export default Error;
