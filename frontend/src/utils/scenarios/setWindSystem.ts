import {
  CUSTOM_WIND_TURBINE,
  LABORATORY_WIND_TURBINE,
} from '../../types/common';
import { InputType } from '../../types/inputType';
import {
  SetSystemArrayType,
  WindSystem,
  SmartSystemParameters,
  WindType,
} from '../../types/scenarios/common';
import { CellChange2Array } from '../cellChange2Array';

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
      if (name === 'type') {
        let params = LABORATORY_WIND_TURBINE;
        if (system.type === WindType.Laboratory) {
          params = LABORATORY_WIND_TURBINE;
        }
        if (system.type === WindType.Custom) {
          params = CUSTOM_WIND_TURBINE;
        }
        system = {
          ...system,
          ...params,
        };
      }
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
    const newArrays = CellChange2Array(e, [system.windSpeed]);
    system.windSpeed = newArrays[0];
  }
  newState.windSystems = newState.windSystems.map((s) => {
    if (system && s.id === id) {
      return system;
    }
    return s;
  });
  return newState;
};
