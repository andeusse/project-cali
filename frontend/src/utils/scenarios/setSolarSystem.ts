import { CellBase, Matrix } from 'react-spreadsheet';
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
} from '../../types/scenarios/common';
import { matrix2Array } from '../matrix2Array';

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
  e: Matrix<CellBase>,
  oldState: T,
  id: string
) => {
  const newState = { ...oldState };
  let system = newState.solarSystems.find((s) => s.id === id);
  if (system) {
    system.radiationArray = matrix2Array(e, 0).slice(0, newState.steps.value);
    system.temperatureArray = matrix2Array(e, 1).slice(0, newState.steps.value);
  }
  newState.solarSystems = newState.solarSystems.map((s) => {
    if (system && s.id === id) {
      return system;
    }
    return s;
  });
  return newState;
};
