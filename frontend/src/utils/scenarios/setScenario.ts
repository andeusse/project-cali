import { InputType } from '../../types/inputType';
import {
  COMMON_BATTERY_SYSTEM,
  COMMON_BIOGAS_SYSTEM,
  COMMON_HYDRAULIC_SYSTEM,
  COMMON_LOAD_SYSTEM,
  COMMON_SOLAR_SYSTEM,
  COMMON_WIND_SYSTEM,
  smartSystemParameters,
} from '../../types/scenarios/common';
import { v4 as uuidv4 } from 'uuid';

export const setScenario = (
  e: any,
  oldState: smartSystemParameters
): smartSystemParameters => {
  let newState = { ...oldState };
  const name: string = e.target.name;
  const value: number = parseFloat(e.target.value);

  if (name === 'steps') {
    if (value > newState.steps.value) {
      newState.solarSystems.forEach((s) => {
        s.radiationArray.push(0);
        s.temperatureArray.push(0);
      });
      newState.batterySystems.forEach((s) => {
        s.chargePowerArray.push(0);
        s.dischargePowerArray.push(0);
      });
    } else if (value < newState.steps.value) {
      newState.solarSystems.forEach((s) => {
        s.radiationArray.splice(-1);
        s.temperatureArray.splice(-1);
      });
      newState.batterySystems.forEach((s) => {
        s.chargePowerArray.splice(-1);
        s.dischargePowerArray.splice(-1);
      });
    }
  }
  if (name.includes('SystemNumber')) {
    if ('solarSystems' in newState && name.includes('solar')) {
      if (value > newState.solarSystemNumber.value) {
        newState.solarSystems = [
          ...newState.solarSystems,
          { ...COMMON_SOLAR_SYSTEM, id: uuidv4() },
        ];
      } else if (value < newState.solarSystemNumber.value) {
        newState.solarSystems.splice(-1);
      }
    }
    if ('biogasSystems' in newState && name.includes('biogas')) {
      if (value > newState.biogasSystemNumber.value) {
        newState.biogasSystems = [
          ...newState.biogasSystems,
          { ...COMMON_BIOGAS_SYSTEM, id: uuidv4() },
        ];
      } else if (value < newState.biogasSystemNumber.value) {
        newState.biogasSystems.splice(-1);
      }
    }
    if ('loadSystems' in newState && name.includes('load')) {
      if (value > newState.loadSystemNumber.value) {
        newState.loadSystems = [
          ...newState.loadSystems,
          { ...COMMON_LOAD_SYSTEM, id: uuidv4() },
        ];
      } else if (value < newState.loadSystemNumber.value) {
        newState.loadSystems.splice(-1);
      }
    }
    if ('batterySystems' in newState && name.includes('battery')) {
      if (value > newState.batterySystemNumber.value) {
        newState.batterySystems = [
          ...newState.batterySystems,
          { ...COMMON_BATTERY_SYSTEM, id: uuidv4() },
        ];
      } else if (value < newState.batterySystemNumber.value) {
        newState.batterySystems.splice(-1);
      }
    }
    if ('hydraulicSystems' in newState && name.includes('hydraulic')) {
      if (value > newState.hydraulicSystemNumber.value) {
        newState.hydraulicSystems = [
          ...newState.hydraulicSystems,
          { ...COMMON_HYDRAULIC_SYSTEM, id: uuidv4() },
        ];
      } else if (value < newState.hydraulicSystemNumber.value) {
        newState.hydraulicSystems.splice(-1);
      }
    }
    if ('windSystems' in newState && name.includes('wind')) {
      if (value > newState.windSystemNumber.value) {
        newState.windSystems = [
          ...newState.windSystems,
          { ...COMMON_WIND_SYSTEM, id: uuidv4() },
        ];
      } else if (value < newState.windSystemNumber.value) {
        newState.windSystems.splice(-1);
      }
    }
  }
  newState = {
    ...newState,
    [name]: {
      ...(newState[name as keyof smartSystemParameters] as InputType),
      value: value,
    },
  };
  return newState;
};
