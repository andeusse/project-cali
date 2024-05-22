import {
  CUSTOM_TURBINE,
  PELTON_TURBINE,
  TURGO_TURBINE,
} from '../../types/common';
import { InputType } from '../../types/inputType';
import {
  HydraulicSystem,
  SetSystemArrayType,
  HydraulicType,
  SmartSystemParameters,
  SortableItemParameter,
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
      if (name === 'maximumWaterHead') {
        system.waterHead.max = parseFloat(value);
      }
      if (name === 'maximumWaterFlow') {
        system.waterFlow.max = parseFloat(value);
      }
      if (name === 'minimumWaterHead') {
        system.waterHead.min = parseFloat(value);
      }
      if (name === 'minimumWaterFlow') {
        system.waterFlow.min = parseFloat(value);
      }
    } else {
      system = { ...system, [name]: e.target.value };
      if (name === 'type') {
        let params = PELTON_TURBINE;
        if (system.type === HydraulicType.Pelton) {
          params = PELTON_TURBINE;
        }
        if (system.type === HydraulicType.Turgo) {
          params = TURGO_TURBINE;
        }
        if (system.type === HydraulicType.Custom) {
          params = CUSTOM_TURBINE;
        }
        system.waterHead = {
          ...system.waterHead,
          min: params.minimumWaterHead.value,
          max: params.maximumWaterHead.value,
          value: params.maximumWaterHead.value / 2,
        };
        system.waterFlow = {
          ...system.waterFlow,
          min: params.minimumWaterFlow.value,
          max: params.maximumWaterFlow.value,
          value: params.maximumWaterFlow.value / 2,
        };
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
