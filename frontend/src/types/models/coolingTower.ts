import Config from '../../config/config';
import { CommonSystemParameter, StepUnitType } from '../common';
import { InputType } from '../inputType';
import { CommonDigitalTwinsParameter, DiagramVariableType } from './common';

export enum FillType {
  FlatSlats = 'FlatSlats',
  CurvedSlats = 'CurvedSlats',
  Structured = 'Structured',
}

export enum FillTypeText {
  FlatSlats = 'Listones planos',
  CurvedSlats = 'Listones curvos',
  Structured = 'Estructurado',
}

export type CoolingTowerParameters = CommonSystemParameter &
  CommonDigitalTwinsParameter & {
    fillType: FillType;
    towerArea: InputType;
    towerHeight: InputType;
    nominalAirFlow: InputType;
    maximumAirPressure: InputType;
    nominalWaterFlow: InputType;
    maximumWaterPressure: InputType;
    topWaterFlow: InputType;
    topWaterTemperature: InputType;
    bottomAirFlow: InputType;
    bottomAirTemperature: InputType;
    bottomAirHumidity: InputType;
    atmosphericPressure: InputType;
  };

export type CoolingTowerOutput = {
  topWaterFlow: number;
  topWaterTemperature: number;
  topAirTemperature: number;
  topAirHumidity: number;
  airTemperatureRise: number;
  bottomWaterTemperature: number;
  waterTemperatureReduction: number;
  bottomAirFlow: number;
  bottomAirTemperature: number;
  bottomAirHumidity: number;
  energyAppliedToWater: number;
  deltaPressure: number;
};

export type CoolingTowerOutputHistoric = {
  topWaterFlow: number[];
  topWaterTemperature: number[];
  topAirTemperature: number[];
  topAirHumidity: number[];
  airTemperatureRise: number[];
  bottomWaterTemperature: number[];
  waterTemperatureReduction: number[];
  bottomAirFlow: number[];
  bottomAirTemperature: number[];
  bottomAirHumidity: number[];
  energyAppliedToWater: number[];
  deltaPressure: number[];
};

export const COOLING_TOWER: CoolingTowerParameters = {
  name: 'Nombre',
  iteration: 1,
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
    step: 0.1,
  },
  stepUnit: StepUnitType.Second,
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
  inputOfflineOperation: true,
  fillType: FillType.Structured,
  towerArea: {
    disabled: true,
    value: 0.0225,
    tooltip: 'Área transversal',
    unit: 'm²',
    variableString: 'Área transversal',
  },
  towerHeight: {
    disabled: true,
    value: 0.645,
    tooltip: 'Altura de la torre',
    unit: 'm',
    variableString: 'Altura de la torre',
  },
  nominalAirFlow: {
    disabled: true,
    value: 13.7,
    tooltip: 'Flujo nominal',
    unit: 'm³ / min',
    variableString: 'Flujo nominal',
  },
  maximumAirPressure: {
    disabled: true,
    value: 286,
    tooltip: 'Presión máxima',
    unit: 'Pa',
    variableString: 'Presión máxima',
  },
  nominalWaterFlow: {
    disabled: true,
    value: 1.9,
    tooltip: 'Flujo nominal',
    unit: 'L / min',
    variableString: 'Flujo nominal',
  },
  maximumWaterPressure: {
    disabled: true,
    value: 72.5,
    tooltip: 'Presión máxima',
    unit: 'psi',
    variableString: 'Presión máxima',
  },
  topWaterFlow: {
    disabled: false,
    value: 1.9,
    tooltip: 'Flujo',
    unit: 'L / min',
    variableString: 'Flujo',
    min: 0,
    max: 10,
    step: 0.1,
  },
  topWaterTemperature: {
    disabled: false,
    value: 50,
    tooltip: 'Temperatura',
    unit: '°C',
    variableString: 'Temperatura',
    min: 0,
    max: 100,
    step: 0.1,
  },
  bottomAirFlow: {
    disabled: false,
    value: 13.7,
    tooltip: 'Flujo',
    unit: 'm³ / min',
    variableString: 'Flujo',
    min: 0,
    max: 30,
    step: 0.1,
  },
  bottomAirTemperature: {
    disabled: false,
    value: 25,
    tooltip: 'Temperatura',
    unit: '°C',
    variableString: 'Temperatura',
    min: -20,
    max: 40,
    step: 0.1,
  },
  bottomAirHumidity: {
    disabled: false,
    value: 80,
    tooltip: 'Humedad',
    unit: '%',
    variableString: 'Humedad',
    min: 0,
    max: 100,
    step: 0.1,
  },
  atmosphericPressure: {
    disabled: false,
    value: 101.3,
    tooltip: 'Presión atmosférica',
    unit: 'kPa',
    variableString: 'Presión atmosférica',
    min: 70,
    max: 120,
    step: 0.1,
  },
};

export const CoolingTowerVariables: DiagramVariableType[] = [
  {
    name: 'Flujo Agua superior',
    variable: 'topWaterFlow',
    unit: 'L/min',
    isShown: true,
    diagramName: 'Flujo Agua',
    fixed: 2,
    x: 0,
    y: 0,
  },
  {
    name: 'Temperatura Agua superior',
    variable: 'topWaterTemperature',
    unit: '°C',
    isShown: true,
    diagramName: 'Tem. Agua',
    fixed: 2,
    x: 0,
    y: 0,
  },
  {
    name: 'Temperatura Aire',
    variable: 'topAirTemperature',
    unit: '°C',
    isShown: true,
    diagramName: 'Temp. Aire',
    fixed: 2,
    x: 0,
    y: 0,
  },
  {
    name: 'Humedad Aire',
    variable: 'topAirHumidity',
    unit: '%',
    isShown: true,
    diagramName: 'Humedad Aire',
    fixed: 2,
    x: 0,
    y: 0,
  },
  {
    name: 'Delta Humedad Aire',
    variable: 'airTemperatureRise',
    unit: '°C',
    isShown: true,
    diagramName: 'ΔTemp. Aire',
    fixed: 2,
    x: 0,
    y: 0,
  },
  {
    name: 'Humedad Agua Inferior',
    variable: 'bottomWaterTemperature',
    unit: '°C',
    isShown: true,
    diagramName: 'Tem. Agua',
    fixed: 2,
    x: 0,
    y: 0,
  },
  {
    name: 'Delta Temperatura Agua',
    variable: 'waterTemperatureReduction',
    unit: '°C',
    isShown: true,
    diagramName: 'ΔTemp. Agua',
    fixed: 2,
    x: 0,
    y: 0,
  },
  {
    name: 'Flujo Aire inferior',
    variable: 'bottomAirFlow',
    unit: 'm3/min',
    isShown: true,
    diagramName: 'Flujo Aire',
    fixed: 2,
    x: 0,
    y: 0,
  },
  {
    name: 'Temperatura Aire inferior',
    variable: 'bottomAirTemperature',
    unit: '°C',
    isShown: true,
    diagramName: 'Temp. Aire',
    fixed: 2,
    x: 0,
    y: 0,
  },
  {
    name: 'Humedad Aire inferior',
    variable: 'bottomAirHumidity',
    unit: '%',
    isShown: true,
    diagramName: 'Humedad Aire',
    fixed: 2,
    x: 0,
    y: 0,
  },
  {
    name: 'Energía aplicada al agua',
    variable: 'energyAppliedToWater',
    unit: 'kJ',
    isShown: true,
    diagramName: 'Energía aplicada',
    fixed: 2,
    x: 0,
    y: 0,
  },
  {
    name: 'Delta de presión',
    variable: 'deltaPressure',
    unit: 'Pa',
    isShown: true,
    diagramName: 'ΔPresión',
    fixed: 2,
    x: 0,
    y: 0,
  },
];