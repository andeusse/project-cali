import {
  CommonSystemParameter,
  SolarPanel as CommonSolarPanel,
  MONOCRYSTALLINE_PANEL,
  CUSTOM_BATTERY,
} from '../common';
import { InputType } from '../inputType';
import { v4 as uuidv4 } from 'uuid';
import { SmartCityParameters } from './smartCity';
import { CellChange } from '@silevis/reactgrid';

export type smartSystemParameters = SmartCityParameters;

export type TabProps = {
  system: SmartCityParameters;
  handleSystemChange: (e: any, id: string, type: SmartSystemType) => void;
  handleTableChange: (
    e: CellChange[],
    id: string,
    type: SmartSystemType
  ) => void;
};

export type SetSystemArrayType<T> = {
  e: CellChange[];
  oldState: T;
  id: string;
};

export enum ScenariosModesType {
  Manual = 'Manual',
  Automatic = 'Automatic',
}

export enum ScenariosModesText {
  Manual = 'Manual',
  Automatic = 'Automático',
}

export enum ScenariosStepUnitType {
  Second = 'Second',
  Minute = 'Minute',
  Hour = 'Hour',
  Day = 'Day',
}

export enum ScenariosStepUnitText {
  Second = 'Segundo(s)',
  Minute = 'Minutos(s)',
  Hour = 'Hora(s)',
  Day = 'Día(s)',
}

export enum ScenariosSolarPanelMeteorologicalInformationType {
  Custom = 'Custom',
  Fixed = 'Fixed',
  Typical = 'Typical',
}

export enum ScenariosSolarPanelMeteorologicalInformationText {
  Custom = 'Perfil personalizado',
  Fixed = 'Perfil fijo',
  Typical = 'Perfil típico',
}

export enum SolarPanelModuleType {
  MonocrystallinePanel = 'MonocrystallinePanel',
  PolicrystallinePanel = 'PolicrystallinePanel',
  FlexPanel = 'FlexPanel',
  CadmiumTelluridePanel = 'CadmiumTelluridePanel',
  Custom = 'Custom',
}

export enum SolarPanelModuleText {
  MonocrystallinePanel = 'Monocristalino',
  PolicrystallinePanel = 'Policristalino',
  FlexPanel = 'Monocristalino flexible',
  CadmiumTelluridePanel = 'Telururo de cadmio',
  Custom = 'Personalizado',
}

export enum ScenariosBatteryInformationType {
  Custom = 'Custom',
  Fixed = 'Fixed',
}

export enum ScenariosBatteryInformationText {
  Custom = 'Perfil personalizado',
  Fixed = 'Perfil fijo',
}

export enum BatteryType {
  Gel = 'Gel',
  Custom = 'Custom',
}

export enum BatteryText {
  Gel = 'Gel (Laboratorio)',
  Custom = 'Personalizado',
}

export type SolarSystem = CommonSystemParameter &
  CommonSolarPanel & {
    id: string;
    modulesNumber: InputType;
    modulePower: InputType;
    meteorologicalInformationMode: ScenariosSolarPanelMeteorologicalInformationType;
    moduleType: SolarPanelModuleType;
    radiation: InputType;
    temperature: InputType;
    radiationArray: number[];
    temperatureArray: number[];
  };

export type BatteryTypeParameters = {
  selfDischargeCoefficient: InputType;
  chargeEfficiency: InputType;
  dischargeDischargeEfficiency: InputType;
};

export type BatterySystem = CommonSystemParameter &
  BatteryTypeParameters & {
    id: string;
    storageCapacity: InputType;
    maxChargePower: InputType;
    minChargePower: InputType;
    maxDischargePower: InputType;
    minDischargePower: InputType;
    stateOfCharge: InputType;
    batteryType: BatteryType;
    informationMode: ScenariosBatteryInformationType;
    chargePowerArray: number[];
    dischargePowerArray: number[];
  };

export type BiogasSystem = CommonSystemParameter & {
  id: string;
  var: InputType;
};

export type LoadSystem = CommonSystemParameter & {
  id: string;
  var: InputType;
};

export type HydraulicSystem = CommonSystemParameter & {
  id: string;
  var: InputType;
};

export type WindSystem = CommonSystemParameter & {
  id: string;
  var: InputType;
};

export enum SmartSystemType {
  Solar = 'Solar',
  Biogas = 'Biogas',
  Load = 'Load',
  Battery = 'Battery',
  Hydraulic = 'Hydraulic',
  Wind = 'Wind',
}

export type CommonScenarioParameters = CommonSystemParameter & {
  operationMode: ScenariosModesType;
  steps: InputType;
  stepTime: InputType;
  stepUnit: ScenariosStepUnitType;
  solarSystemNumber: InputType;
  biogasSystemNumber: InputType;
  loadSystemNumber: InputType;
  solarSystems: SolarSystem[];
  biogasSystems: BiogasSystem[];
  loadSystems: LoadSystem[];
};

export const COMMON_SOLAR_SYSTEM: SolarSystem = {
  id: uuidv4(),
  name: 'Sistema solar',
  modulesNumber: {
    disabled: false,
    value: 10,
    tooltip: 'Número de módulos solares',
    unit: '',
    variableString: 'Módulos solares',
    min: 1,
    max: 100000,
  },
  modulePower: {
    disabled: false,
    value: 500,
    tooltip: 'Potencia pico de cada módulo',
    unit: 'W',
    variableString: 'Potencia pico',
    min: 1,
    max: 1000,
  },
  meteorologicalInformationMode:
    ScenariosSolarPanelMeteorologicalInformationType.Custom,
  moduleType: SolarPanelModuleType.MonocrystallinePanel,
  ...MONOCRYSTALLINE_PANEL,
  radiation: {
    disabled: false,
    value: 800,
    tooltip: 'Irradiancia solar',
    unit: 'W / m²',
    variableString: 'Irradiancia solar',
    min: 0,
    max: 1500,
    step: 100,
  },
  temperature: {
    disabled: false,
    value: 25,
    tooltip: 'Temperatura ambiente',
    unit: '°C',
    variableString: 'Temperatura ambiente',
    min: -10,
    max: 50,
  },
  radiationArray: Array(24).fill(0),
  temperatureArray: Array(24).fill(0),
};

export const COMMON_BATTERY_SYSTEM: BatterySystem = {
  id: uuidv4(),
  name: 'Sistema de baterías',
  storageCapacity: {
    disabled: false,
    value: 10,
    tooltip: 'Capacidad de almacenamiento',
    unit: 'kW',
    variableString: 'Capacidad almacenamiento',
    min: 0.1,
    max: 10000,
    step: 0.1,
  },
  maxChargePower: {
    disabled: false,
    value: 10,
    tooltip: 'Potencia máxima de carga',
    unit: 'kW',
    variableString: 'Potencia máxima de carga',
    min: 0.1,
    max: 10000,
    step: 0.1,
  },
  minChargePower: {
    disabled: false,
    value: 0,
    tooltip: 'Potencia mínima de carga',
    unit: 'kW',
    variableString: 'Potencia mínima de carga',
    min: 0.1,
    max: 10,
    step: 0.1,
  },
  maxDischargePower: {
    disabled: false,
    value: 10,
    tooltip: 'Potencia máxima de descarga',
    unit: 'kW',
    variableString: 'Potencia máxima de descarga',
    min: 0.1,
    max: 10000,
    step: 0.1,
  },
  minDischargePower: {
    disabled: false,
    value: 0,
    tooltip: 'Potencia mínima de descarga',
    unit: 'kW',
    variableString: 'Potencia mínima de descarga',
    min: 0.1,
    max: 10,
    step: 0.1,
  },
  stateOfCharge: {
    disabled: false,
    value: 100,
    tooltip: 'Estado de carga inicial',
    unit: '',
    variableString: 'SOC',
    min: 0,
    max: 100,
  },
  informationMode: ScenariosBatteryInformationType.Custom,
  batteryType: BatteryType.Custom,
  ...CUSTOM_BATTERY,
  chargePowerArray: Array(24).fill(0),
  dischargePowerArray: Array(24).fill(0),
};

export const COMMON_HYDRAULIC_SYSTEM: HydraulicSystem = {
  id: uuidv4(),
  name: '',
  var: {
    disabled: false,
    value: 0,
    tooltip: '',
    unit: '',
    variableString: '',
  },
};

export const COMMON_WIND_SYSTEM: WindSystem = {
  id: uuidv4(),
  name: '',
  var: {
    disabled: false,
    value: 0,
    tooltip: '',
    unit: '',
    variableString: '',
  },
};

export const COMMON_LOAD_SYSTEM: LoadSystem = {
  id: uuidv4(),
  name: '',
  var: {
    disabled: false,
    value: 0,
    tooltip: '',
    unit: '',
    variableString: '',
  },
};

export const COMMON_BIOGAS_SYSTEM: BiogasSystem = {
  id: uuidv4(),
  name: '',
  var: {
    disabled: false,
    value: 0,
    tooltip: '',
    unit: '',
    variableString: '',
  },
};

export const COMMON_SCENARIO: CommonScenarioParameters = {
  name: 'Nombre',
  operationMode: ScenariosModesType.Manual,
  steps: {
    disabled: false,
    value: 24,
    tooltip: 'Número de pasos a simular',
    unit: '',
    variableString: 'Número de pasos',
    min: 1,
    max: 10000,
  },
  stepTime: {
    disabled: false,
    value: 1,
    tooltip: 'Tiempo por paso',
    unit: '',
    variableString: 'Tiempo por paso',
    min: 0.1,
    max: 100,
    step: 0.1,
  },
  stepUnit: ScenariosStepUnitType.Second,
  solarSystemNumber: {
    disabled: false,
    value: 1,
    tooltip: 'Número de sistemas solares',
    unit: '',
    variableString: 'Sistemas solares',
    min: 0,
    max: 100,
  },
  biogasSystemNumber: {
    disabled: false,
    value: 1,
    tooltip: 'Número de sistemas de biogás',
    unit: '',
    variableString: 'Sistemas de biogás',
    min: 0,
    max: 100,
  },
  loadSystemNumber: {
    disabled: false,
    value: 1,
    tooltip: 'Número de cargas',
    unit: '',
    variableString: 'Número de cargas',
    min: 1,
    max: 100,
  },
  solarSystems: [{ ...COMMON_SOLAR_SYSTEM }],
  biogasSystems: [{ ...COMMON_BIOGAS_SYSTEM }],
  loadSystems: [{ ...COMMON_LOAD_SYSTEM }],
};
