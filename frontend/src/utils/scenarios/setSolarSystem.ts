import { Matrix } from 'react-spreadsheet';
import {
  CADMIUM_TELLURIDE_PANEL,
  CUSTOM_PANEL,
  FLEX_PANEL,
  MONOCRYSTALLINE_PANEL,
  POLICRYSTALLINE_PANEL,
} from '../../types/common';
import { InputType } from '../../types/inputType';
import { SolarPanel, SolarPanelModuleType } from '../../types/scenarios/common';
import { SmartCityParameters } from '../../types/scenarios/smartCity';
import { SmartFactoryParameters } from '../../types/scenarios/smartFactory';
import { SmartHomeParameters } from '../../types/scenarios/smartHome';
import { matrix2Array } from '../matrix2Array';

export type smartSystemParameters =
  | SmartCityParameters
  | SmartFactoryParameters
  | SmartHomeParameters;

export const setSolarSystemById = <T extends smartSystemParameters>(
  e: any,
  oldState: T,
  id: string
) => {
  const newState = { ...oldState };
  const value = e.target.value;
  const name = e.target.name;

  let system = newState.solarPanels.find((s) => s.id === id);
  if (system !== undefined) {
    if (typeof system[name as keyof SolarPanel] === 'object') {
      system = {
        ...system,
        [name]: {
          ...(system[name as keyof SolarPanel] as InputType),
          value: parseFloat(value),
        },
      };
    } else {
      system = { ...system, [name]: e.target.value };
      if (name === 'moduleType') {
        let panelParams = MONOCRYSTALLINE_PANEL;
        if (
          system[name as keyof SolarPanel] ===
          SolarPanelModuleType.MonocrystallinePanel
        ) {
          panelParams = MONOCRYSTALLINE_PANEL;
        }
        if (
          system[name as keyof SolarPanel] ===
          SolarPanelModuleType.PolicrystallinePanel
        ) {
          panelParams = POLICRYSTALLINE_PANEL;
        }
        if (
          system[name as keyof SolarPanel] === SolarPanelModuleType.FlexPanel
        ) {
          panelParams = FLEX_PANEL;
        }
        if (
          system[name as keyof SolarPanel] ===
          SolarPanelModuleType.CadmiumTelluridePanel
        ) {
          panelParams = CADMIUM_TELLURIDE_PANEL;
        }
        if (system[name as keyof SolarPanel] === SolarPanelModuleType.Custom) {
          panelParams = CUSTOM_PANEL;
        }
        system = {
          ...system,
          ...panelParams,
        };
      }
    }
    newState.solarPanels = newState.solarPanels.map((s) => {
      if (system && s.id === id) {
        return system;
      }
      return s;
    });
  }
  return newState;
};

export const setSolarSystemArraysById = <T extends smartSystemParameters>(
  e: Matrix<{
    value: number;
  }>,
  oldState: T,
  id: string
) => {
  const newState = { ...oldState };
  let system = newState.solarPanels.find((s) => s.id === id);
  if (system) {
    system.radiationArray = matrix2Array(e, 0).slice(0, newState.steps.value);
    system.temperatureArray = matrix2Array(e, 1).slice(0, newState.steps.value);
  }
  newState.solarPanels = newState.solarPanels.map((s) => {
    if (system && s.id === id) {
      return system;
    }
    return s;
  });
  return newState;
};
