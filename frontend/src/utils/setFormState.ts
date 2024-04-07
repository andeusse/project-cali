import { InputType } from '../types/models/common';
import { TurbineParameters } from '../types/models/turbine';
import { SolarWindParameters } from '../types/models/solar';
import { BiogasParameters } from '../types/models/biogas';
import { SmartCityParameters } from '../types/models/smartCity';
import { setTurbine } from './models/setTurbine';
import { setBiogas } from './models/setBiogas';
import { setSolar } from './models/setSolar';

type formType =
  | TurbineParameters
  | SolarWindParameters
  | BiogasParameters
  | SmartCityParameters;

export const setFormState = <T extends formType>(
  e: any,
  oldState: T,
  variableName?: string
) => {
  let newState = { ...oldState };

  const name = e.target.name as string;
  const type = e.target.type as string;

  if ('turbineType' in oldState) {
    if (
      name === 'turbineType' ||
      name === 'controller.customize' ||
      name === 'inputOfflineOperation'
    ) {
      return setTurbine(e, oldState);
    }
  }
  if ('anaerobicReactorVolume1' in oldState) {
    if (
      name === 'inputOfflineOperation' ||
      name === 'inputDigitalTwin' ||
      name === 'inputSubstrateConditions' ||
      name === 'inputPump104' ||
      name === 'inputPump102' ||
      name === 'inputPump101' ||
      name === 'inputOperationMode'
    ) {
      return setBiogas(e, oldState);
    }
  }
  if ('monocrystallinePanel' in oldState) {
    if (e.target.name === 'controller.customize') {
      return setSolar(e, oldState);
    }
  }

  const splitName = name.split('.');
  if (splitName.length !== 1) {
    if (splitName.length === 2) {
      const s: any = oldState[splitName[0] as keyof T];
      if (typeof s[splitName[1]] === 'object') {
        newState = {
          ...oldState,
          [splitName[0]]: {
            ...s,
            [splitName[1]]: {
              ...(s[splitName[1]] as InputType),
              value: e.target.value,
            },
          },
        };
      } else {
        let newValue = e.target.value;
        if (type === 'checkbox') {
          newValue = e.target.checked;
        }
        newState = {
          ...oldState,
          [splitName[0]]: {
            ...s,
            [splitName[1]]: newValue,
          },
        };
      }
    }
  } else if (type === 'checkbox' && name === 'variableCustomize') {
    if (variableName) {
      (newState[variableName as keyof T] as InputType).disabled =
        !e.target.checked;
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
