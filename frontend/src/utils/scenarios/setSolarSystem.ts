import {
  CADMIUM_TELLURIDE_PANEL,
  CUSTOM_PANEL,
  FLEX_PANEL,
  MONOCRYSTALLINE_PANEL,
  POLICRYSTALLINE_PANEL,
} from '../../types/common';
import { InputType } from '../../types/inputType';
import {
  SolarSystem,
  SolarPanelModuleType,
  smartSystemParameters,
  ScenariosSolarPanelMeteorologicalInformationType,
  SetSystemArrayType,
} from '../../types/scenarios/common';
import { CellChange2Array } from '../cellChange2Array';

export const setSolarSystemById = <T extends smartSystemParameters>(
  e: any,
  oldState: T,
  id: string
) => {
  const newState = { ...oldState };
  const value = e.target.value;
  const name = e.target.name;

  let system = newState.solarSystems.find((s) => s.id === id);
  if (system !== undefined) {
    if (typeof system[name as keyof SolarSystem] === 'object') {
      system = {
        ...system,
        [name]: {
          ...(system[name as keyof SolarSystem] as InputType),
          value: parseFloat(value),
        },
      };
    } else {
      system = { ...system, [name]: e.target.value };
      if (name === 'moduleType') {
        let params = MONOCRYSTALLINE_PANEL;
        if (
          system[name as keyof SolarSystem] ===
          SolarPanelModuleType.MonocrystallinePanel
        ) {
          params = MONOCRYSTALLINE_PANEL;
        }
        if (
          system[name as keyof SolarSystem] ===
          SolarPanelModuleType.PolicrystallinePanel
        ) {
          params = POLICRYSTALLINE_PANEL;
        }
        if (
          system[name as keyof SolarSystem] === SolarPanelModuleType.FlexPanel
        ) {
          params = FLEX_PANEL;
        }
        if (
          system[name as keyof SolarSystem] ===
          SolarPanelModuleType.CadmiumTelluridePanel
        ) {
          params = CADMIUM_TELLURIDE_PANEL;
        }
        if (system[name as keyof SolarSystem] === SolarPanelModuleType.Custom) {
          params = CUSTOM_PANEL;
        }
        system = {
          ...system,
          ...params,
        };
      }
      if (name === 'meteorologicalInformationMode') {
        if (
          system.meteorologicalInformationMode ===
          ScenariosSolarPanelMeteorologicalInformationType.Fixed
        ) {
          system.radiation.tooltip = 'Irradiancia solar';
          system.radiation.variableString = 'Irradiancia solar';

          system.temperature.tooltip = 'Temperatura ambiente';
          system.temperature.variableString = 'Temperatura ambiente';
        }
        if (
          system.meteorologicalInformationMode ===
          ScenariosSolarPanelMeteorologicalInformationType.Typical
        ) {
          system.radiation.tooltip = 'Irradiancia solar máxima';
          system.radiation.variableString = 'Irradiancia solar máxima';

          system.temperature.tooltip = 'Temperatura ambiente máxima';
          system.temperature.variableString = 'Temperatura ambiente máxima';
        }
      }
    }
    newState.solarSystems = newState.solarSystems.map((s) => {
      if (system && s.id === id) {
        return system;
      }
      return s;
    });
  }
  return newState;
};

export const setSolarSystemArraysById = <T extends smartSystemParameters>(
  props: SetSystemArrayType<T>
) => {
  const { e, oldState, id } = props;
  const newState = { ...oldState };
  let system = newState.solarSystems.find((s) => s.id === id);
  if (system) {
    const newArrays = CellChange2Array(e, [
      system.radiationArray,
      system.temperatureArray,
    ]);
    system.radiationArray = newArrays[0];
    system.temperatureArray = newArrays[1];
  }
  newState.solarSystems = newState.solarSystems.map((s) => {
    if (system && s.id === id) {
      return system;
    }
    return s;
  });
  return newState;
};
