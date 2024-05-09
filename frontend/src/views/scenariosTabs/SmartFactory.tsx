import {
  Grid,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Accordion,
  AccordionDetails,
  AccordionSummary,
  Typography,
  TextField,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import React, { useState } from 'react';
import CustomNumberField from '../../components/UI/CustomNumberField';
import { SMART_CITY, SmartCityParameters } from '../../types/models/smartCity';
import { getValueByKey } from '../../utils/getValueByKey';
import { setFormState } from '../../utils/setFormState';
import ErrorDialog from '../../components/UI/ErrorDialog';

import smartFactoryIllustration from '../../assets/illustrations/smartFactory.png';
import {
  ScenariosModesType,
  ScenariosStepUnitType,
  ScenariosStepUnitText,
} from '../../types/models/common';
import {
  SMART_FACTORY,
  SmartFactoryParameters,
} from '../../types/models/smartFactory';

type Props = {};

const SmartFactory = (props: Props) => {
  const [system, setSystem] = useState(SMART_FACTORY);
  const [isOpen, setIsOpen] = useState(false);
  const [isImageExpanded, setIsImageExpanded] = useState(true);
  const [isParametersExpanded, setIsParametersExpanded] = useState(true);

  const error = '';

  const handleChange = (e: any, variableName?: string) => {
    const newState = setFormState<SmartFactoryParameters>(
      e,
      system,
      variableName
    );
    if (newState) {
      setSystem(newState as SmartFactoryParameters);
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

export default SmartFactory;
