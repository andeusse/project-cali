import { CUSTOM_BIOGAS, EXAMPLE_BIOGAS } from '../../types/common';
import { InputType } from '../../types/inputType';
import {
  BiogasSystem,
  BiogasType,
  SmartSystemParameters,
} from '../../types/scenarios/common';

export const setBiogasSystemById = <T extends SmartSystemParameters>(
  e: any,
  oldState: T,
  id: string
) => {
  const newState = { ...oldState };
  const value = e.target.value;
  const name = e.target.name;
  let system = newState.biogasSystems.find((s) => s.id === id);
  if (system !== undefined) {
    if (typeof system[name as keyof BiogasSystem] === 'object') {
      system = {
        ...system,
        [name]: {
          ...(system[name as keyof BiogasSystem] as InputType),
          value: parseFloat(value),
        },
      };
      if (name === 'ambienteTemperature') {
        system = {
          ...system,
          temperatureSetpoint1: {
            ...system.temperatureSetpoint1,
            min: system.ambienteTemperature.value,
          },
          temperatureSetpoint2: {
            ...system.temperatureSetpoint2,
            min: system.ambienteTemperature.value,
          },
        };
      }
    } else {
      system = { ...system, [name]: e.target.value };
      if (name === 'type') {
        let params = EXAMPLE_BIOGAS;
        if (system.type === BiogasType.Laboratory) {
          params = EXAMPLE_BIOGAS;
        }
        if (system.type === BiogasType.Custom) {
          params = CUSTOM_BIOGAS;
        }
        system = {
          ...system,
          ...params,
        };
      }
    }
  }
  newState.biogasSystems = newState.biogasSystems.map((s) => {
    if (system && s.id === id) {
      return system;
    }
    return s;
  });
  return newState;
};
