import {
  BatterySystem,
  BiogasSystem,
  InputType,
  LoadSystem,
  SolarSystem,
} from './common';

export enum OperationModeType {
  Manual = 'Manual',
  Automatic = 'Automático',
}

export enum StepUnitType {
  Second = 'Segundo(s)',
  Minute = 'Minutos(s)',
  Hour = 'Hora(s)',
  Day = 'Día(s)',
}

export type SmartCityParameters = {
  operationMode: OperationModeType;
  steps: InputType;
  stepTime: InputType;
  stepUnit: StepUnitType;
  solarSystemNumber: InputType;
  batterySystemNumber: InputType;
  BiogasSystemNumber: InputType;
  LoadSystemNumber: InputType;
  solarSystems: SolarSystem[];
  batterySystems: BatterySystem[];
  BiogasSystems: BiogasSystem[];
  LoadSystems: LoadSystem[];
};

export const SOLAR_SYSTEM: SolarSystem = {
  name: 'Solar system',
};

export const BATTERY_SYSTEM: BatterySystem = {
  name: 'Battery system',
};

export const BIOGAS_SYSTEM: BiogasSystem = {
  name: 'Biogas system',
};

export const LOAD_SYSTEM: LoadSystem = {
  name: 'Load system',
};

export const SMART_CITY: SmartCityParameters = {
  operationMode: OperationModeType.Manual,
  steps: {
    disabled: false,
    value: 1,
    tooltip: 'Número de pasos a simular',
    unit: '',
    variableString: 'Número de pasos',
    variableSubString: '',
    min: 1,
  },
  stepTime: {
    disabled: false,
    value: 1,
    tooltip: 'Tiempo por paso',
    unit: '',
    variableString: 'Tiempo por paso',
    variableSubString: '',
    min: 1,
  },
  stepUnit: StepUnitType.Second,
  solarSystemNumber: {
    disabled: false,
    value: 1,
    tooltip: 'Número de sistemas solares',
    unit: '',
    variableString: 'Sistemas solares',
    variableSubString: '',
    min: 0,
  },
  batterySystemNumber: {
    disabled: false,
    value: 1,
    tooltip: 'Número de sistemas de baterías',
    unit: '',
    variableString: 'Sistemas de baterías',
    variableSubString: '',
    min: 0,
  },
  BiogasSystemNumber: {
    disabled: false,
    value: 1,
    tooltip: 'Número de sistemas de biogás',
    unit: '',
    variableString: 'Sistemas de biogás',
    variableSubString: '',
    min: 0,
  },
  LoadSystemNumber: {
    disabled: false,
    value: 1,
    tooltip: '',
    unit: '',
    variableString: '',
    variableSubString: '',
    min: 0,
  },
  solarSystems: [SOLAR_SYSTEM],
  batterySystems: [BATTERY_SYSTEM],
  BiogasSystems: [BIOGAS_SYSTEM],
  LoadSystems: [LOAD_SYSTEM],
};
