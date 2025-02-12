import { FormControl, Tooltip, TextField, InputAdornment } from '@mui/material';
import { CustomTextFieldType } from '../../types/customTextField';
import { useCallback, useEffect, useState } from 'react';

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

  const [numberFieldValue, setNumberFieldValue] = useState(value.toString());

  const useDebounce = (cb: any, delay: number) => {
    const [debounceValue, setDebounceValue] = useState(cb);
    useEffect(() => {
      const handler = setTimeout(() => {
        setDebounceValue(cb);
      }, delay);
      return () => {
        clearTimeout(handler);
      };
    }, [cb, delay]);
    return debounceValue;
  };

  const debounceValue = useDebounce(numberFieldValue, DEBOUNCE_TIME);

  const handleVariableChange = useCallback(() => {
    if (name !== undefined) {
      var variableTemp = {
        target: {
          type: 'text',
          name: name,
          value: 0,
        },
      };
      if (debounceValue !== '') {
        let newValue = parseFloat(debounceValue);
        variableTemp.target.value = newValue;
        if (isInteger) {
          variableTemp.target.value = Math.round(newValue);
        }
        if (variable.min !== undefined && newValue < variable.min) {
          variableTemp.target.value = variable.min;
        }
        if (variable.max !== undefined && newValue > variable.max) {
          variableTemp.target.value = variable.max;
        }
        if (
          name
            .toLocaleLowerCase()
            .includes('PowerFactor'.toLocaleLowerCase()) &&
          newValue === 0
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
        setNumberFieldValue(variableTemp.target.value.toString());
        handleChange(variableTemp);
      }
    }
  }, [debounceValue, isInteger, name, variable.max, variable.min]);

  useEffect(() => {
    setNumberFieldValue(value.toString());
  }, [value]);

  useEffect(() => {
    handleVariableChange();
  }, [handleVariableChange]);

  const handleValueChange = (e: any) => {
    setNumberFieldValue(e.target.value);
  };

  const onWheel = (e: any) => {
    e.target.blur();
  };

  const onBlur = (e: any) => {};

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
          value={numberFieldValue}
          name={name}
          onChange={handleValueChange}
          onWheel={onWheel}
          onBlur={(event) => (!disableKeyDown ? onBlur(event) : undefined)}
          onKeyDown={(event) =>
            disableKeyDown ? event.preventDefault() : undefined
          }
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
