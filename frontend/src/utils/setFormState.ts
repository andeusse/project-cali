import { InputType } from '../types/models/common';
import { TurbineParameters } from '../types/models/turbine';
import { SolarPanelParameters } from '../types/models/solar';
import { BiogasParameters } from '../types/models/biogas';
import { SmartCityParameters } from '../types/models/smartCity';

export const setFormState = <
  T extends
    | TurbineParameters
    | SolarPanelParameters
    | BiogasParameters
    | SmartCityParameters
>(
  e: any,
  oldState: T,
  variableName?: string
) => {
  let newState = { ...oldState };
  if (e.target.name === 'controllerCustomize') {
    if ('turbineType' in newState) {
      newState.controllerCustomize = e.target.checked;
      newState.controllerChargeVoltageBulk.disabled = !e.target.checked;
      newState.controllerChargeVoltageFloat.disabled = !e.target.checked;
      newState.controllerChargingMinimunVoltage.disabled = !e.target.checked;
      newState.controllerSinkOffVoltage.disabled = !e.target.checked;
      newState.controllerSinkOnVoltage.disabled = !e.target.checked;
    }
  } else if (e.target.name === 'inputOfflineOperation') {
    if ('turbineType' in newState) {
      newState.inputOfflineOperation = !newState.inputOfflineOperation;
      if (newState.inputOfflineOperation) {
        newState.inputPressure.disabled = false;
        newState.inputFlow.disabled = false;
        newState.inputActivePower.disabled = false;
        newState.inputPowerFactor.disabled = false;
      }
    }
    if ('anaerobicReactorVolume1' in newState) {
      newState.inputOfflineOperation = !newState.inputOfflineOperation;
    }
  } else if (
    e.target.type === 'checkbox' &&
    e.target.name === 'variableCustomize'
  ) {
    if (variableName) {
      (newState[variableName as keyof T] as InputType).disabled =
        !e.target.checked;
    }
  } else if (typeof oldState[e.target.name as keyof T] === 'object') {
    newState = {
      ...oldState,
      [e.target.name]: {
        ...(oldState[e.target.name as keyof T] as InputType),
        value: parseFloat(e.target.value),
      },
    };
  } else if (e.target.type === 'checkbox') {
    newState = { ...oldState, [e.target.name]: e.target.checked };
  } else {
    newState = { ...oldState, [e.target.name]: e.target.value };
  }
  return newState;
};
