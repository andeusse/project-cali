import { CommonGraphType } from '../graph';
import {
  CommonSystemParameter,
  DiagramVariableType,
  InputType,
} from './common';

export enum TurbineType {
  Pelton = 'Pelton',
  Turgo = 'Turgo',
}

export enum ControllerStateType {
  Encendida = 'Encendida',
  Apagada = 'Apagada',
}

export type TurbineParameters = CommonSystemParameter & {
  turbineType: TurbineType;
  sinkLoadInitialState: ControllerStateType;
  controllerCustomize: boolean;
  controllerEfficiency: InputType;
  controllerChargeVoltageBulk: InputType;
  controllerChargeVoltageFloat: InputType;
  controllerChargingMinimunVoltage: InputType;
  controllerSinkOffVoltage: InputType;
  controllerSinkOnVoltage: InputType;
  batteryStateOfCharge: InputType;
  batteryTemperatureCoefficient: InputType;
  batteryCapacity: InputType;
  batterySelfDischargeCoefficient: InputType;
  batteryChargeDischargeEfficiency: InputType;
  batteryTemperatureCompensationCoefficient: InputType;
  inverterEfficiency: InputType;
  inverterNominalPower: InputType;
  inputOfflineOperation: boolean;
  inputPressure: InputType;
  inputFlow: InputType;
  inputDirectCurrentPower: boolean;
  inputActivePower: InputType;
  inputPowerFactor: InputType;
  simulatedBatteryStateOfCharge?: number;
  simulatedDirectCurrentVoltage?: number;
  simulatedSinkLoadState?: boolean;
  simulatedInverterState?: boolean;
};

export type TurbineOutput = {
  turbineCurrent: number;
  turbinePower: number;
  turbineVoltage: number;
  directCurrentVoltage: number;
  controllerCurrent: number;
  controllerPower: number;
  batteryStateOfCharge: number;
  batteryVoltage: number;
  batteryCurrent: number;
  batteryPower: number;
  batteryTemperature?: number;
  inverterApparentPower: number;
  inverterActivePower: number;
  inverterReactivePower: number;
  inverterState: boolean;
  inverterOutputVoltage: number;
  inverterOutputCurrent: number;
  inverterInputCurrent: number;
  inverterInputPower: number;
  sinkLoadState: boolean;
  sinkLoadPower: number;
  inputPressure?: number;
  inputFlow?: number;
  inputActivePower?: number;
  inputPowerFactor?: number;
};

export type TurbineOutputHistoric = CommonGraphType & {
  turbineCurrent: number[];
  turbinePower: number[];
  turbineVoltage: number[];
  directCurrentVoltage: number[];
  controllerCurrent: number[];
  controllerPower: number[];
  batteryStateOfCharge: number[];
  batteryVoltage: number[];
  batteryCurrent: number[];
  batteryPower: number[];
  batteryTemperature?: number[];
  inverterApparentPower: number[];
  inverterActivePower: number[];
  inverterReactivePower: number[];
  inverterState: boolean[];
  inverterOutputVoltage: number[];
  inverterOutputCurrent: number[];
  inverterInputCurrent: number[];
  inverterInputPower: number[];
  sinkLoadState: boolean[];
  sinkLoadPower: number[];
};

export const TURBINE: TurbineParameters = {
  name: 'Nombre',
  timeMultiplier: {
    disabled: false,
    value: 1,
    tooltip: 'Multiplicador de tiempo',
    unit: '',
    variableString: '',
    variableSubString: '',
    min: 1,
    max: 10,
  },
  turbineType: TurbineType.Pelton,
  controllerCustomize: false,
  sinkLoadInitialState: ControllerStateType.Apagada,
  controllerEfficiency: {
    disabled: true,
    value: 96,
    tooltip: 'Eficiencia del controlador de carga',
    unit: '%',
    variableString: 'η',
    variableSubString: 'controller',
  },
  controllerChargeVoltageBulk: {
    disabled: true,
    value: 27.2,
    tooltip: 'Voltaje de carga bulk',
    unit: 'V',
    variableString: 'V',
    variableSubString: 'bulk',
    min: 20,
    max: 35,
  },
  controllerChargeVoltageFloat: {
    disabled: true,
    value: 27.8,
    tooltip: 'Voltaje de carga flotante',
    unit: 'V',
    variableString: 'V',
    variableSubString: 'float',
    min: 20,
    max: 35,
  },
  controllerChargingMinimunVoltage: {
    disabled: true,
    value: 24,
    tooltip: 'Voltaje mínimo de inicio de carga',
    unit: 'V',
    variableString: 'V',
    variableSubString: 'bat_min',
    min: 24,
    max: 35,
  },
  controllerSinkOffVoltage: {
    disabled: true,
    value: 24.75,
    tooltip: 'Voltaje de apagado de carga disipadora',
    unit: 'V',
    variableString: 'V',
    variableSubString: 'sink_off',
    min: 24,
    max: 35,
  },
  controllerSinkOnVoltage: {
    disabled: true,
    value: 28,
    tooltip: 'Voltaje de encendido de carga disipadora',
    unit: 'V',
    variableString: 'V',
    variableSubString: 'sink_on',
    min: 24,
    max: 35,
  },
  batteryStateOfCharge: {
    disabled: false,
    value: 50,
    tooltip: 'Estado de carga inicial',
    unit: '%',
    variableString: 'SOC',
    variableSubString: 'inicial',
    min: 0,
    max: 100,
  },
  batteryTemperatureCoefficient: {
    disabled: true,
    value: 0.6,
    tooltip: 'Coeficiente de temperatura',
    unit: '% / °C',
    variableString: 'δ',
    variableSubString: 'C',
  },
  batteryCapacity: {
    disabled: true,
    value: 150,
    tooltip: 'Capacidad',
    unit: 'Ah',
    variableString: 'Capacidad',
    variableSubString: 'bat',
  },
  batterySelfDischargeCoefficient: {
    disabled: true,
    value: 2.5,
    tooltip: 'Coeficiente de autodescarga',
    unit: '% / dia',
    variableString: 'σ',
    variableSubString: 'bat',
  },
  batteryChargeDischargeEfficiency: {
    disabled: true,
    value: 98,
    tooltip: 'Eficiencia de carga y descarga',
    unit: '% / mes',
    variableString: 'η',
    variableSubString: 'bat',
  },
  batteryTemperatureCompensationCoefficient: {
    disabled: true,
    value: -0.06,
    tooltip: 'Coeficiente de compensación de temperatura',
    unit: 'V / °C',
    variableString: 'δ',
    variableSubString: 'V',
  },
  inverterEfficiency: {
    disabled: true,
    value: 90,
    tooltip: 'Eficiencia',
    unit: '%',
    variableString: 'η',
    variableSubString: 'inverter',
  },
  inverterNominalPower: {
    disabled: true,
    value: 90,
    tooltip: 'Potencia nominal',
    unit: 'kW',
    variableString: 'P',
    variableSubString: 'inverter',
  },
  inputOfflineOperation: false,
  inputPressure: {
    disabled: true,
    value: 100,
    tooltip: 'Presión',
    unit: 'kPa',
    variableString: 'Presión',
    variableSubString: '',
    min: 0,
    max: 1000,
  },
  inputFlow: {
    disabled: true,
    value: 8,
    tooltip: 'Flujo',
    unit: 'l / s',
    variableString: 'Flujo',
    variableSubString: '',
    min: 0,
    max: 10,
  },
  inputDirectCurrentPower: false,
  inputActivePower: {
    disabled: true,
    value: 200,
    tooltip: 'Potencia activa',
    unit: 'W',
    variableString: 'Potencia activa',
    variableSubString: '',
    min: 0,
    max: 100000,
  },
  inputPowerFactor: {
    disabled: true,
    value: 1,
    tooltip: 'Factor de potencia',
    unit: '',
    variableString: 'Factor de potencia',
    variableSubString: '',
    min: -1,
    max: 1,
  },
};

export const TURBINE_DIAGRAM_VARIABLES: DiagramVariableType[] = [
  {
    name: 'Voltaje turbina',
    variable: 'turbineVoltage',
    x: 255,
    y: 60,
    diagramName: 'Voltaje',
    unit: 'Vcd',
    fixed: 1,
  },
  {
    name: 'Corriente turbina',
    variable: 'turbineCurrent',
    x: 255,
    y: 85,
    diagramName: 'Corriente',
    unit: 'Acd',
    fixed: 1,
  },
  {
    name: 'Potencia turbina',
    variable: 'turbinePower',
    x: 255,
    y: 110,
    diagramName: 'Potencia',
    unit: 'W',
    fixed: 1,
  },
  {
    name: 'Voltaje corriente directa',
    variable: 'directCurrentVoltage',
    x: 130,
    y: 600,
    diagramName: 'Voltaje',
    unit: 'Vcd',
    fixed: 1,
  },
  {
    name: 'Corriente controlador',
    variable: 'controllerCurrent',
    x: 130,
    y: 625,
    diagramName: 'Corriente',
    unit: 'Acd',
    fixed: 1,
  },
  {
    name: 'Potencia controlador',
    variable: 'controllerPower',
    x: 130,
    y: 650,
    diagramName: 'Potencia',
    unit: 'W',
    fixed: 1,
  },
  {
    name: 'Estado de carga batería',
    variable: 'batteryStateOfCharge',
    x: 410,
    y: 50,
    diagramName: 'SOC',
    unit: '%',
    fixed: 3,
  },
  {
    name: 'Voltaje batería',
    variable: 'batteryVoltage',
    x: 410,
    y: 75,
    diagramName: 'Voltaje',
    unit: 'Vcd',
    fixed: 3,
  },
  {
    name: 'Corriente batería',
    variable: 'batteryCurrent',
    x: 410,
    y: 100,
    diagramName: 'Corriente',
    unit: 'Acd',
    fixed: 1,
  },
  {
    name: 'Potencia batería',
    variable: 'batteryPower',
    x: 410,
    y: 125,
    diagramName: 'Potencia',
    unit: 'W',
    fixed: 1,
  },
  {
    name: 'Temperatura batería',
    variable: 'batteryTemperature',
    x: 410,
    y: 150,
    diagramName: 'Temperatura',
    unit: '°C',
    fixed: 1,
  },
  {
    name: 'Potencia de entrada inversor',
    variable: 'inverterInputPower',
    x: 620,
    y: 75,
    diagramName: 'P entrada',
    unit: 'W',
    fixed: 1,
  },
  {
    name: 'Corriente de entrada inversor',
    variable: 'inverterInputCurrent',
    x: 620,
    y: 100,
    diagramName: 'I entrada',
    unit: 'Acd',
    fixed: 1,
  },
  {
    name: 'Potencia activa inversor',
    variable: 'inverterActivePower',
    x: 550,
    y: 350,
    diagramName: 'P activa',
    unit: 'W',
    fixed: 1,
  },
  {
    name: 'Potencia reactiva inversor',
    variable: 'inverterReactivePower',
    x: 550,
    y: 375,
    diagramName: 'P reactiva',
    unit: 'var',
    fixed: 1,
  },
  {
    name: 'Potencia aparente inversor',
    variable: 'inverterApparentPower',
    x: 550,
    y: 400,
    diagramName: 'P aparente',
    unit: 'VA',
    fixed: 1,
  },
  {
    name: 'Voltaje de salida inversor',
    variable: 'inverterOutputVoltage',
    x: 550,
    y: 425,
    diagramName: 'Voltaje',
    unit: 'Vca',
    fixed: 1,
  },
  {
    name: 'Corriente de salida inversor',
    variable: 'inverterOutputCurrent',
    x: 550,
    y: 450,
    diagramName: 'Corriente',
    unit: 'Aca',
    fixed: 1,
  },
  {
    name: 'Estado inversor',
    variable: 'inverterState',
    x: 550,
    y: 475,
    diagramName: 'Estado',
    unit: '',
    fixed: 1,
  },
  {
    name: 'Estado carga disipadora',
    variable: 'sinkLoadState',
    x: 470,
    y: 700,
    diagramName: 'Estado',
    unit: '',
    fixed: 1,
  },
  {
    name: 'Potencia carga disipadora',
    variable: 'sinkLoadPower',
    x: 470,
    y: 725,
    diagramName: 'Potencia',
    unit: 'W',
    fixed: 1,
  },
];

export const PELTON_TURBINE: InputType[] = [
  {
    disabled: true,
    value: 0.623,
    tooltip: 'Potencia nominal de la turbin',
    unit: 'kW',
    variableString: 'P',
    variableSubString: 'tn',
  },
  {
    disabled: true,
    value: 3,
    tooltip: 'Mínima cabeza de agua de operación de la turbina',
    unit: 'm',
    variableString: 'H',
    variableSubString: 'min',
  },
  {
    disabled: true,
    value: 130,
    tooltip: 'Máxima cabeza de agua de operación de la turbina',
    unit: 'm',
    variableString: 'H',
    variableSubString: 'max',
  },
  {
    disabled: true,
    value: 75,
    tooltip: 'Eficiencia de la turbina',
    unit: '%',
    variableString: 'η',
    variableSubString: 't',
  },
  {
    disabled: true,
    value: 0.0001,
    tooltip: 'Mínimo caudal de operación de la turbina',
    unit: 'm³',
    variableString: 'Q',
    variableSubString: 'min',
  },
  {
    disabled: true,
    value: 0.01,
    tooltip: 'Máximo caudal de operación de la turbina',
    unit: 'm³',
    variableString: 'Q',
    variableSubString: 'max',
  },
];

export const TURGO_TURBINE: InputType[] = [
  {
    disabled: true,
    value: 1.042,
    tooltip: 'Potencia nominal de la turbina',
    unit: 'kW',
    variableString: 'P',
    variableSubString: 'tn',
  },
  {
    disabled: true,
    value: 2,
    tooltip: 'Mínima cabeza de agua de operación de la turbina',
    unit: 'm',
    variableString: 'H',
    variableSubString: 'min',
  },
  {
    disabled: true,
    value: 30,
    tooltip: 'Máxima cabeza de agua de operación de la turbina',
    unit: 'm',
    variableString: 'H',
    variableSubString: 'max',
  },
  {
    disabled: true,
    value: 75,
    tooltip: 'Eficiencia de la turbina',
    unit: '%',
    variableString: 'η',
    variableSubString: 't',
  },
  {
    disabled: true,
    value: 0.008,
    tooltip: 'Mínimo caudal de operación de la turbina',
    unit: 'm³',
    variableString: 'Q',
    variableSubString: 'min',
  },
  {
    disabled: true,
    value: 0.016,
    tooltip: 'Máximo caudal de operación de la turbina',
    unit: 'm³',
    variableString: 'Q',
    variableSubString: 'max',
  },
];
