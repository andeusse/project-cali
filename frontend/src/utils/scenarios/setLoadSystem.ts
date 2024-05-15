import { Matrix, CellBase } from 'react-spreadsheet';
import { InputType } from '../../types/inputType';
import {
  LoadSystem,
  smartSystemParameters,
} from '../../types/scenarios/common';
import { matrix2Array } from '../matrix2Array';

export const setLoadSystemById = <T extends smartSystemParameters>(
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

export const setLoadSystemArraysById = <T extends smartSystemParameters>(
  e: Matrix<CellBase>,
  oldState: T,
  id: string
) => {
  const newState = { ...oldState };
  let system = newState.loadSystems.find((s) => s.id === id);
  if (system) {
    // system.chargePowerArray = matrix2Array(e, 0).slice(0, newState.steps.value);
  }
  newState.loadSystems = newState.loadSystems.map((s) => {
    if (system && s.id === id) {
      return system;
    }
    return s;
  });
  return newState;
};
