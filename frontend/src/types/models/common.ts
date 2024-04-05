import { ControllerStateType } from './turbine';

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
  x?: number;
  y?: number;
  diagramName?: string;
  unit: string;
  fixed?: number;
  isShown: boolean;
};

export type CommonSystemParameter = {
  name: string;
};

export type CommonDigitalTwinsParameter = {
  inputOfflineOperation: boolean;
  timeMultiplier: InputType;
};

export type SolarPanel = {
  isConnected: boolean;
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

export type Battery = {
  stateOfCharge: InputType;
  temperatureCoefficient: InputType;
  capacity: InputType;
  selfDischargeCoefficient: InputType;
  chargeDischargeEfficiency: InputType;
  temperatureCompensationCoefficient: InputType;
};

export const BATTERY: Battery = {
  stateOfCharge: {
    disabled: false,
    value: 50,
    tooltip: 'Estado de carga inicial',
    unit: '%',
    variableString: 'SOC',
    variableSubString: 'inicial',
    min: 0,
    max: 100,
  },
  temperatureCoefficient: {
    disabled: true,
    value: 0.6,
    tooltip: 'Coeficiente de temperatura',
    unit: '% / °C',
    variableString: 'δ',
    variableSubString: 'C',
  },
  capacity: {
    disabled: true,
    value: 150,
    tooltip: 'Capacidad',
    unit: 'Ah',
    variableString: 'Capacidad',
    variableSubString: 'bat',
  },
  selfDischargeCoefficient: {
    disabled: true,
    value: 2.5,
    tooltip: 'Coeficiente de autodescarga',
    unit: '% / dia',
    variableString: 'σ',
    variableSubString: 'bat',
  },
  chargeDischargeEfficiency: {
    disabled: true,
    value: 98,
    tooltip: 'Eficiencia de carga y descarga',
    unit: '% / mes',
    variableString: 'η',
    variableSubString: 'bat',
  },
  temperatureCompensationCoefficient: {
    disabled: true,
    value: -0.06,
    tooltip: 'Coeficiente de compensación de temperatura',
    unit: 'V / °C',
    variableString: 'δ',
    variableSubString: 'V',
  },
};
