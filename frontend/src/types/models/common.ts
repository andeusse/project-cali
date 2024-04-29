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
  hasAdditionalCondition?: boolean;
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