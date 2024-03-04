import { InputType } from './common';

export enum TurbineType {
  Pelton = 'Pelton',
  Turgo = 'Turgo',
}

export function string2TurbineType(s: string): TurbineType {
  return s === TurbineType.Pelton ? TurbineType.Pelton : TurbineType.Turgo;
}

export enum ControllerStateType {
  Encendida = 'Encendida',
  Apagada = 'Apagada',
}

export function string2ControllerStateType(s: string): ControllerStateType {
  return s === ControllerStateType.Encendida
    ? ControllerStateType.Encendida
    : ControllerStateType.Apagada;
}

export type TurbineParameters = {
  turbineType: TurbineType;
  controllerInitialState: ControllerStateType;
  controllerCustomize: boolean;
  controllerEfficiency: InputType;
  controllerChargeVoltageBulk: InputType;
  controllerChargeVoltageFloat: InputType;
  controllerChargingMinimunVoltage: InputType;
  controllerDissipatorOffVoltage: InputType;
  controllerDissipatorOnVoltage: InputType;
  batteryStateOfCharge: InputType;
  batteryTemperatureCoefficient: InputType;
  batteryCapacity: InputType;
  batterySelfDischargeCoefficient: InputType;
  batteryChargeDischargeEfficiency: InputType;
  batteryTemperatureCompensationCoefficient: InputType;
  inverterEfficiency: InputType;
  inverterNominalPower: InputType;
  inputPressure: InputType;
  inputFlow: InputType;
  inputActivePower: InputType;
  inputPowerFactor: InputType;
};

export const TURBINE: TurbineParameters = {
  turbineType: TurbineType.Pelton,
  controllerCustomize: false,
  controllerInitialState: ControllerStateType.Apagada,
  controllerEfficiency: {
    disabled: true,
    value: 96,
    tooltip: 'Eficiencia del controlador de carga',
    unit: '%',
    variableName: 'η',
    subIndex: 'controller',
  },
  controllerChargeVoltageBulk: {
    disabled: true,
    value: 27.2,
    tooltip: 'Voltaje de carga bulk',
    unit: 'V',
    variableName: 'V',
    subIndex: 'bulk',
    min: 20,
    max: 35,
  },
  controllerChargeVoltageFloat: {
    disabled: true,
    value: 27.8,
    tooltip: 'Voltaje de carga flotante',
    unit: 'V',
    variableName: 'V',
    subIndex: 'float',
    min: 20,
    max: 35,
  },
  controllerChargingMinimunVoltage: {
    disabled: true,
    value: 24,
    tooltip: 'Voltaje mínimo de inicio de carga',
    unit: 'V',
    variableName: 'V',
    subIndex: 'bat_min',
    min: 24,
    max: 35,
  },
  controllerDissipatorOffVoltage: {
    disabled: true,
    value: 24.75,
    tooltip: 'Voltaje de apagado de carga disipadora',
    unit: 'V',
    variableName: 'V',
    subIndex: 'sink_off',
    min: 24,
    max: 35,
  },
  controllerDissipatorOnVoltage: {
    disabled: true,
    value: 28,
    tooltip: 'Voltaje de encendido de carga disipadora',
    unit: 'V',
    variableName: 'V',
    subIndex: 'sink_on',
    min: 24,
    max: 35,
  },
  batteryStateOfCharge: {
    disabled: false,
    value: 100,
    tooltip: 'Estado de carga inicial',
    unit: '%',
    variableName: 'SOC',
    subIndex: 'inicial',
    min: 0,
    max: 100,
  },
  batteryTemperatureCoefficient: {
    disabled: true,
    value: 0.6,
    tooltip: 'Coeficiente de temperatura',
    unit: '% / °C',
    variableName: 'δ',
    subIndex: 'C',
  },
  batteryCapacity: {
    disabled: true,
    value: 150,
    tooltip: 'Capacidad',
    unit: 'Ah',
    variableName: 'Capacidad',
    subIndex: 'bat',
  },
  batterySelfDischargeCoefficient: {
    disabled: true,
    value: 2.5,
    tooltip: 'Coeficiente de autodescarga',
    unit: '% / dia',
    variableName: 'σ',
    subIndex: 'bat',
  },
  batteryChargeDischargeEfficiency: {
    disabled: true,
    value: 98,
    tooltip: 'Eficiencia de carga y descarga',
    unit: '% / mes',
    variableName: 'η',
    subIndex: 'bat',
  },
  batteryTemperatureCompensationCoefficient: {
    disabled: true,
    value: -0.06,
    tooltip: 'Coeficiente de compensación de temperatura',
    unit: 'v / °C',
    variableName: 'δ',
    subIndex: 'V',
  },
  inverterEfficiency: {
    disabled: true,
    value: 90,
    tooltip: 'Eficiencia',
    unit: '%',
    variableName: 'η',
    subIndex: 'inverter',
  },
  inverterNominalPower: {
    disabled: true,
    value: 90,
    tooltip: 'Potencia nominal',
    unit: 'kW',
    variableName: 'P',
    subIndex: 'inverter',
  },

  inputPressure: {
    disabled: true,
    value: 100,
    tooltip: 'Presión',
    unit: 'kPa',
    variableName: 'Presión',
    subIndex: '',
    min: 0,
    max: 1000,
  },
  inputFlow: {
    disabled: true,
    value: 8,
    tooltip: 'Flujo',
    unit: 'l / s',
    variableName: 'Flujo',
    subIndex: '',
    min: 0,
    max: 10,
  },
  inputActivePower: {
    disabled: true,
    value: 200,
    tooltip: 'Potencia activa',
    unit: 'W',
    variableName: 'Potencia activa',
    subIndex: '',
    min: 0,
    max: 100000,
  },
  inputPowerFactor: {
    disabled: true,
    value: 1,
    tooltip: 'Factor de potencia',
    unit: '',
    variableName: 'Factor de potencia',
    subIndex: '',
    min: -1,
    max: 1,
  },
};

export const PELTON_TURBINE = [
  {
    disabled: true,
    value: 0.623,
    tooltip: 'Potencia nominal de la turbin',
    unit: 'kW',
    variableName: 'P',
    subIndex: 'tn',
  },
  {
    disabled: true,
    value: 3,
    tooltip: 'Mínima cabeza de agua de operación de la turbina',
    unit: 'm',
    variableName: 'H',
    subIndex: 'min',
  },
  {
    disabled: true,
    value: 130,
    tooltip: 'Máxima cabeza de agua de operación de la turbina',
    unit: 'm',
    variableName: 'H',
    subIndex: 'max',
  },
  {
    disabled: true,
    value: 75,
    tooltip: 'Eficiencia de la turbina',
    unit: '%',
    variableName: 'η',
    subIndex: 't',
  },
  {
    disabled: true,
    value: 0.0001,
    tooltip: 'Mínimo caudal de operación de la turbina',
    unit: 'm³',
    variableName: 'Q',
    subIndex: 'min',
  },
  {
    disabled: true,
    value: 0.01,
    tooltip: 'Máximo caudal de operación de la turbina',
    unit: 'm³',
    variableName: 'Q',
    subIndex: 'max',
  },
];

export const TURGO_TURBINE = [
  {
    disabled: true,
    value: 1.042,
    tooltip: 'Potencia nominal de la turbina',
    unit: 'kW',
    variableName: 'P',
    subIndex: 'tn',
  },
  {
    disabled: true,
    value: 2,
    tooltip: 'Mínima cabeza de agua de operación de la turbina',
    unit: 'm',
    variableName: 'H',
    subIndex: 'min',
  },
  {
    disabled: true,
    value: 30,
    tooltip: 'Máxima cabeza de agua de operación de la turbina',
    unit: 'm',
    variableName: 'H',
    subIndex: 'max',
  },
  {
    disabled: true,
    value: 75,
    tooltip: 'Eficiencia de la turbina',
    unit: '%',
    variableName: 'η',
    subIndex: 't',
  },
  {
    disabled: true,
    value: 0.008,
    tooltip: 'Mínimo caudal de operación de la turbina',
    unit: 'm³',
    variableName: 'Q',
    subIndex: 'min',
  },
  {
    disabled: true,
    value: 0.016,
    tooltip: 'Máximo caudal de operación de la turbina',
    unit: 'm³',
    variableName: 'Q',
    subIndex: 'max',
  },
];
