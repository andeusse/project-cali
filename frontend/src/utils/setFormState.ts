import { InputType } from '../types/models/common';
import { SolarPanelParameters } from '../types/models/solar';
import { TurbineParameters } from '../types/models/turbine';

export const setFormState = <
  T extends TurbineParameters | SolarPanelParameters
>(
  e: any,
  oldState: T,
  variableName?: string
) => {
  let newState = { ...oldState };
  if (e.target.name === 'controllerCustomize') {
    if ('controllerCustomize' in newState) {
      newState.controllerCustomize = e.target.checked;
      newState.controllerChargeVoltageBulk.disabled = !e.target.checked;
      newState.controllerChargeVoltageFloat.disabled = !e.target.checked;
      newState.controllerChargingMinimunVoltage.disabled = !e.target.checked;
      newState.controllerDissipatorOffVoltage.disabled = !e.target.checked;
      newState.controllerDissipatorOnVoltage.disabled = !e.target.checked;
    }
  } else if (
    e.target.type === 'checkbox' &&
    e.target.name === 'variableCustomize'
  ) {
    if (variableName) {
      (newState[variableName as keyof T] as InputType).disabled =
        !e.target.checked;
    }
    return newState;
  } else if (typeof oldState[e.target.name as keyof T] === 'object') {
    newState = {
      ...oldState,
      [e.target.name]: {
        ...(oldState[e.target.name as keyof T] as InputType),
        value: e.target.value,
      },
    };
  } else if (e.target.type === 'checkbox') {
    newState = { ...oldState, [e.target.name]: e.target.checked };
  } else {
    newState = { ...oldState, [e.target.name]: e.target.value };
  }
  return newState;
};
