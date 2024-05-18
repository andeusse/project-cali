import { InputType } from '../../types/inputType';
import {
  SetSystemArrayType,
  WindSystem,
  SmartSystemParameters,
} from '../../types/scenarios/common';

export const setWindSystemById = <T extends SmartSystemParameters>(
  e: any,
  oldState: T,
  id: string
) => {
  const newState = { ...oldState };
  const value = e.target.value;
  const name = e.target.name;
  let system = newState.windSystems.find((s) => s.id === id);
  if (system !== undefined) {
    if (typeof system[name as keyof WindSystem] === 'object') {
      system = {
        ...system,
        [name]: {
          ...(system[name as keyof WindSystem] as InputType),
          value: parseFloat(value),
        },
      };
    } else {
      system = { ...system, [name]: e.target.value };
    }
  }
  newState.windSystems = newState.windSystems.map((s) => {
    if (system && s.id === id) {
      return system;
    }
    return s;
  });
  return newState;
};

export const setWindSystemArraysById = <T extends SmartSystemParameters>(
  props: SetSystemArrayType<T>
) => {
  const { e, oldState, id } = props;
  const newState = { ...oldState };
  let system = newState.windSystems.find((s) => s.id === id);
  if (system) {
    // system.chargePowerArray = matrix2Array(e, 0).slice(0, newState.steps.value);
  }
  newState.windSystems = newState.windSystems.map((s) => {
    if (system && s.id === id) {
      return system;
    }
    return s;
  });
  return newState;
};
