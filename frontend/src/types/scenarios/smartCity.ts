import { InputType } from '../inputType';
import {
  CommonScenarioParameters,
  COMMON_SCENARIO,
  BatterySystem,
  COMMON_BATTERY_SYSTEM,
  COMMON_HYDRAULIC_SYSTEM,
  COMMON_WIND_SYSTEM,
  HydraulicSystem,
  WindSystem,
} from './common';

export type SmartCityParameters = CommonScenarioParameters & {
  houseArea: InputType;
  batterySystemNumber: InputType;
  hydraulicSystemNumber: InputType;
  windSystemNumber: InputType;
  batterySystems: BatterySystem[];
  hydraulicSystems: HydraulicSystem[];
  windSystems: WindSystem[];
};

export const SMART_CITY: SmartCityParameters = {
  ...COMMON_SCENARIO,
  houseArea: {
    disabled: false,
    value: 100,
    tooltip: 'Área de la casa',
    unit: 'm²',
    variableString: 'Área de la casa',
    min: 1,
    max: 1000,
  },
  batterySystemNumber: {
    disabled: false,
    value: 1,
    tooltip: 'Número de sistemas de baterías',
    unit: '',
    variableString: 'Sistemas de baterías',
    min: 0,
    max: 100,
  },
  hydraulicSystemNumber: {
    disabled: false,
    value: 1,
    tooltip: 'Número de sistemas hidráulicos',
    unit: '',
    variableString: 'Sistemas hidráulicos',
    min: 0,
    max: 100,
  },
  windSystemNumber: {
    disabled: false,
    value: 1,
    tooltip: 'Número de sistemas de eólicos',
    unit: '',
    variableString: 'Sistemas eólicos',
    min: 0,
    max: 100,
  },
  batterySystems: [{ ...COMMON_BATTERY_SYSTEM }],
  hydraulicSystems: [{ ...COMMON_HYDRAULIC_SYSTEM }],
  windSystems: [{ ...COMMON_WIND_SYSTEM }],
};

export const SMART_FACTORY: SmartCityParameters = {
  ...SMART_CITY,
};

export const SMART_HOME: SmartCityParameters = {
  ...SMART_CITY,
  solarSystemNumber: {
    ...SMART_CITY.solarSystemNumber,
    max: 10,
  },
};
