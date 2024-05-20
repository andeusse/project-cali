import { InputType } from '../../types/inputType';
import {
  COMMON_BATTERY_SYSTEM,
  COMMON_BIOGAS_SYSTEM,
  COMMON_HYDRAULIC_SYSTEM,
  COMMON_LOAD_SYSTEM,
  COMMON_SOLAR_SYSTEM,
  COMMON_WIND_SYSTEM,
  SmartSystemParameters,
} from '../../types/scenarios/common';
import { v4 as uuidv4 } from 'uuid';

export const setScenario = (
  e: any,
  oldState: SmartSystemParameters
): SmartSystemParameters => {
  let newState = { ...oldState };
  const name: string = e.target.name;
  const value: number = parseFloat(e.target.value);

  if (name === 'steps') {
    newState.solarSystems.forEach((s) => {
      s.radiationArray = Array(value ? value : 1).fill(0);
      s.temperatureArray = Array(value ? value : 1).fill(0);
    });
    newState.batterySystems.forEach((s) => {
      s.chargePowerArray = Array(value ? value : 1).fill(0);
      s.dischargePowerArray = Array(value ? value : 1).fill(0);
    });
    newState.hydraulicSystems.forEach((s) => {
      s.waterHeadArray = Array(value ? value : 1).fill(0);
      s.waterFlowArray = Array(value ? value : 1).fill(0);
    });
    newState.windSystems.forEach((s) => {
      s.windSpeedArray = Array(value ? value : 1).fill(0);
    });
    newState.loadSystems.forEach((s) => {
      s.powerArray = Array(value ? value : 1).fill(10);
    });
  }
  if (name.includes('SystemNumber')) {
    if ('solarSystems' in newState && name.includes('solar')) {
      if (value > newState.solarSystemNumber.value) {
        const newSystem = {
          ...COMMON_SOLAR_SYSTEM,
          radiationArray: Array(newState.steps.value).fill(0),
          temperatureArray: Array(newState.steps.value).fill(0),
          id: uuidv4(),
        };
        newState.priorityList.push({ id: newSystem.id, name: newSystem.name });
        newState.solarSystems = [
          ...newState.solarSystems,
          {
            ...newSystem,
          },
        ];
      } else if (value < newState.solarSystemNumber.value) {
        const removeSystem =
          newState.solarSystems[newState.solarSystems.length - 1];
        newState.priorityList = [
          ...newState.priorityList.filter((f) => f.id !== removeSystem.id),
        ];
        newState.solarSystems.splice(-1);
      }
    }
    if ('batterySystems' in newState && name.includes('battery')) {
      if (value > newState.batterySystemNumber.value) {
        const newSystem = {
          ...COMMON_BATTERY_SYSTEM,
          chargePowerArray: Array(newState.steps.value).fill(0),
          dischargePowerArray: Array(newState.steps.value).fill(0),
          id: uuidv4(),
        };
        newState.priorityList.push({ id: newSystem.id, name: newSystem.name });
        newState.batterySystems = [
          ...newState.batterySystems,
          { ...newSystem },
        ];
      } else if (value < newState.batterySystemNumber.value) {
        const removeSystem =
          newState.batterySystems[newState.batterySystems.length - 1];
        newState.priorityList = [
          ...newState.priorityList.filter((f) => f.id !== removeSystem.id),
        ];
        newState.batterySystems.splice(-1);
      }
    }
    if ('hydraulicSystems' in newState && name.includes('hydraulic')) {
      if (value > newState.hydraulicSystemNumber.value) {
        const newSystem = {
          ...COMMON_HYDRAULIC_SYSTEM,
          waterHeadArray: Array(newState.steps.value).fill(0),
          waterFlowArray: Array(newState.steps.value).fill(0),
          id: uuidv4(),
        };
        newState.priorityList.push({ id: newSystem.id, name: newSystem.name });
        newState.hydraulicSystems = [
          ...newState.hydraulicSystems,
          { ...newSystem },
        ];
      } else if (value < newState.hydraulicSystemNumber.value) {
        const removeSystem =
          newState.hydraulicSystems[newState.hydraulicSystems.length - 1];
        newState.priorityList = [
          ...newState.priorityList.filter((f) => f.id !== removeSystem.id),
        ];
        newState.hydraulicSystems.splice(-1);
      }
    }
    if ('windSystems' in newState && name.includes('wind')) {
      if (value > newState.windSystemNumber.value) {
        const newSystem = {
          ...COMMON_WIND_SYSTEM,
          windSpeedArray: Array(newState.steps.value).fill(0),
          id: uuidv4(),
        };
        newState.priorityList.push({ id: newSystem.id, name: newSystem.name });
        newState.windSystems = [...newState.windSystems, { ...newSystem }];
      } else if (value < newState.windSystemNumber.value) {
        const removeSystem =
          newState.windSystems[newState.windSystems.length - 1];
        newState.priorityList = [
          ...newState.priorityList.filter((f) => f.id !== removeSystem.id),
        ];
        newState.windSystems.splice(-1);
      }
    }
    if ('biogasSystems' in newState && name.includes('biogas')) {
      if (value > newState.biogasSystemNumber.value) {
        const newSystem = { ...COMMON_BIOGAS_SYSTEM, id: uuidv4() };
        newState.priorityList.push({ id: newSystem.id, name: newSystem.name });
        newState.biogasSystems = [...newState.biogasSystems, { ...newSystem }];
      } else if (value < newState.biogasSystemNumber.value) {
        const removeSystem =
          newState.biogasSystems[newState.biogasSystems.length - 1];
        newState.priorityList = [
          ...newState.priorityList.filter((f) => f.id !== removeSystem.id),
        ];
        newState.biogasSystems.splice(-1);
      }
    }
    if ('loadSystems' in newState && name.includes('load')) {
      if (value > newState.loadSystemNumber.value) {
        newState.loadSystems = [
          ...newState.loadSystems,
          {
            ...COMMON_LOAD_SYSTEM,
            powerArray: Array(newState.steps.value).fill(10),
            id: uuidv4(),
          },
        ];
      } else if (value < newState.loadSystemNumber.value) {
        newState.loadSystems.splice(-1);
      }
    }
  }
  newState = {
    ...newState,
    [name]: {
      ...(newState[name as keyof SmartSystemParameters] as InputType),
      value: value,
    },
  };
  return newState;
};
