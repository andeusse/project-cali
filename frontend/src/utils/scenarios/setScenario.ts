import { InputType } from '../../types/inputType';
import {
  COMMON_BATTERY_SYSTEM,
  COMMON_BIOGAS_SYSTEM,
  COMMON_HYDRAULIC_SYSTEM,
  COMMON_SOLAR_SYSTEM,
  COMMON_WIND_SYSTEM,
  SMART_CITY_LOAD_SYSTEM,
  SMART_FACTORY_LOAD_SYSTEM,
  SMART_HOME_LOAD_SYSTEM,
  ScenariosLoadInputInformationType,
  ScenariosModesType,
  ScenariosSolarWindInputInformationType,
  ScenariosStepUnitType,
  SmartScenarioType,
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

  if (name === 'operationMode') {
    newState = { ...newState, [name]: e.target.value };
    if (
      newState.operationMode === ScenariosModesType.Automatic &&
      newState.batterySystemNumber.value !== 0
    ) {
      newState.steps = {
        ...newState.steps,
        value: 24,
        disabled: true,
      };
      newState.stepTime = {
        ...newState.stepTime,
        value: 1,
        disabled: true,
      };
      newState.stepUnit = ScenariosStepUnitType.Hour;
    } else {
      newState.steps = {
        ...newState.steps,
        disabled: false,
      };
      newState.stepTime = {
        ...newState.stepTime,
        disabled: false,
      };
    }
    return newState;
  }
  if (name === 'steps') {
    if (value !== 24) {
      newState.solarSystems.forEach((s) => {
        if (
          s.informationMode === ScenariosSolarWindInputInformationType.Typical
        ) {
          s.informationMode = ScenariosSolarWindInputInformationType.Fixed;
          s.radiation.tooltip = 'Irradiancia solar';
          s.radiation.variableString = 'Irradiancia solar';

          s.temperature.tooltip = 'Temperatura ambiente';
          s.temperature.variableString = 'Temperatura ambiente';
        }
      });
      newState.windSystems.forEach((s) => {
        if (
          s.informationMode === ScenariosSolarWindInputInformationType.Typical
        ) {
          s.informationMode = ScenariosSolarWindInputInformationType.Fixed;
          s.windSpeed.tooltip = 'Velocidad del viento';
          s.windSpeed.variableString = 'Velocidad del viento';
        }
      });
      newState.loadSystems.forEach((s) => {
        if (
          s.informationMode === ScenariosLoadInputInformationType.Commercial ||
          s.informationMode === ScenariosLoadInputInformationType.Industrial ||
          s.informationMode === ScenariosLoadInputInformationType.Residential
        ) {
          s.informationMode = ScenariosLoadInputInformationType.Fixed;
        }
      });
    }
    newState.solarSystems.forEach((s) => {
      s.radiationArray = Array(value ? value : 1).fill(800);
      s.temperatureArray = Array(value ? value : 1).fill(23);
    });
    newState.batterySystems.forEach((s) => {
      s.chargePowerArray = Array(value ? value : 1).fill(
        s.maxChargePower.value / 2
      );
      s.dischargePowerArray = Array(value ? value : 1).fill(
        s.maxDischargePower.value / 2
      );
    });
    newState.hydraulicSystems.forEach((s) => {
      s.waterHeadArray = Array(value ? value : 1).fill(
        s.maximumWaterHead.value / 2
      );
      s.waterFlowArray = Array(value ? value : 1).fill(
        s.maximumWaterFlow.value / 2
      );
    });
    newState.windSystems.forEach((s) => {
      s.windSpeedArray = Array(value ? value : 1).fill(s.ratedWindSpeed.value);
    });
    newState.loadSystems.forEach((s) => {
      s.powerArray = Array(value ? value : 1).fill(100);
    });
  }
  if (name.includes('SystemNumber')) {
    if ('solarSystems' in newState && name.includes('solar')) {
      if (value > newState.solarSystemNumber.value) {
        const newSystem = {
          ...COMMON_SOLAR_SYSTEM,
          name: `Sistema solar ${newState.solarSystemNumber.value + 1}`,
          radiationArray: Array(newState.steps.value).fill(800),
          temperatureArray: Array(newState.steps.value).fill(23),
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
      if (value === 0) {
        newState.steps = {
          ...newState.steps,
          disabled: false,
        };
        newState.stepTime = {
          ...newState.stepTime,
          disabled: false,
        };
      } else if (newState.operationMode === ScenariosModesType.Automatic) {
        newState.steps = {
          ...newState.steps,
          value: 24,
          disabled: true,
        };
        newState.stepTime = {
          ...newState.stepTime,
          value: 1,
          disabled: true,
        };
      }
      if (value > newState.batterySystemNumber.value) {
        const newSystem = {
          ...COMMON_BATTERY_SYSTEM,
          name: `Sistema de baterías ${newState.batterySystemNumber.value + 1}`,
          chargePowerArray: Array(newState.steps.value).fill(
            COMMON_BATTERY_SYSTEM.maxChargePower.value / 2
          ),
          dischargePowerArray: Array(newState.steps.value).fill(
            COMMON_BATTERY_SYSTEM.maxDischargePower.value / 2
          ),
          id: uuidv4(),
        };
        newState.batterySystems = [
          ...newState.batterySystems,
          { ...newSystem },
        ];
      } else if (value < newState.batterySystemNumber.value) {
        newState.batterySystems.splice(-1);
      }
    }
    if ('hydraulicSystems' in newState && name.includes('hydraulic')) {
      if (value > newState.hydraulicSystemNumber.value) {
        const newSystem = {
          ...COMMON_HYDRAULIC_SYSTEM,
          name: `Sistema de turbinas ${
            newState.hydraulicSystemNumber.value + 1
          }`,
          waterHeadArray: Array(newState.steps.value).fill(
            COMMON_HYDRAULIC_SYSTEM.maximumWaterHead.value / 2
          ),
          waterFlowArray: Array(newState.steps.value).fill(
            COMMON_HYDRAULIC_SYSTEM.maximumWaterFlow.value / 2
          ),
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
          name: `Sistema eólico ${newState.windSystemNumber.value + 1}`,
          windSpeedArray: Array(newState.steps.value).fill(
            COMMON_WIND_SYSTEM.ratedWindSpeed.value
          ),
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
        const newSystem = {
          ...COMMON_BIOGAS_SYSTEM,
          name: `Sistema de biogas ${newState.biogasSystemNumber.value + 1}`,
          id: uuidv4(),
        };
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
      let loadSystem = SMART_CITY_LOAD_SYSTEM;
      if (newState.smartScenarioType === SmartScenarioType.smartCity) {
        loadSystem = SMART_CITY_LOAD_SYSTEM;
      } else if (
        newState.smartScenarioType === SmartScenarioType.smartFactory
      ) {
        loadSystem = SMART_FACTORY_LOAD_SYSTEM;
      } else if (newState.smartScenarioType === SmartScenarioType.smartHome) {
        loadSystem = SMART_HOME_LOAD_SYSTEM;
      }
      if (value > newState.loadSystemNumber.value) {
        newState.loadSystems = [
          ...newState.loadSystems,
          {
            ...loadSystem,
            name: `Carga ${newState.loadSystemNumber.value + 1}`,
            powerArray: Array(newState.steps.value).fill(100),
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