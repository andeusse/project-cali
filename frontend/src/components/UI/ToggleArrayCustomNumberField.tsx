import { ToggleArrayCustomTextFieldType } from '../../types/customTextField';
import { FormControlLabel, Grid, Switch } from '@mui/material';
import CustomNumberField from './CustomNumberField';

const ToggleArrayCustomNumberField = (
  props: ToggleArrayCustomTextFieldType
) => {
  const {
    variable,
    name,
    handleChange,
    falseText = 'Auto',
    trueText = 'Manual',
    disabled,
    variableName,
    arrayDisabled,
    showToggle = true,
    steps,
  } = props;

  const { disabled: _, arrayDisabled: _0, ...otherProps } = props;

  return (
    <Grid container spacing={2}>
      {'arrayEnabled' in variable && !variable.arrayEnabled && (
        <>
          <Grid item xs={12} md={7} xl={7}>
            <CustomNumberField {...otherProps}></CustomNumberField>
          </Grid>
          {showToggle && (
            <Grid item xs={6} md={5} xl={5} sx={{ alignContent: 'center' }}>
              <FormControlLabel
                control={
                  <Switch
                    checked={!variable.disabled}
                    name="variableCustomize"
                    disabled={disabled}
                    onChange={(e) => {
                      if (handleChange) {
                        handleChange(e, name);
                      }
                    }}
                    color="default"
                  />
                }
                label={variable.disabled ? falseText : trueText}
              />
            </Grid>
          )}
        </>
      )}
      {'arrayEnabled' in variable && steps !== 1 && (
        <>
          <Grid item xs={12} md={7} xl={7} sx={{ alignContent: 'center' }}>
            {`Perfil de ${variableName.toLowerCase()}:`}
          </Grid>
          <Grid item xs={6} md={5} xl={5} sx={{ alignContent: 'center' }}>
            <FormControlLabel
              control={
                <Switch
                  checked={variable.arrayEnabled}
                  name="variableArrayCustomize"
                  disabled={arrayDisabled}
                  onChange={(e) => {
                    if (handleChange) {
                      handleChange(e, name);
                    }
                  }}
                  color="default"
                />
              }
              label={variable.arrayEnabled ? 'On' : 'Off'}
            />
          </Grid>
        </>
      )}
    </Grid>
  );
};

export default ToggleArrayCustomNumberField;
