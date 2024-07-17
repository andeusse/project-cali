import Config from '../../config/config';
import { CommonSystemParameter } from '../common';
import { CommonChartType } from '../graph';
import { InputType } from '../inputType';
import {
  Battery,
  CommonController,
  CommonDigitalTwinsParameter,
  DiagramVariableType,
} from './common';

export enum TurbineType {
  Pelton = 'Pelton',
  Turgo = 'Turgo',
}

export enum ControllerStateType {
  Encendida = 'Encendida',
  Apagada = 'Apagada',
}

export enum SinkLoadModeType {
  Auto = 'Auto',
  On = 'On',
  Off = 'Off',
}

export type Controller = CommonController & {
  sinkLoadInitialState: ControllerStateType;
  sinkOffVoltage: InputType;
  sinkOnVoltage: InputType;
};

export type TurbineParameters = CommonSystemParameter &
  CommonDigitalTwinsParameter & {
    isBatteryConnected: boolean;
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
    sinkLoadMode: SinkLoadModeType;
    simulatedBatteryStateOfCharge?: number;
    simulatedDirectCurrentVoltage?: number;
    simulatedSinkLoadState?: boolean;
    simulatedInverterState?: boolean;
    simulatedChargeCycleInitialSOC?: number;
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
  batteryState: number;
  directCurrentLoadPower: number;
  directCurrentLoadVoltage: number;
  directCurrentLoadCurrent: number;
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
  chargeCycleInitialSOC?: number;
};

export type TurbineOutputHistoric = CommonChartType & {
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
  batteryState: number[];
  directCurrentLoadPower: number[];
  directCurrentLoadVoltage: number[];
  directCurrentLoadCurrent: number[];
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

const CONTROLLER: Controller = {
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
    value: 23,
    tooltip: 'Voltaje mínimo de inicio de carga',
    unit: 'V',
    variableString: 'V',
    variableSubString: 'bat_min',
    min: 15,
    max: 35,
    step: 0.1,
  },
  sinkOffVoltage: {
    disabled: true,
    value: 24,
    tooltip: 'Voltaje de apagado de carga disipadora',
    unit: 'V',
    variableString: 'V',
    variableSubString: 'sink_off',
    min: 22,
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

const BATTERY: Battery = {
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
    unit: '% / mes',
    variableString: 'σ',
    variableSubString: 'bat',
  },
  chargeDischargeEfficiency: {
    disabled: true,
    value: 98,
    tooltip: 'Eficiencia de carga y descarga',
    unit: '%',
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

export const PELTON_TURBINE_CONST: TurbineConsts = {
  inputPressure: {
    disabled: false,
    value: 22,
    tooltip: 'Presión',
    unit: 'mH₂O',
    variableString: 'Presión',
    min: 0,
    max: 30,
  },
  inputFlow: {
    disabled: false,
    value: 6,
    tooltip: 'Flujo',
    unit: 'L / s',
    variableString: 'Flujo',
    min: 0,
    max: 15,
  },
};

export const TURGO_TURBINE_CONST: TurbineConsts = {
  inputPressure: {
    disabled: false,
    value: 19,
    tooltip: 'Presión',
    unit: 'mH₂O',
    variableString: 'Presión',
    min: 0,
    max: 30,
  },
  inputFlow: {
    disabled: false,
    value: 11,
    tooltip: 'Flujo',
    unit: 'L / s',
    variableString: 'Flujo',
    min: 0,
    max: 20,
  },
};

export const TURBINE: TurbineParameters = {
  name: 'Nombre',
  isBatteryConnected: true,
  queryTime: Config.QUERY_TIME_OFFLINE,
  disableParameters: false,
  timeMultiplier: {
    disabled: false,
    value: 1,
    tooltip: 'Multiplicador de tiempo',
    unit: '',
    variableString: 'TM',
    min: 1,
    max: 60,
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
    value: 1500,
    tooltip: 'Potencia nominal',
    unit: 'W',
    variableString: 'P',
    variableSubString: 'inverter',
  },
  inputOfflineOperation: true,
  inputDirectCurrentPower: false,
  inputActivePower: {
    disabled: false,
    value: 200,
    tooltip: 'Potencia activa',
    unit: 'W',
    variableString: 'Potencia activa',
    min: 0,
    max: 100000,
    step: 10,
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
  sinkLoadMode: SinkLoadModeType.Auto,
  ...PELTON_TURBINE_CONST,
};

export const PELTON_TURBINE_DIAGRAM_VARIABLES: DiagramVariableType[] = [
  {
    name: 'Potencia turbina',
    variable: 'turbinePower',
    x: 20,
    y: 580,
    diagramName: 'Potencia',
    unit: 'W',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Voltaje turbina',
    variable: 'turbineVoltage',
    x: 20,
    y: 660,
    diagramName: 'Voltaje',
    unit: 'Vcd',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Corriente turbina',
    variable: 'turbineCurrent',
    x: 20,
    y: 740,
    diagramName: 'Corriente',
    unit: 'Acd',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Potencia controlador',
    variable: 'controllerPower',
    x: 2040,
    y: 320,
    diagramName: 'Potencia',
    unit: 'W',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Voltaje corriente directa',
    variable: 'directCurrentVoltage',
    x: 2040,
    y: 400,
    diagramName: 'Voltaje',
    unit: 'Vcd',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Corriente controlador',
    variable: 'controllerCurrent',
    x: 2040,
    y: 480,
    diagramName: 'Corriente',
    unit: 'Acd',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Eficiencia controlador',
    variable: 'controllerEfficiency',
    x: 2040,
    y: 560,
    diagramName: 'Eficiencia',
    unit: '%',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Estado de carga batería',
    variable: 'batteryStateOfCharge',
    x: 2580,
    y: 1460,
    diagramName: 'SOC',
    unit: '%',
    fixed: 3,
    isShown: true,
  },
  {
    name: 'Potencia batería',
    variable: 'batteryPower',
    x: 2580,
    y: 1540,
    diagramName: 'Potencia',
    unit: 'W',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Voltaje batería',
    variable: 'batteryVoltage',
    x: 2580,
    y: 1620,
    diagramName: 'Voltaje',
    unit: 'Vcd',
    fixed: 3,
    isShown: true,
  },
  {
    name: 'Corriente batería',
    variable: 'batteryCurrent',
    x: 2580,
    y: 1700,
    diagramName: 'Corriente',
    unit: 'Acd',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Estado batería',
    variable: 'batteryState',
    x: 2580,
    y: 1780,
    diagramName: 'Estado',
    unit: '',
    fixed: 0,
    isShown: true,
  },
  {
    name: 'Temperatura batería',
    variable: 'batteryTemperature',
    x: 2580,
    y: 1860,
    diagramName: 'Temperatura',
    unit: '°C',
    fixed: 1,
    isShown: true,
    hasAdditionalCondition: 0,
  },
  {
    name: 'Potencia de entrada inversor',
    variable: 'inverterInputPower',
    x: 3600,
    y: 480,
    diagramName: 'P. entrada',
    unit: 'W',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Corriente de entrada inversor',
    variable: 'inverterInputCurrent',
    x: 3600,
    y: 560,
    diagramName: 'I. entrada',
    unit: 'Acd',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Estado inversor',
    variable: 'inverterState',
    x: 3600,
    y: 640,
    diagramName: 'Estado',
    unit: '',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Eficiencia inversor',
    variable: 'inverterEfficiency',
    x: 3600,
    y: 720,
    diagramName: 'Eficiencia',
    unit: '%',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Potencia aparente inversor',
    variable: 'inverterApparentPower',
    x: 3600,
    y: 1000,
    diagramName: 'P. aparente',
    unit: 'VA',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Potencia activa inversor',
    variable: 'inverterActivePower',
    x: 3600,
    y: 1080,
    diagramName: 'P. activa',
    unit: 'W',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Potencia reactiva inversor',
    variable: 'inverterReactivePower',
    x: 3600,
    y: 1160,
    diagramName: 'P. reactiva',
    unit: 'var',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Voltaje de salida inversor',
    variable: 'inverterOutputVoltage',
    x: 3600,
    y: 1240,
    diagramName: 'Voltaje',
    unit: 'Vca',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Corriente de salida inversor',
    variable: 'inverterOutputCurrent',
    x: 3600,
    y: 1320,
    diagramName: 'Corriente',
    unit: 'Aca',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Potencia activa carga',
    variable: 'inputActivePower',
    x: 3600,
    y: 1700,
    diagramName: 'Potencia',
    unit: 'W',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Factor de potencia carga',
    variable: 'inputPowerFactor',
    x: 3600,
    y: 1780,
    diagramName: 'FP',
    unit: '',
    fixed: 2,
    isShown: true,
  },
  {
    name: 'Estado carga disipadora',
    variable: 'sinkLoadState',
    x: 600,
    y: 1150,
    diagramName: 'Estado',
    unit: '',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Potencia carga disipadora',
    variable: 'sinkLoadPower',
    x: 600,
    y: 1230,
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
];

export const TURGO_TURBINE_DIAGRAM_VARIABLES: DiagramVariableType[] = [
  {
    name: 'Potencia turbina',
    variable: 'turbinePower',
    x: 20,
    y: 1700,
    diagramName: 'Potencia',
    unit: 'W',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Voltaje turbina',
    variable: 'turbineVoltage',
    x: 20,
    y: 1780,
    diagramName: 'Voltaje',
    unit: 'Vcd',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Corriente turbina',
    variable: 'turbineCurrent',
    x: 20,
    y: 1860,
    diagramName: 'Corriente',
    unit: 'Acd',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Potencia controlador',
    variable: 'controllerPower',
    x: 960,
    y: 2000,
    diagramName: 'Potencia',
    unit: 'W',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Voltaje corriente directa',
    variable: 'directCurrentVoltage',
    x: 960,
    y: 2080,
    diagramName: 'Voltaje',
    unit: 'Vcd',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Corriente controlador',
    variable: 'controllerCurrent',
    x: 960,
    y: 2160,
    diagramName: 'Corriente',
    unit: 'Acd',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Eficiencia controlador',
    variable: 'controllerEfficiency',
    x: 960,
    y: 2240,
    diagramName: 'Eficiencia',
    unit: '%',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Estado de carga batería',
    variable: 'batteryStateOfCharge',
    x: 2580,
    y: 1460,
    diagramName: 'SOC',
    unit: '%',
    fixed: 3,
    isShown: true,
  },
  {
    name: 'Potencia batería',
    variable: 'batteryPower',
    x: 2580,
    y: 1540,
    diagramName: 'Potencia',
    unit: 'W',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Voltaje batería',
    variable: 'batteryVoltage',
    x: 2580,
    y: 1620,
    diagramName: 'Voltaje',
    unit: 'Vcd',
    fixed: 3,
    isShown: true,
  },
  {
    name: 'Corriente batería',
    variable: 'batteryCurrent',
    x: 2580,
    y: 1700,
    diagramName: 'Corriente',
    unit: 'Acd',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Estado batería',
    variable: 'batteryState',
    x: 2580,
    y: 1780,
    diagramName: 'Estado',
    unit: '',
    fixed: 0,
    isShown: true,
  },
  {
    name: 'Temperatura batería',
    variable: 'batteryTemperature',
    x: 2580,
    y: 1860,
    diagramName: 'Temperatura',
    unit: '°C',
    fixed: 1,
    isShown: true,
    hasAdditionalCondition: 0,
  },
  {
    name: 'Potencia carga CD',
    variable: 'directCurrentLoadPower',
    x: 2360,
    y: 2080,
    diagramName: 'Potencia',
    unit: 'W',
    fixed: 1,
    isShown: true,
    hasAdditionalCondition: 1,
  },
  {
    name: 'Voltaje carga CD',
    variable: 'directCurrentLoadVoltage',
    x: 2360,
    y: 2160,
    diagramName: 'Voltaje',
    unit: 'V',
    fixed: 1,
    isShown: true,
    hasAdditionalCondition: 1,
  },
  {
    name: 'Corriente carga CD',
    variable: 'directCurrentLoadCurrent',
    x: 2360,
    y: 2240,
    diagramName: 'Corriente',
    unit: 'mA',
    fixed: 1,
    isShown: true,
    hasAdditionalCondition: 1,
  },
  {
    name: 'Potencia de entrada inversor',
    variable: 'inverterInputPower',
    x: 3600,
    y: 480,
    diagramName: 'P. entrada',
    unit: 'W',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Corriente de entrada inversor',
    variable: 'inverterInputCurrent',
    x: 3600,
    y: 560,
    diagramName: 'I. entrada',
    unit: 'Acd',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Estado inversor',
    variable: 'inverterState',
    x: 3600,
    y: 640,
    diagramName: 'Estado',
    unit: '',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Eficiencia inversor',
    variable: 'inverterEfficiency',
    x: 3600,
    y: 720,
    diagramName: 'Eficiencia',
    unit: '%',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Potencia aparente inversor',
    variable: 'inverterApparentPower',
    x: 3600,
    y: 1000,
    diagramName: 'P. aparente',
    unit: 'VA',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Potencia activa inversor',
    variable: 'inverterActivePower',
    x: 3600,
    y: 1080,
    diagramName: 'P. activa',
    unit: 'W',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Potencia reactiva inversor',
    variable: 'inverterReactivePower',
    x: 3600,
    y: 1160,
    diagramName: 'P. reactiva',
    unit: 'var',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Voltaje de salida inversor',
    variable: 'inverterOutputVoltage',
    x: 3600,
    y: 1240,
    diagramName: 'Voltaje',
    unit: 'Vca',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Corriente de salida inversor',
    variable: 'inverterOutputCurrent',
    x: 3600,
    y: 1320,
    diagramName: 'Corriente',
    unit: 'Aca',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Potencia activa carga',
    variable: 'inputActivePower',
    x: 3600,
    y: 1700,
    diagramName: 'Potencia',
    unit: 'W',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Factor de potencia carga',
    variable: 'inputPowerFactor',
    x: 3600,
    y: 1780,
    diagramName: 'FP',
    unit: '',
    fixed: 2,
    isShown: true,
  },
  {
    name: 'Estado carga disipadora',
    variable: 'sinkLoadState',
    x: 600,
    y: 1150,
    diagramName: 'Estado',
    unit: '',
    fixed: 1,
    isShown: true,
  },
  {
    name: 'Potencia carga disipadora',
    variable: 'sinkLoadPower',
    x: 600,
    y: 1230,
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
];

export const PELTON_TURBINE: InputType[] = [
  {
    disabled: true,
    value: 623,
    tooltip: 'Potencia nominal de la turbina',
    unit: 'W',
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
    value: 55,
    tooltip: 'Eficiencia de la turbina',
    unit: '%',
    variableString: 'η',
    variableSubString: 't',
  },
  {
    disabled: true,
    value: 0.1,
    tooltip: 'Mínimo caudal de operación de la turbina',
    unit: 'L / s',
    variableString: 'Q',
    variableSubString: 'min',
  },
  {
    disabled: true,
    value: 10,
    tooltip: 'Máximo caudal de operación de la turbina',
    unit: 'L / s',
    variableString: 'Q',
    variableSubString: 'max',
  },
];

export const TURGO_TURBINE: InputType[] = [
  {
    disabled: true,
    value: 1042,
    tooltip: 'Potencia nominal de la turbina',
    unit: 'W',
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
    value: 45,
    tooltip: 'Eficiencia de la turbina',
    unit: '%',
    variableString: 'η',
    variableSubString: 't',
  },
  {
    disabled: true,
    value: 8,
    tooltip: 'Mínimo caudal de operación de la turbina',
    unit: 'L / s',
    variableString: 'Q',
    variableSubString: 'min',
  },
  {
    disabled: true,
    value: 16,
    tooltip: 'Máximo caudal de operación de la turbina',
    unit: 'L / s',
    variableString: 'Q',
    variableSubString: 'max',
  },
];

type TurbineConsts = {
  inputPressure: InputType;
  inputFlow: InputType;
};
