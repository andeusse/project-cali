import { TurbineParameters } from '../types/models/turbine';
import { SolarWindParameters } from '../types/models/solar';
import { BiogasParameters } from '../types/models/biogas';
import { setTurbine } from './models/setTurbine';
import { setBiogas } from './models/setBiogas';
import { setSolar } from './models/setSolar';
import { setFormObjectValue } from './setFormObjectValue';
import { InputArrayType, InputType } from '../types/inputType';
import { setScenario } from './scenarios/setScenario';
import { SmartSystemParameters } from '../types/scenarios/common';
import { setCoolingTower } from './models/setCoolingTower';
import { CoolingTowerParameters } from '../types/models/coolingTower';
import { HydrogencellParameters } from '../types/models/hydrogenCell';
import { setHydrogenCell } from './models/setHydrogenCell';
import { BiochemicalMethanePotentialParameters } from '../types/models/biochemicalMethanePotential';

export type formType =
  | TurbineParameters
  | SolarWindParameters
  | BiogasParameters
  | CoolingTowerParameters
  | SmartSystemParameters
  | HydrogencellParameters
  | BiochemicalMethanePotentialParameters;

export const setFormState = <T extends formType>(
  e: any,
  oldState: T,
  variableName?: string
) => {
  let newState = { ...oldState };

  const name = e.target.name as string;
  const type = e.target.type as string;
  const splitName = name.split('.');

  if ('turbineType' in oldState) {
    if (
      name === 'turbineType' ||
      name === 'controller.customize' ||
      name === 'inputOfflineOperation' ||
      name === 'steps'
    ) {
      return setTurbine(e, oldState);
    }
  }
  if ('monocrystallinePanel' in oldState) {
    if (
      e.target.name === 'controller.customize' ||
      e.target.name === 'hybridInverter.customize' ||
      e.target.name === 'inputOfflineOperation' ||
      e.target.name === 'inputOperationMode' ||
      (splitName.length !== 1 && splitName[1] === 'isConnected') ||
      name === 'steps'
    ) {
      return setSolar(e, oldState);
    }
  }
  if ('anaerobicReactorVolume1' in oldState) {
    if (
      name === 'inputOfflineOperation' ||
      name === 'digitalTwinState' ||
      name === 'inputSubstrateConditions' ||
      name === 'inputPump104' ||
      name === 'inputPump102' ||
      name === 'inputPump101' ||
      name === 'inputMixTK100' ||
      name === 'inputMixR101' ||
      name === 'inputMixR102' ||
      name === 'inputOperationMode' ||
      name === 'operationModelType'
    ) {
      return setBiogas(e, oldState);
    }
  }
  if ('topWaterFlow' in oldState) {
    if (name === 'inputOfflineOperation' || name === 'steps') {
      return setCoolingTower(e, oldState);
    }
  }
  if ('electronicLoadMode' in oldState) {
    if (name === 'inputOfflineOperation' || name === 'steps') {
      return setHydrogenCell(e, oldState);
    }
  }
  if ('operationMode' in oldState) {
    if (
      name.includes('SystemNumber') ||
      name === 'steps' ||
      name === 'operationMode'
    ) {
      return setScenario(e, oldState);
    }
  }

  if (splitName.length !== 1) {
    if (splitName.length === 2) {
      let newValue = e.target.value;
      if (type === 'checkbox') {
        newValue = e.target.checked;
      }
      newState = setFormObjectValue<T>(oldState, splitName, newValue);
    }
  } else if (type === 'checkbox' && name === 'variableCustomize') {
    if (variableName) {
      (
        newState[variableName as keyof T] as InputType | InputArrayType
      ).disabled = !e.target.checked;
    }
  } else if (type === 'checkbox' && name === 'variableArrayCustomize') {
    if (variableName) {
      (newState[variableName as keyof T] as InputArrayType).arrayEnabled =
        e.target.checked;
    }
  } else if (typeof oldState[name as keyof T] === 'object') {
    newState = {
      ...oldState,
      [name]: {
        ...(oldState[name as keyof T] as InputType),
        value: parseFloat(e.target.value),
      },
    };
  } else if (type === 'checkbox') {
    newState = { ...oldState, [name]: e.target.checked };
  } else {
    newState = { ...oldState, [name]: e.target.value };
  }
  return newState;
};
