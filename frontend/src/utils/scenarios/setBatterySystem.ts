import { Matrix, CellBase } from 'react-spreadsheet';
import { InputType } from '../../types/inputType';
import {
  BatterySystem,
  BatteryType,
  smartSystemParameters,
} from '../../types/scenarios/common';
import { matrix2Array } from '../matrix2Array';
import { CUSTOM_BATTERY, GEL_BATTERY } from '../../types/common';

export const setBatterySystemById = <T extends smartSystemParameters>(
  e: any,
  oldState: T,
  id: string
) => {
  const newState = { ...oldState };
  const value = e.target.value;
  const name = e.target.name;

  let system = newState.batterySystems.find((s) => s.id === id);
  if (system !== undefined) {
    if (typeof system[name as keyof BatterySystem] === 'object') {
      system = {
        ...system,
        [name]: {
          ...(system[name as keyof BatterySystem] as InputType),
          value: parseFloat(value),
        },
      };
    } else {
      system = { ...system, [name]: e.target.value };
      if (name === 'batteryType') {
        let params = CUSTOM_BATTERY;
        if (system[name as keyof BatterySystem] === BatteryType.Custom) {
          params = CUSTOM_BATTERY;
        } else {
          params = GEL_BATTERY;
        }
        system = {
          ...system,
          ...params,
        };
      }
    }
  }
  newState.batterySystems = newState.batterySystems.map((s) => {
    if (system && s.id === id) {
      return system;
    }
    return s;
  });
  return newState;
};

export const setBatterySystemArraysById = <T extends smartSystemParameters>(
  e: Matrix<CellBase>,
  oldState: T,
  id: string
) => {
  const newState = { ...oldState };
  let system = newState.batterySystems.find((s) => s.id === id);
  if (system) {
    system.chargePowerArray = matrix2Array(e, 0).slice(0, newState.steps.value);
    system.dischargePowerArray = matrix2Array(e, 1).slice(
      0,
      newState.steps.value
    );
  }
  newState.batterySystems = newState.batterySystems.map((s) => {
    if (system && s.id === id) {
      return system;
    }
    return s;
  });
  return newState;
};
