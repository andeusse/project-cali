import {
  Accordion,
  AccordionDetails,
  AccordionSummary,
  FormControl,
  Grid,
  InputLabel,
  MenuItem,
  Select,
  TextField,
  Typography,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import React, { useState } from 'react';
import {
  SMART_CITY,
  SmartCityParameters,
} from '../../types/scenarios/smartCity';
import { setFormState } from '../../utils/setFormState';
import CustomNumberField from '../../components/UI/CustomNumberField';
import { getValueByKey } from '../../utils/getValueByKey';
import ErrorDialog from '../../components/UI/ErrorDialog';

import smartHomeIllustration from '../../assets/illustrations/smartHome.png';

type Props = {};

const SmartHome = (props: Props) => {
  const [system, setSystem] = useState(SMART_CITY);
  const [isOpen, setIsOpen] = useState(false);
  const [isImageExpanded, setIsImageExpanded] = useState(true);
  const [isParametersExpanded, setIsParametersExpanded] = useState(true);

  const error = '';

  const handleChange = (e: any, variableName?: string) => {
    const newState = setFormState<SmartCityParameters>(e, system, variableName);
    if (newState) {
      setSystem(newState as SmartCityParameters);
    }
  };

  return (
    <>
      <ErrorDialog
        isOpen={isOpen}
        setIsOpen={setIsOpen}
        error={error}
      ></ErrorDialog>
      <Grid container spacing={2}></Grid>
    </>
  );
};

export default SmartHome;
