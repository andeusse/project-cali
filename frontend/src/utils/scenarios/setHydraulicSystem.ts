import {
  CUSTOM_TURBINE,
  PELTON_TURBINE,
  TURGO_TURBINE,
} from '../../types/common';
import { InputType } from '../../types/inputType';
import {
  HydraulicSystem,
  SetSystemArrayType,
  TurbineType,
  SmartSystemParameters,
} from '../../types/scenarios/common';
import { CellChange2Array } from '../cellChange2Array';

export const setHydraulicSystemById = <T extends SmartSystemParameters>(
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
      if (name === 'type') {
        let params = PELTON_TURBINE;
        if (system.type === TurbineType.Pelton) {
          params = PELTON_TURBINE;
        }
        if (system.type === TurbineType.Turgo) {
          params = TURGO_TURBINE;
        }
        if (system.type === TurbineType.Custom) {
          params = CUSTOM_TURBINE;
        }
        system = {
          ...system,
          ...params,
        };
      }
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

export const setHydraulicSystemArraysById = <T extends SmartSystemParameters>(
  props: SetSystemArrayType<T>
) => {
  const { e, oldState, id } = props;
  const newState = { ...oldState };
  let system = newState.hydraulicSystems.find((s) => s.id === id);
  if (system) {
    const newArrays = CellChange2Array(e, [
      system.waterHeadArray,
      system.waterFlowArray,
    ]);
    system.waterHeadArray = newArrays[0];
    system.waterFlowArray = newArrays[1];
  }
  newState.hydraulicSystems = newState.hydraulicSystems.map((s) => {
    if (system && s.id === id) {
      return system;
    }
    return s;
  });
  return newState;
};
