import { FormControl, Tooltip, TextField, InputAdornment } from '@mui/material';
import { CustomTextFieldType } from '../../types/customTextField';
import { useCallback, useEffect, useRef, useState } from 'react';
import Constants from '../../config/constants';

const CustomNumberField = (props: CustomTextFieldType) => {
  const {
    variable,
    name,
    handleChange,
    disabled: disabledProp,
    isInteger,
    disableKeyDown,
  } = props;
  const { disabled, value, tooltip, unit, variableString, variableSubString } =
    variable;

  const [inputValue, setInputValue] = useState(value.toString());

  const timeoutId = useRef<NodeJS.Timeout | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(event.target.value);
    resetInactivityTimer();
  };

  const setValue = useCallback(
    (value: string) => {
      const numValue = Number(value);
      if (name !== undefined) {
        var variableTemp = {
          target: {
            type: 'text',
            name: name,
            value: 0,
          },
        };
        if (value !== '') {
          variableTemp.target.value = numValue;
          if (isInteger) {
            variableTemp.target.value = Math.round(numValue);
          }
          if (variable.min !== undefined && numValue < variable.min) {
            variableTemp.target.value = variable.min;
          }
          if (variable.max !== undefined && numValue > variable.max) {
            variableTemp.target.value = variable.max;
          }
          if (
            name
              .toLocaleLowerCase()
              .includes('PowerFactor'.toLocaleLowerCase()) &&
            numValue === 0
          ) {
            variableTemp.target.value = 1;
          }
        } else {
          if (variable.min !== undefined) {
            variableTemp.target.value = variable.min;
          } else {
            variableTemp.target.value = 0;
          }
        }
        if (handleChange !== undefined) {
          handleChange(variableTemp);
          setInputValue(variableTemp.target.value.toString());
        }
      }
    },
    [handleChange, isInteger, name, variable.max, variable.min]
  );

  useEffect(() => {
    return () => {
      if (timeoutId.current) {
        clearTimeout(timeoutId.current);
      }
    };
  }, []);

  useEffect(() => {
    setInputValue(value.toString());
  }, [value]);

  const handleFocus = () => {
    resetInactivityTimer();
  };

  const handleWheel = (e: any) => {
    e.target.blur();
  };

  const handleBlur = () => {
    setValue(inputValue);
    clearTimeout(timeoutId.current as NodeJS.Timeout);
  };

  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (disableKeyDown && event.key !== 'Enter') {
      event.preventDefault();
      return;
    }
    if (event.key === 'Enter') {
      event.preventDefault();
      setValue(inputValue);
    }
  };

  const resetInactivityTimer = () => {
    if (timeoutId.current) {
      clearTimeout(timeoutId.current);
    }
    timeoutId.current = setTimeout(() => {
      if (inputRef.current) {
        inputRef.current.blur();
      }
    }, Constants.INACTIVITY_TIMEOUT);
  };

  return (
    <FormControl fullWidth>
      <Tooltip
        title={`${tooltip} ${
          variable.min !== undefined ? `Mínimo: ${variable.min}` : ''
        } ${variable.max !== undefined ? `Máximo: ${variable.max}` : ''}`}
        placement="right"
        arrow
      >
        <TextField
          label={
            <>
              {variableString}
              <sub>{variableSubString}</sub>
            </>
          }
          disabled={disabled || disabledProp}
          value={inputValue}
          name={name}
          onFocus={handleFocus}
          onChange={handleInputChange}
          onWheel={handleWheel}
          onBlur={handleBlur}
          onKeyDown={handleKeyDown}
          inputRef={inputRef}
          InputProps={{
            type: 'number',
            inputProps: {
              min: variable.min,
              max: variable.max,
              step: variable.step,
            },
            endAdornment: (
              <InputAdornment position="end">{unit}</InputAdornment>
            ),
          }}
        />
      </Tooltip>
    </FormControl>
  );
};

export default CustomNumberField;
