import { FormControl, Tooltip, TextField, InputAdornment } from '@mui/material';
import { CustomTextFieldType } from '../../types/customTextField';
import { useCallback, useEffect, useState } from 'react';
import { debounce } from 'lodash';

const DEBOUNCE_TIME = 2000;

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
  const [, setDebouncedValue] = useState('');

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(event.target.value);
    debouncedSetValue(event.target.value);
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
          setDebouncedValue(value);
          handleChange(variableTemp);
          setInputValue(variableTemp.target.value.toString());
        }
      }
    },
    [handleChange, isInteger, name, variable.max, variable.min]
  );

  // eslint-disable-next-line react-hooks/exhaustive-deps
  const debouncedSetValue = useCallback(
    debounce((value: string) => {
      setValue(value);
    }, DEBOUNCE_TIME),
    []
  );

  useEffect(() => {
    setInputValue(value.toString());
  }, [value]);

  const onWheel = (e: any) => {
    e.target.blur();
  };

  const onBlur = () => {
    setValue(inputValue);
  };

  const onKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (disableKeyDown && event.key !== 'Enter') {
      event.preventDefault();
      return;
    }
    if (event.key === 'Enter') {
      event.preventDefault();
      setValue(inputValue);
    }
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
          onChange={handleInputChange}
          onWheel={onWheel}
          onBlur={onBlur}
          onKeyDown={onKeyDown}
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
