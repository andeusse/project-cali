import { InputType } from '../../types/inputType';
import {
  LoadSystem,
  SetSystemArrayType,
  SmartSystemParameters,
} from '../../types/scenarios/common';
import { CellChange2Array } from '../cellChange2Array';

export const setLoadSystemById = <T extends SmartSystemParameters>(
  e: any,
  oldState: T,
  id: string
) => {
  const newState = { ...oldState };
  const value = e.target.value;
  const name = e.target.name;
  let system = newState.loadSystems.find((s) => s.id === id);
  if (system !== undefined) {
    if (typeof system[name as keyof LoadSystem] === 'object') {
      system = {
        ...system,
        [name]: {
          ...(system[name as keyof LoadSystem] as InputType),
          value: parseFloat(value),
        },
      };
    } else {
      system = { ...system, [name]: e.target.value };
    }
  }
  newState.loadSystems = newState.loadSystems.map((s) => {
    if (system && s.id === id) {
      return system;
    }
    return s;
  });
  return newState;
};

export const setLoadSystemArraysById = <T extends SmartSystemParameters>(
  props: SetSystemArrayType<T>
) => {
  const { e, oldState, id } = props;
  const newState = { ...oldState };
  let system = newState.loadSystems.find((s) => s.id === id);
  if (system) {
    const newArrays = CellChange2Array(e, [system.powerArray]);
    system.powerArray = newArrays[0].map((v) => {
      v = v < 10000000 ? v : 10000000;
      v = v > 0.1 ? v : 0.1;
      return v;
    });
  }
  newState.loadSystems = newState.loadSystems.map((s) => {
    if (system && s.id === id) {
      return system;
    }
    return s;
  });
  return newState;
};
