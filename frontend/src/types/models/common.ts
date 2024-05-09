import { TabType } from '../tab';
import { SmartCityParameters } from './smartCity';

export type InputType = {
  disabled: boolean;
  value: number;
  tooltip: string;
  unit: string;
  variableString: string;
  variableSubString?: string;
  min?: number;
  max?: number;
  step?: number;
};

export type DiagramVariableType = {
  name: string;
  variable: string;
  unit: string;
  isShown: boolean;
  diagramName?: string;
  fixed?: number;
  x?: number;
  y?: number;
  hasAdditionalCondition?: number;
};

export type CommonSystemParameter = {
  name: string;
};

export type CommonDigitalTwinsParameter = {
  inputOfflineOperation: boolean;
  timeMultiplier: InputType;
  queryTime: number;
  disableParameters: boolean;
};

export type IsConnected = {
  isConnected: boolean;
  isConnectedDisabled: boolean;
};

export type SolarPanel = IsConnected & {
  peakPower: InputType;
  deratingFactor: InputType;
  efficiency: InputType;
  nominalIrradiance: InputType;
  testIrradiance: InputType;
  nominalTemperature: InputType;
  testTemperature: InputType;
  operatingTemperature: InputType;
  temperatureVariationCoefficient: InputType;
};

export type WindTurbine = {
  peakPower: InputType;
  rotorHeight: InputType;
  anemometerHeight: InputType;
  ratedWindSpeed: InputType;
  lowerCutoffWindSpeed: InputType;
  upperCutoffWindSpeed: InputType;
};

export type CommonController = {
  customize: boolean;
  efficiency: InputType;
  chargeVoltageBulk: InputType;
  chargeVoltageFloat: InputType;
  chargingMinimunVoltage: InputType;
};

export type Battery = {
  stateOfCharge: InputType;
  temperatureCoefficient: InputType;
  capacity: InputType;
  selfDischargeCoefficient: InputType;
  chargeDischargeEfficiency: InputType;
  temperatureCompensationCoefficient: InputType;
};

export type Inverter = IsConnected & {
  efficiency: InputType;
  nominalPower: InputType;
};

export type InverterHybrid = IsConnected &
  Inverter & {
    customize: boolean;
    chargeVoltageBulk: InputType;
    chargeVoltageFloat: InputType;
    chargingMinimunVoltage: InputType;
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

export type CommonScenarioParameters = CommonSystemParameter & {
  operationMode: ScenariosModesType;
  steps: InputType;
  stepTime: InputType;
  stepUnit: ScenariosStepUnitType;
  solarSystemNumber: InputType;
  biogasSystemNumber: InputType;
  loadSystemNumber: InputType;
};

export const COMMON_SCENARIO: CommonScenarioParameters = {
  name: 'Nombre',
  operationMode: ScenariosModesType.Manual,
  steps: {
    disabled: false,
    value: 1,
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
};

export const COMMON_TABS: TabType[] = [
  {
    title: 'Solar',
    children: undefined,
  },
  {
    title: 'Biogás',
    children: undefined,
  },
  {
    title: 'Demanda',
    children: undefined,
  },
];
