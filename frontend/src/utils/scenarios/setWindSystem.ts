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
  SortableItemParameter,
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
      if (name === 'name') {
        newState.priorityList = newState.priorityList.map((e) => {
          if (system && e.id === id) {
            const value: SortableItemParameter = {
              id: e.id,
              name: system.name,
            };
            return value;
          }
          return e;
        });
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
    const newArrays = CellChange2Array(e, [system.windSpeedArray]);
    system.windSpeedArray = newArrays[0];
  }
  newState.windSystems = newState.windSystems.map((s) => {
    if (system && s.id === id) {
      return system;
    }
    return s;
  });
  return newState;
};
