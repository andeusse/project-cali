import Config from '../../config/config';
import { CommonGraphType } from '../graph';
import {
  Battery,
  CommonController,
  CommonDigitalTwinsParameter,
  CommonSystemParameter,
  DiagramVariableType,
  InputType,
  Inverter,
  IsConnected,
  SolarPanel,
  WindTurbine,
} from './common';

export enum OperationModeType {
  Mode1 = 'Mode1',
  Mode2 = 'Mode2',
  Mode3 = 'Mode3',
  Mode4 = 'Mode4',
  Mode5 = 'Mode5',
}

export enum OperationModeText {
  Mode1 = 'Paneles individuales',
  Mode2 = 'Paneles en serie',
  Mode3 = 'Paneles en paralelo',
  Mode4 = 'Aerogenerador',
  Mode5 = 'Paneles y aerogenerador',
}

export type SolarWindParameters = CommonSystemParameter &
  CommonDigitalTwinsParameter & {
    inputOperationMode: OperationModeType;
    monocrystallinePanel: SolarPanel;
    policrystallinePanel: SolarPanel;
    flexPanel: SolarPanel;
    cadmiumTelluridePanel: SolarPanel;
    windTurbine: WindTurbine;
    battery1: Battery;
    isBattery2: boolean;
    battery2: Battery;
    controller: IsConnected & CommonController;
    offgridInverter: Inverter;
    hybridInverter: Inverter;
    solarRadiation1: InputType;
    solarRadiation2: InputType;
    temperature: InputType;
    windSpeed: InputType;
    windDensity: InputType;
    alternCurrentLoadPower: InputType;
    alternCurrentLoadPowerFactor: InputType;
    directCurrentLoadPower: InputType;
    externalGridState: boolean;
  };

const MONOCRYSTALLINE_PANEL: SolarPanel = {
  isConnected: true,
  isConnectedDisabled: false,
  peakPower: {
    disabled: true,
    value: 100,
    tooltip: 'Potencia pico del generador solar',
    unit: 'W',
    variableString: 'Potencia pico',
  },
  deratingFactor: {
    disabled: false,
    value: 1,
    tooltip: 'Factor de reducción de la potencia',
    unit: '',
    variableString: 'f',
    variableSubString: 'pu',
    min: 0.7,
    max: 1,
    step: 0.01,
  },
  efficiency: {
    disabled: true,
    value: 15.44,
    tooltip: 'Eficiencia del panel',
    unit: '%',
    variableString: 'η',
    variableSubString: 'C',
  },
  nominalIrradiance: {
    disabled: true,
    value: 800,
    tooltip: 'Irradiancia a condiciones nominales de operación',
    unit: 'W / m²',
    variableString: 'G',
    variableSubString: 'NOCT',
  },
  testIrradiance: {
    disabled: true,
    value: 1000,
    tooltip: 'Irradiancia a condiciones estándar de prueba',
    unit: 'W / m²',
    variableString: 'G',
    variableSubString: 'STC',
  },
  nominalTemperature: {
    disabled: true,
    value: 45,
    tooltip: 'Temperatura del módulo en condiciones nominales de operación',
    unit: '°C',
    variableString: 'Tc',
    variableSubString: 'NOCT',
  },
  testTemperature: {
    disabled: true,
    value: 25,
    tooltip: 'Temperatura del módulo en condiciones estándar de prueba',
    unit: '°C',
    variableString: 'Tc',
    variableSubString: 'STC',
  },
  operatingTemperature: {
    disabled: true,
    value: 20,
    tooltip: 'Temperatura ambiente normal de operación',
    unit: '°C',
    variableString: 'Ta',
    variableSubString: 'NOCT',
  },
  temperatureVariationCoefficient: {
    disabled: true,
    value: -0.39,
    tooltip: 'Coeficiente de variación de la potencia con la temperatura',
    unit: '% / °C',
    variableString: 'μ',
    variableSubString: 'pm',
  },
};

const POLICRYSTALLINE_PANEL: SolarPanel = {
  isConnected: false,
  isConnectedDisabled: false,
  peakPower: {
    disabled: true,
    value: 100,
    tooltip: 'Potencia pico del generador solar',
    unit: 'W',
    variableString: 'Potencia pico',
  },
  deratingFactor: {
    disabled: false,
    value: 1,
    tooltip: 'Factor de reducción de la potencia',
    unit: '',
    variableString: 'f',
    variableSubString: 'pu',
    min: 0.7,
    max: 1,
    step: 0.01,
  },
  efficiency: {
    disabled: true,
    value: 15.44,
    tooltip: 'Eficiencia del panel',
    unit: '%',
    variableString: 'η',
    variableSubString: 'C',
  },
  nominalIrradiance: {
    disabled: true,
    value: 800,
    tooltip: 'Irradiancia a condiciones nominales de operación',
    unit: 'W / m²',
    variableString: 'G',
    variableSubString: 'NOCT',
  },
  testIrradiance: {
    disabled: true,
    value: 1000,
    tooltip: 'Irradiancia a condiciones estándar de prueba',
    unit: 'W / m²',
    variableString: 'G',
    variableSubString: 'STC',
  },
  nominalTemperature: {
    disabled: true,
    value: 45,
    tooltip: 'Temperatura del módulo en condiciones nominales de operación',
    unit: '°C',
    variableString: 'Tc',
    variableSubString: 'NOCT',
  },
  testTemperature: {
    disabled: true,
    value: 25,
    tooltip: 'Temperatura del módulo en condiciones estándar de prueba',
    unit: '°C',
    variableString: 'Tc',
    variableSubString: 'STC',
  },
  operatingTemperature: {
    disabled: true,
    value: 20,
    tooltip: 'Temperatura ambiente normal de operación',
    unit: '°C',
    variableString: 'Ta',
    variableSubString: 'NOCT',
  },
  temperatureVariationCoefficient: {
    disabled: true,
    value: -0.39,
    tooltip: 'Coeficiente de variación de la potencia con la temperatura',
    unit: '% / °C',
    variableString: 'μ',
    variableSubString: 'pm',
  },
};

const FLEX_PANEL: SolarPanel = {
  isConnected: false,
  isConnectedDisabled: false,
  peakPower: {
    disabled: true,
    value: 100,
    tooltip: 'Potencia pico del generador solar',
    unit: 'W',
    variableString: 'Potencia pico',
  },
  deratingFactor: {
    disabled: false,
    value: 1,
    tooltip: 'Factor de reducción de la potencia',
    unit: '',
    variableString: 'f',
    variableSubString: 'pu',
    min: 0.7,
    max: 1,
    step: 0.01,
  },
  efficiency: {
    disabled: true,
    value: 15.43,
    tooltip: 'Eficiencia del panel',
    unit: '%',
    variableString: 'η',
    variableSubString: 'C',
  },
  nominalIrradiance: {
    disabled: true,
    value: 800,
    tooltip: 'Irradiancia a condiciones nominales de operación',
    unit: 'W / m²',
    variableString: 'G',
    variableSubString: 'NOCT',
  },
  testIrradiance: {
    disabled: true,
    value: 1000,
    tooltip: 'Irradiancia a condiciones estándar de prueba',
    unit: 'W / m²',
    variableString: 'G',
    variableSubString: 'STC',
  },
  nominalTemperature: {
    disabled: true,
    value: 45,
    tooltip: 'Temperatura del módulo en condiciones nominales de operación',
    unit: '°C',
    variableString: 'Tc',
    variableSubString: 'NOCT',
  },
  testTemperature: {
    disabled: true,
    value: 25,
    tooltip: 'Temperatura del módulo en condiciones estándar de prueba',
    unit: '°C',
    variableString: 'Tc',
    variableSubString: 'STC',
  },
  operatingTemperature: {
    disabled: true,
    value: 20,
    tooltip: 'Temperatura ambiente normal de operación',
    unit: '°C',
    variableString: 'Ta',
    variableSubString: 'NOCT',
  },
  temperatureVariationCoefficient: {
    disabled: true,
    value: -0.42,
    tooltip: 'Coeficiente de variación de la potencia con la temperatura',
    unit: '% / °C',
    variableString: 'μ',
    variableSubString: 'pm',
  },
};

const CADMIUM_TELLURIDE_PANEL: SolarPanel = {
  isConnected: false,
  isConnectedDisabled: false,
  peakPower: {
    disabled: true,
    value: 77.5,
    tooltip: 'Potencia pico del generador solar',
    unit: 'W',
    variableString: 'Potencia pico',
  },
  deratingFactor: {
    disabled: false,
    value: 1,
    tooltip: 'Factor de reducción de la potencia',
    unit: '',
    variableString: 'f',
    variableSubString: 'pu',
    min: 0.7,
    max: 1,
    step: 0.01,
  },
  efficiency: {
    disabled: true,
    value: 11,
    tooltip: 'Eficiencia del panel',
    unit: '%',
    variableString: 'η',
    variableSubString: 'C',
  },
  nominalIrradiance: {
    disabled: true,
    value: 800,
    tooltip: 'Irradiancia a condiciones nominales de operación',
    unit: 'W / m²',
    variableString: 'G',
    variableSubString: 'NOCT',
  },
  testIrradiance: {
    disabled: true,
    value: 1000,
    tooltip: 'Irradiancia a condiciones estándar de prueba',
    unit: 'W / m²',
    variableString: 'G',
    variableSubString: 'STC',
  },
  nominalTemperature: {
    disabled: true,
    value: 42,
    tooltip: 'Temperatura del módulo en condiciones nominales de operación',
    unit: '°C',
    variableString: 'Tc',
    variableSubString: 'NOCT',
  },
  testTemperature: {
    disabled: true,
    value: 25,
    tooltip: 'Temperatura del módulo en condiciones estándar de prueba',
    unit: '°C',
    variableString: 'Tc',
    variableSubString: 'STC',
  },
  operatingTemperature: {
    disabled: true,
    value: 20,
    tooltip: 'Temperatura ambiente normal de operación',
    unit: '°C',
    variableString: 'Ta',
    variableSubString: 'NOCT',
  },
  temperatureVariationCoefficient: {
    disabled: true,
    value: -0.25,
    tooltip: 'Coeficiente de variación de la potencia con la temperatura',
    unit: '% / °C',
    variableString: 'μ',
    variableSubString: 'pm',
  },
};

const WIND_TURBINE: WindTurbine = {
  peakPower: {
    disabled: true,
    value: 200,
    tooltip: 'Potencia pico del aerogenerador',
    unit: 'W',
    variableString: 'Potencia pico',
  },
  rotorHeight: {
    disabled: false,
    value: 1.5,
    tooltip: 'Altura del rotor del aerogenerador',
    unit: 'm',
    variableString: 'H',
    variableSubString: 'r',
    min: 0,
    max: 10,
    step: 0.1,
  },
  anemometerHeight: {
    disabled: false,
    value: 1.5,
    tooltip: 'Altura del anemómetro',
    unit: 'm',
    variableString: 'H',
    variableSubString: 'a',
    min: 0,
    max: 10,
    step: 0.1,
  },
  ratedWindSpeed: {
    disabled: true,
    value: 11.5,
    tooltip: 'Velocidad de viento nominal',
    unit: 'm / s',
    variableString: 'V',
    variableSubString: 'n',
  },
  lowerCutoffWindSpeed: {
    disabled: true,
    value: 2,
    tooltip: 'Velocidad de viento de corte inferior',
    unit: 'm / s',
    variableString: 'V',
    variableSubString: 'f',
  },
  upperCutoffWindSpeed: {
    disabled: true,
    value: 65,
    tooltip: 'Velocidad de viento de corte superior',
    unit: 'm / s',
    variableString: 'V',
    variableSubString: 'c',
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
    value: 50,
    tooltip: 'Capacidad',
    unit: 'Ah',
    variableString: 'Capacidad',
    variableSubString: 'bat',
  },
  selfDischargeCoefficient: {
    disabled: true,
    value: 0.08,
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
    value: -0.015,
    tooltip: 'Coeficiente de compensación de temperatura',
    unit: 'V / °C',
    variableString: 'δ',
    variableSubString: 'V',
  },
};

const CONTROLLER: IsConnected & CommonController = {
  isConnected: true,
  isConnectedDisabled: false,
  customize: false,
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
    min: 10,
    max: 35,
    step: 0.1,
  },
};

const OFFGRID_INVERTER: Inverter = {
  isConnected: true,
  isConnectedDisabled: false,
  efficiency: {
    disabled: true,
    value: 90,
    tooltip: 'Eficiencia inversor',
    unit: '%',
    variableString: 'η',
    variableSubString: 'Inversor',
  },
  nominalPower: {
    disabled: true,
    value: 1500,
    tooltip: 'Potencia nominal inversor',
    unit: 'W',
    variableString: 'P',
    variableSubString: 'Inversor',
  },
};

const HYBRID_INVERTER: Inverter = {
  isConnected: false,
  isConnectedDisabled: false,
  efficiency: {
    disabled: true,
    value: 90,
    tooltip: 'Eficiencia inversor',
    unit: '%',
    variableString: 'η',
    variableSubString: 'Inversor',
  },
  nominalPower: {
    disabled: true,
    value: 1000,
    tooltip: 'Potencia nominal inversor',
    unit: 'W',
    variableString: 'P',
    variableSubString: 'Inversor',
  },
};

export type SolarWindOutput = {
  batteryTemperature: number;
  batteryVoltage: number;
  directCurrentLoadVoltage: number;
  externalGridVoltage: number;
  hybridInverterActivePower: number;
  hybridInverterApparentPower: number;
  hybridInverterOutputCurrent: number;
  hybridInverterReactivePower: number;
  hybridInverterVoltage: number;
  inverterActivePower: number;
  inverterApparentPower: number;
  inverterOutputCurrent: number;
  inverterReactivePower: number;
  inverterVoltage: number;
  solarPanelCurrent: number;
  solarPanelGeneratedEnergy: number;
  solarPanelPower: number;
  solarPanelTemperature: number;
  solarPanelVoltage: number;
  windTurbineCurrent: number;
  windTurbineGeneratedEnergy: number;
  windTurbinePower: number;
  windTurbineRevolutions: number;
  windTurbineVoltage: number;
};

export type SolarWindOutputHistoric = CommonGraphType & {
  batteryTemperature: number[];
  batteryVoltage: number[];
  directCurrentLoadVoltage: number[];
  externalGridVoltage: number[];
  hybridInverterActivePower: number[];
  hybridInverterApparentPower: number[];
  hybridInverterOutputCurrent: number[];
  hybridInverterReactivePower: number[];
  hybridInverterVoltage: number[];
  inverterActivePower: number[];
  inverterApparentPower: number[];
  inverterOutputCurrent: number[];
  inverterReactivePower: number[];
  inverterVoltage: number[];
  solarPanelCurrent: number[];
  solarPanelGeneratedEnergy: number[];
  solarPanelPower: number[];
  solarPanelTemperature: number[];
  solarPanelVoltage: number[];
  windTurbineCurrent: number[];
  windTurbineGeneratedEnergy: number[];
  windTurbinePower: number[];
  windTurbineRevolutions: number[];
  windTurbineVoltage: number[];
};

export const SOLAR_WIND: SolarWindParameters = {
  name: 'Nombre',
  queryTime: Config.QUERY_TIME_OFFLINE,
  timeMultiplier: {
    disabled: false,
    value: 1,
    tooltip: 'Multiplicador de tiempo',
    unit: '',
    variableString: '',
    min: 1,
    max: 10,
  },
  inputOfflineOperation: true,
  inputOperationMode: OperationModeType.Mode1,
  monocrystallinePanel: MONOCRYSTALLINE_PANEL,
  policrystallinePanel: POLICRYSTALLINE_PANEL,
  flexPanel: FLEX_PANEL,
  cadmiumTelluridePanel: CADMIUM_TELLURIDE_PANEL,
  windTurbine: WIND_TURBINE,
  battery1: BATTERY,
  isBattery2: false,
  battery2: BATTERY,
  controller: CONTROLLER,
  offgridInverter: OFFGRID_INVERTER,
  hybridInverter: HYBRID_INVERTER,
  solarRadiation1: {
    disabled: false,
    value: 800,
    tooltip: 'Radiación solar 1',
    unit: 'W / m²',
    variableString: 'Radiación solar 1',
    min: 0,
    max: 1500,
    step: 100,
  },
  solarRadiation2: {
    disabled: false,
    value: 800,
    tooltip: 'Radiación solar 2',
    unit: 'W / m²',
    variableString: 'Radiación solar 2',
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
  windSpeed: {
    disabled: false,
    value: 10,
    tooltip: 'Velocidad del viento',
    unit: 'm / s',
    variableString: 'Velocidad del viento',
    min: 0,
    max: 70,
  },
  windDensity: {
    disabled: false,
    value: 1.12,
    tooltip: 'Densidad del aire',
    unit: 'kg / m³',
    variableString: 'Densidad del aire',
    min: 0.8,
    max: 1.5,
    step: 0.01,
  },
  alternCurrentLoadPower: {
    disabled: false,
    value: 200,
    tooltip: 'Potencia de la carga de alterna',
    unit: 'W',
    variableString: 'Potencia',
    min: 0,
    max: 2000,
    step: 100,
  },
  alternCurrentLoadPowerFactor: {
    disabled: false,
    value: 1,
    tooltip: 'Factor de potencia de la carga de alterna',
    unit: '',
    variableString: 'Factor de potencia',
    min: -1,
    max: 1,
    step: 0.1,
  },
  directCurrentLoadPower: {
    disabled: false,
    value: 200,
    tooltip: 'Potencia de la carga de directa',
    unit: 'W',
    variableString: 'Potencia',
    min: 0,
    max: 2000,
    step: 100,
  },
  externalGridState: false,
};

export const SOLAR_WIND_DIAGRAM_VARIABLES: DiagramVariableType[] = [
  {
    name: 'Temperatura de batería',
    variable: 'batteryTemperature',
    unit: '',
    isShown: false,
    diagramName: '',
    fixed: 1,
    x: 0,
    y: 0,
  },
  {
    name: 'Voltaje de las baterías (Controlador)',
    variable: 'batteryVoltage',
    unit: '',
    isShown: false,
    diagramName: '',
    fixed: 1,
    x: 0,
    y: 0,
  },
  {
    name: 'Voltaje carga CD',
    variable: 'directCurrentLoadVoltage',
    unit: '',
    isShown: false,
    diagramName: '',
    fixed: 1,
    x: 0,
    y: 0,
  },
  {
    name: 'Voltaje de la red externa',
    variable: 'externalGridVoltage',
    unit: '',
    isShown: false,
    diagramName: '',
    fixed: 1,
    x: 0,
    y: 0,
  },
  {
    name: 'Potencia Activa salida del inversor hibrido (inversor o analizador)',
    variable: 'hybridInverterActivePower',
    unit: '',
    isShown: false,
    diagramName: '',
    fixed: 1,
    x: 0,
    y: 0,
  },
  {
    name: 'Potencia Aparente salida del inversor hibrido (inversor o analizador)',
    variable: 'hybridInverterApparentPower',
    unit: '',
    isShown: false,
    diagramName: '',
    fixed: 1,
    x: 0,
    y: 0,
  },
  {
    name: 'Corriente a la salida del inversor hibrido (inversor o analizador)',
    variable: 'hybridInverterOutputCurrent',
    unit: '',
    isShown: false,
    diagramName: '',
    fixed: 1,
    x: 0,
    y: 0,
  },
  {
    name: 'Potencia Reactiva salida del inversor hibrido (analizador)',
    variable: 'hybridInverterReactivePower',
    unit: '',
    isShown: false,
    diagramName: '',
    fixed: 1,
    x: 0,
    y: 0,
  },
  {
    name: 'Voltaje AC a la salida del inversor hibrido (inversor o analizador)',
    variable: 'hybridInverterVoltage',
    unit: '',
    isShown: false,
    diagramName: '',
    fixed: 1,
    x: 0,
    y: 0,
  },
  {
    name: 'Potencia Activa salida del inversor (inversor o analizador)',
    variable: 'inverterActivePower',
    unit: '',
    isShown: false,
    diagramName: '',
    fixed: 1,
    x: 0,
    y: 0,
  },
  {
    name: 'Potencia Aparente salida del inversor (inversor o analizador)',
    variable: 'inverterApparentPower',
    unit: '',
    isShown: false,
    diagramName: '',
    fixed: 1,
    x: 0,
    y: 0,
  },
  {
    name: 'Corriente a la salida del inversor (inversor o analizador)',
    variable: 'inverterOutputCurrent',
    unit: '',
    isShown: false,
    diagramName: '',
    fixed: 1,
    x: 0,
    y: 0,
  },
  {
    name: 'Potencia Reactiva salida del inversor (analizador)',
    variable: 'inverterReactivePower',
    unit: '',
    isShown: false,
    diagramName: '',
    fixed: 1,
    x: 0,
    y: 0,
  },
  {
    name: 'Voltaje AC a la salida del inversor (inversor o analizador)',
    variable: 'inverterVoltage',
    unit: '',
    isShown: false,
    diagramName: '',
    fixed: 1,
    x: 0,
    y: 0,
  },
  {
    name: 'Corriente paneles (pv) (Controlador)',
    variable: 'solarPanelCurrent',
    unit: '',
    isShown: false,
    diagramName: '',
    fixed: 1,
    x: 0,
    y: 0,
  },
  {
    name: 'Energía generada por paneles (kWh) (pv) (Controlador)',
    variable: 'solarPanelGeneratedEnergy',
    unit: '',
    isShown: false,
    diagramName: '',
    fixed: 1,
    x: 0,
    y: 0,
  },
  {
    name: 'Potencia paneles (pv) (Controlador)',
    variable: 'solarPanelPower',
    unit: '',
    isShown: false,
    diagramName: '',
    fixed: 1,
    x: 0,
    y: 0,
  },
  {
    name: 'Temperatura para los 4 Paneles (pv)',
    variable: 'solarPanelTemperature',
    unit: '',
    isShown: false,
    diagramName: '',
    fixed: 1,
    x: 0,
    y: 0,
  },
  {
    name: 'Voltaje paneles solares (pv) (Controlador)',
    variable: 'solarPanelVoltage',
    unit: '',
    isShown: false,
    diagramName: '',
    fixed: 1,
    x: 0,
    y: 0,
  },
  {
    name: 'Corriente Aerogenerador (fan) (Controlador)',
    variable: 'windTurbineCurrent',
    unit: '',
    isShown: false,
    diagramName: '',
    fixed: 1,
    x: 0,
    y: 0,
  },
  {
    name: 'Energía generada por aerogenerador (kWh)(fan) (Controlador)',
    variable: 'windTurbineGeneratedEnergy',
    unit: '',
    isShown: false,
    diagramName: '',
    fixed: 1,
    x: 0,
    y: 0,
  },
  {
    name: 'Potencia aerogenerador (fan)(Controlador)',
    variable: 'windTurbinePower',
    unit: '',
    isShown: false,
    diagramName: '',
    fixed: 1,
    x: 0,
    y: 0,
  },
  {
    name: 'RPMs aerogenerador (fan)',
    variable: 'windTurbineRevolutions',
    unit: '',
    isShown: false,
    diagramName: '',
    fixed: 1,
    x: 0,
    y: 0,
  },
  {
    name: 'Voltaje aerogenerador (fan) (Controlador)',
    variable: 'windTurbineVoltage',
    unit: '',
    isShown: false,
    diagramName: '',
    fixed: 1,
    x: 0,
    y: 0,
  },
];
