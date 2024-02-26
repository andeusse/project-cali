import { inputType } from './common';

export enum turbineType {
  Pelton = 'Pelton',
  Turgo = 'Turgo',
}

export function string2TurbineType(s: string): turbineType {
  return s === turbineType.Pelton ? turbineType.Pelton : turbineType.Turgo;
}

export enum controllerStateType {
  Encendida = 'Encendida',
  Apagada = 'Apagada',
}

export function string2ControllerStateType(s: string): controllerStateType {
  return s === controllerStateType.Encendida
    ? controllerStateType.Encendida
    : controllerStateType.Apagada;
}

export type turbine = {
  turbineType: turbineType;
  controllerInitialState: controllerStateType;
  controllerCustomize: boolean;
  controllerEfficiency: inputType;
  controllerChargeVoltageBulk: inputType;
  controllerChargeVoltageFloat: inputType;
  controllerChargingMinimunVoltage: inputType;
  controllerDissipatorOffVoltage: inputType;
  controllerDissipatorOnVoltage: inputType;
  batteryStateOfCharge: inputType;
  batteryTemperatureCoefficient: inputType;
  batteryCapacity: inputType;
  batterySelfDischargeCoefficient: inputType;
  batteryChargeDischargeEfficiency: inputType;
  batteryTemperatureCompensationCoefficient: inputType;
  inverterEfficiency: inputType;
  inverterNominalPower: inputType;
};

export const TURBINE: turbine = {
  turbineType: turbineType.Pelton,
  controllerCustomize: false,
  controllerInitialState: controllerStateType.Apagada,
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
  },
  controllerChargeVoltageFloat: {
    disabled: true,
    value: 27.8,
    tooltip: 'Voltaje de carga flotante',
    unit: 'V',
    variableName: 'V',
    subIndex: 'float',
  },
  controllerChargingMinimunVoltage: {
    disabled: true,
    value: 24,
    tooltip: 'Voltaje mínimo de inicio de carga',
    unit: 'V',
    variableName: 'V',
    subIndex: 'bat_min',
  },
  controllerDissipatorOffVoltage: {
    disabled: true,
    value: 24.75,
    tooltip: 'Voltaje de apagado de carga disipadora',
    unit: 'V',
    variableName: 'V',
    subIndex: 'sink_off',
  },
  controllerDissipatorOnVoltage: {
    disabled: true,
    value: 28,
    tooltip: 'Voltaje de encendido de carga disipadora',
    unit: 'V',
    variableName: 'V',
    subIndex: 'sink_on',
  },
  batteryStateOfCharge: {
    disabled: false,
    value: 100,
    tooltip: 'Estado de carga inicial',
    unit: '%',
    variableName: 'SOC',
    subIndex: 'inicial',
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
