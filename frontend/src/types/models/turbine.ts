import { CommonGraphType } from '../graph';
import {
  BATTERY,
  Battery,
  CommonDigitalTwinsParameter,
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

export type Controller = {
  sinkLoadInitialState: ControllerStateType;
  customize: boolean;
  efficiency: InputType;
  chargeVoltageBulk: InputType;
  chargeVoltageFloat: InputType;
  chargingMinimunVoltage: InputType;
  sinkOffVoltage: InputType;
  sinkOnVoltage: InputType;
};

export type TurbineParameters = CommonSystemParameter &
  CommonDigitalTwinsParameter & {
    turbineType: TurbineType;
    controller: Controller;
    battery: Battery;
    inverterEfficiency: InputType;
    inverterNominalPower: InputType;
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

export const CONTROLLER: Controller = {
  customize: false,
  sinkLoadInitialState: ControllerStateType.Apagada,
  efficiency: {
    disabled: true,
    value: 96,
    tooltip: 'Eficiencia del controlador de carga',
    unit: '%',
    variableString: 'η',
    variableSubString: 'controller',
  },
  chargeVoltageBulk: {
    disabled: true,
    value: 27.2,
    tooltip: 'Voltaje de carga bulk',
    unit: 'V',
    variableString: 'V',
    variableSubString: 'bulk',
    min: 20,
    max: 35,
    step: 0.1,
  },
  chargeVoltageFloat: {
    disabled: true,
    value: 27.8,
    tooltip: 'Voltaje de carga flotante',
    unit: 'V',
    variableString: 'V',
    variableSubString: 'float',
    min: 20,
    max: 35,
    step: 0.1,
  },
  chargingMinimunVoltage: {
    disabled: true,
    value: 24,
    tooltip: 'Voltaje mínimo de inicio de carga',
    unit: 'V',
    variableString: 'V',
    variableSubString: 'bat_min',
    min: 24,
    max: 35,
    step: 0.1,
  },
  sinkOffVoltage: {
    disabled: true,
    value: 24.75,
    tooltip: 'Voltaje de apagado de carga disipadora',
    unit: 'V',
    variableString: 'V',
    variableSubString: 'sink_off',
    min: 24,
    max: 35,
    step: 0.1,
  },
  sinkOnVoltage: {
    disabled: true,
    value: 28,
    tooltip: 'Voltaje de encendido de carga disipadora',
    unit: 'V',
    variableString: 'V',
    variableSubString: 'sink_on',
    min: 24,
    max: 35,
    step: 0.1,
  },
};

export const TURBINE: TurbineParameters = {
  name: 'Nombre',
  timeMultiplier: {
    disabled: false,
    value: 1,
    tooltip: 'Multiplicador de tiempo',
    unit: '',
    variableString: 'TM',
    min: 1,
    max: 60,
    step: 1,
  },
  turbineType: TurbineType.Pelton,
  controller: CONTROLLER,
  battery: BATTERY,
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
  inputOfflineOperation: true,
  inputPressure: {
    disabled: false,
    value: 31,
    tooltip: 'Presión',
    unit: 'psi',
    variableString: 'Presión',
    min: 4.2,
    max: 185,
  },
  inputFlow: {
    disabled: false,
    value: 360,
    tooltip: 'Flujo',
    unit: 'L / m',
    variableString: 'Flujo',
    min: 6,
    max: 600,
  },
  inputDirectCurrentPower: false,
  inputActivePower: {
    disabled: false,
    value: 200,
    tooltip: 'Potencia activa',
    unit: 'W',
    variableString: 'Potencia activa',
    min: 0,
    max: 100000,
  },
  inputPowerFactor: {
    disabled: false,
    value: 1,
    tooltip: 'Factor de potencia',
    unit: '',
    variableString: 'Factor de potencia',
    min: -1,
    max: 1,
    step: 0.1,
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
    isShown: true,
  },
  {
    name: 'Corriente turbina',
    variable: 'turbineCurrent',
    x: 255,
    y: 85,
    diagramName: 'Corriente',
    unit: 'Acd',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Potencia turbina',
    variable: 'turbinePower',
    x: 255,
    y: 110,
    diagramName: 'Potencia',
    unit: 'W',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Voltaje corriente directa',
    variable: 'directCurrentVoltage',
    x: 130,
    y: 600,
    diagramName: 'Voltaje',
    unit: 'Vcd',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Corriente controlador',
    variable: 'controllerCurrent',
    x: 130,
    y: 625,
    diagramName: 'Corriente',
    unit: 'Acd',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Potencia controlador',
    variable: 'controllerPower',
    x: 130,
    y: 650,
    diagramName: 'Potencia',
    unit: 'W',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Estado de carga batería',
    variable: 'batteryStateOfCharge',
    x: 410,
    y: 50,
    diagramName: 'SOC',
    unit: '%',
    fixed: 3,
    isShown: true,
  },
  {
    name: 'Voltaje batería',
    variable: 'batteryVoltage',
    x: 410,
    y: 75,
    diagramName: 'Voltaje',
    unit: 'Vcd',
    fixed: 3,
    isShown: true,
  },
  {
    name: 'Corriente batería',
    variable: 'batteryCurrent',
    x: 410,
    y: 100,
    diagramName: 'Corriente',
    unit: 'Acd',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Potencia batería',
    variable: 'batteryPower',
    x: 410,
    y: 125,
    diagramName: 'Potencia',
    unit: 'W',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Temperatura batería',
    variable: 'batteryTemperature',
    x: 410,
    y: 150,
    diagramName: 'Temperatura',
    unit: '°C',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Potencia de entrada inversor',
    variable: 'inverterInputPower',
    x: 620,
    y: 75,
    diagramName: 'P entrada',
    unit: 'W',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Corriente de entrada inversor',
    variable: 'inverterInputCurrent',
    x: 620,
    y: 100,
    diagramName: 'I entrada',
    unit: 'Acd',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Potencia activa inversor',
    variable: 'inverterActivePower',
    x: 550,
    y: 350,
    diagramName: 'P activa',
    unit: 'W',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Potencia reactiva inversor',
    variable: 'inverterReactivePower',
    x: 550,
    y: 375,
    diagramName: 'P reactiva',
    unit: 'var',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Potencia aparente inversor',
    variable: 'inverterApparentPower',
    x: 550,
    y: 400,
    diagramName: 'P aparente',
    unit: 'VA',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Voltaje de salida inversor',
    variable: 'inverterOutputVoltage',
    x: 550,
    y: 425,
    diagramName: 'Voltaje',
    unit: 'Vca',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Corriente de salida inversor',
    variable: 'inverterOutputCurrent',
    x: 550,
    y: 450,
    diagramName: 'Corriente',
    unit: 'Aca',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Estado inversor',
    variable: 'inverterState',
    x: 550,
    y: 475,
    diagramName: 'Estado',
    unit: '',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Estado carga disipadora',
    variable: 'sinkLoadState',
    x: 470,
    y: 700,
    diagramName: 'Estado',
    unit: '',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Potencia carga disipadora',
    variable: 'sinkLoadPower',
    x: 470,
    y: 725,
    diagramName: 'Potencia',
    unit: 'W',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Presión turbina',
    variable: 'inputPressure',
    unit: 'W',
    isShown: false,
  },
  {
    name: 'Flujo turbina',
    variable: 'inputFlow',
    unit: 'W',
    isShown: false,
  },
  {
    name: 'Potencia activa carga',
    variable: 'inputActivePower',
    unit: 'W',
    isShown: false,
  },
  {
    name: 'Factor de potencia carga',
    variable: 'inputPowerFactor',
    unit: 'W',
    isShown: false,
  },
];

export const PELTON_TURBINE: InputType[] = [
  {
    disabled: true,
    value: 0.623,
    tooltip: 'Potencia nominal de la turbina',
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

type TurbineConsts = {
  inputPressure: InputType;
  inputFlow: InputType;
};

export const PELTON_TURBINE_CONST: TurbineConsts = {
  inputPressure: {
    disabled: false,
    value: 31,
    tooltip: 'Presión',
    unit: 'psi',
    variableString: 'Presión',
    min: 4.2,
    max: 185,
  },
  inputFlow: {
    disabled: false,
    value: 360,
    tooltip: 'Flujo',
    unit: 'L / m',
    variableString: 'Flujo',
    min: 6,
    max: 600,
  },
};

export const TURGO_TURBINE_CONST: TurbineConsts = {
  inputPressure: {
    disabled: false,
    value: 27,
    tooltip: 'Presión',
    unit: 'psi',
    variableString: 'Presión',
    min: 2.8,
    max: 43,
  },
  inputFlow: {
    disabled: false,
    value: 678,
    tooltip: 'Flujo',
    unit: 'L / m',
    variableString: 'Flujo',
    min: 480,
    max: 960,
  },
};
