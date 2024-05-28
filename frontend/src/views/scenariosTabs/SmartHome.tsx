import {
  Grid,
  Accordion,
  AccordionSummary,
  Typography,
  AccordionDetails,
} from '@mui/material';
import { useState } from 'react';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

import illustration from '../../assets/illustrations/smartHome.png';

const SmartHome = () => {
  const [isImageExpanded, setIsImageExpanded] = useState(true);

  return (
    <Grid container spacing={2}>
      <Grid item xs={12} md={12} xl={12}>
        <Accordion
          expanded={isImageExpanded}
          onChange={() => setIsImageExpanded(!isImageExpanded)}
        >
          <AccordionSummary
            expandIcon={<ExpandMoreIcon />}
            aria-controls="panel1-content"
            id="panel1-header"
            sx={{ margin: 0 }}
          >
            <Typography variant="h4">Sistema</Typography>
          </AccordionSummary>
          <AccordionDetails>
            <img
              style={{
                height: '500px',
                display: 'block',
                marginLeft: 'auto',
                marginRight: 'auto',
              }}
              src={illustration}
              alt="smartCityIllustration"
            ></img>
          </AccordionDetails>
        </Accordion>
      </Grid>
    </Grid>
  );
};

export default SmartHome;
