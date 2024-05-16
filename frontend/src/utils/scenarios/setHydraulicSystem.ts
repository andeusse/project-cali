import { InputType } from '../../types/inputType';
import {
  HydraulicSystem,
  SetSystemArrayType,
  smartSystemParameters,
} from '../../types/scenarios/common';

export const setHydraulicSystemById = <T extends smartSystemParameters>(
  e: any,
  oldState: T,
  id: string
) => {
  const newState = { ...oldState };
  const value = e.target.value;
  const name = e.target.name;
  let system = newState.hydraulicSystems.find((s) => s.id === id);
  if (system !== undefined) {
    if (typeof system[name as keyof HydraulicSystem] === 'object') {
      system = {
        ...system,
        [name]: {
          ...(system[name as keyof HydraulicSystem] as InputType),
          value: parseFloat(value),
        },
      };
    } else {
      system = { ...system, [name]: e.target.value };
    }
  }
  newState.hydraulicSystems = newState.hydraulicSystems.map((s) => {
    if (system && s.id === id) {
      return system;
    }
    return s;
  });
  return newState;
};

export const setHydraulicSystemArraysById = <T extends smartSystemParameters>(
  props: SetSystemArrayType<T>
) => {
  const { e, oldState, id } = props;
  const newState = { ...oldState };
  let system = newState.hydraulicSystems.find((s) => s.id === id);
  if (system) {
    // system.chargePowerArray = matrix2Array(e, 0).slice(0, newState.steps.value);
  }
  newState.hydraulicSystems = newState.hydraulicSystems.map((s) => {
    if (system && s.id === id) {
      return system;
    }
    return s;
  });
  return newState;
};
