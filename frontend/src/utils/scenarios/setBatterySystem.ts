import { InputType } from '../../types/inputType';
import {
  BatterySystem,
  BatteryType,
  SetSystemArrayType,
  smartSystemParameters,
} from '../../types/scenarios/common';
import { CellChange2Array } from '../cellChange2Array';
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
      if (name === 'maxChargePower') {
        system.minChargePower.max = parseFloat(value);
      }
      if (name === 'maxDischargePower') {
        system.minDischargePower.max = parseFloat(value);
      }
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
  props: SetSystemArrayType<T>
) => {
  const { e, oldState, id } = props;
  const newState = { ...oldState };
  let system = newState.batterySystems.find((s) => s.id === id);
  if (system) {
    const newArrays = CellChange2Array(e, [
      system.chargePowerArray,
      system.dischargePowerArray,
    ]);
    system.chargePowerArray = newArrays[0];
    system.dischargePowerArray = newArrays[1];
  }
  newState.batterySystems = newState.batterySystems.map((s) => {
    if (system && s.id === id) {
      return system;
    }
    return s;
  });
  return newState;
};
