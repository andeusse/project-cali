import Config from '../../config/config';
import { CommonSystemParameter, StepUnitType } from '../common';
import { CommonChartType } from '../graph';
import { InputArrayType, InputType } from '../inputType';
import { CommonDigitalTwinsParameter, DiagramVariableType } from './common';

export enum ElectronicLoadModeType {
  Current = 'Current',
  Power = 'Power',
  Resistance = 'Resistance',
}

export enum ElectronicLoadModeText {
  Current = 'Corriente constante',
  Power = 'Potencia constante',
  Resistance = 'Resistencia constante',
}

export enum LightsModeType {
  Parallel = 'Parallel',
  Series = 'Series',
}

export enum LightsModeText {
  Parallel = 'Encendido en paralelo',
  Series = 'Encendido en serie',
}

export type HydrogencellParameters = CommonSystemParameter &
  CommonDigitalTwinsParameter & {
    electronicLoadMode: ElectronicLoadModeType;
    lightsMode: LightsModeType;
    cellMaximumPower: InputType;
    cellMaximumCurrent: InputType;
    cellRatedVoltage: InputType;
    cellRatedEfficiency: InputType;
    cellRatedHydrogenPressure: InputType;
    cellRatedHydrogenFlow: InputType;
    converterMinimumVoltage: InputType;
    converterRatedPower: InputType;
    electronicLoadMaximumCurent: InputType;
    electronicLoadMaximumPower: InputType;
    lightsIndividualPower: InputType;
    cellSelfFeeding: boolean;
    lightsConnected: boolean;
    inputHydrogenFlow: InputArrayType;
    inputHydrogenPressure: InputArrayType;
    inputCellTemperature: InputArrayType;
    inputElectronicLoadCurrent: InputArrayType;
    inputElectronicLoadPower: InputArrayType;
    inputElectronicLoadResistance: InputArrayType;
    inputHydrogenFlowArray: number[];
    inputHydrogenPressureArray: number[];
    inputCellTemperatureArray: number[];
    inputElectronicLoadCurrentArray: number[];
    inputElectronicLoadPowerArray: number[];
    inputElectronicLoadResistanceArray: number[];
    simulatedCellVoltage?: number;
    simulatedGeneratedEnergy?: number;
  };

export type HydrogenCellOutput = {
  hydrogenFlow: number;
  hydrogenPressure: number;
  cellCurrent: number;
  cellVoltage: number;
  cellPower: number;
  cellTemperature: number;
  electronicLoadCurrent: number;
  electronicLoadVoltage: number;
  electronicLoadPower: number;
  cellSelfFeedingPower: number;
  lightsPower: number;
  fanPercentage: number;
  cellEfficiency: number;
  cellGeneratedEnergy: number;
  converterEfficiency: number;
};

export type HydrogenCellOutputHistoric = CommonChartType & {
  hydrogenFlow: number[];
  hydrogenPressure: number[];
  cellCurrent: number[];
  cellVoltage: number[];
  cellPower: number[];
  cellTemperature: number[];
  electronicLoadCurrent: number[];
  electronicLoadVoltage: number[];
  electronicLoadPower: number[];
  cellSelfFeedingPower: number[];
  lightsPower: number[];
  fanPercentage: number[];
  cellEfficiency: number[];
  cellGeneratedEnergy: number[];
  converterEfficiency: number[];
};

export const HYDROGEN_CELL: HydrogencellParameters = {
  inputOfflineOperation: true,
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
    min: 1,
    max: 10000,
    step: 1,
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
  cellSelfFeeding: false,
  lightsConnected: false,
  electronicLoadMode: ElectronicLoadModeType.Current,
  lightsMode: LightsModeType.Parallel,
  cellMaximumPower: {
    disabled: true,
    value: 50,
    tooltip: 'Potencia nominal de la celda',
    unit: 'W',
    variableString: 'Potencia nominal',
  },
  cellMaximumCurrent: {
    disabled: true,
    value: 4.2,
    tooltip: 'Corriente nominal de la celda',
    unit: 'A',
    variableString: 'Corriente nominal',
  },
  cellRatedVoltage: {
    disabled: true,
    value: 0,
    tooltip: 'Voltage nominal de la celda',
    unit: 'V',
    variableString: 'Voltaje de salida',
    stringValue: '12 - 18',
  },
  cellRatedEfficiency: {
    disabled: true,
    value: 48,
    tooltip: 'Eficiencia nominal de la celda',
    unit: '%',
    variableString: 'Eficiencia',
  },
  cellRatedHydrogenPressure: {
    disabled: true,
    value: 0,
    tooltip: 'Presión nominal de la celda',
    unit: 'psi',
    variableString: 'Presión de entrada',
    stringValue: '4 - 5',
  },
  cellRatedHydrogenFlow: {
    disabled: true,
    value: 0.6,
    tooltip: 'Flujo nominal de hidrógeno',
    unit: 'L/min',
    variableString: 'Flujo máximo',
  },
  converterMinimumVoltage: {
    disabled: true,
    value: 9,
    tooltip: 'Voltage mínimo del conversor',
    unit: 'V',
    variableString: 'Voltage mínimo de entrada',
  },
  converterRatedPower: {
    disabled: true,
    value: 400,
    tooltip: 'Potencia nominal del conversor',
    unit: 'W',
    variableString: 'Potencia',
  },
  electronicLoadMaximumCurent: {
    disabled: true,
    value: 40,
    tooltip: 'Corriente máxima carga electrónica',
    unit: 'A',
    variableString: 'Corriente máxima',
  },
  electronicLoadMaximumPower: {
    disabled: true,
    value: 400,
    tooltip: 'Potencia máxima carga electrónica',
    unit: 'W',
    variableString: 'Potencia máxima',
  },
  lightsIndividualPower: {
    disabled: true,
    value: 3,
    tooltip: 'Potencia individual luces',
    unit: 'W',
    variableString: 'Potencia por luminaria',
  },
  inputHydrogenFlow: {
    disabled: false,
    value: 0.4,
    tooltip: 'Fluho de hidrógeno',
    unit: 'L/min',
    variableString: 'Flujo hidrógeno',
    min: 0,
    max: 1,
    step: 1,
    arrayEnabled: false,
  },
  inputHydrogenPressure: {
    disabled: false,
    value: 5,
    tooltip: 'Presión de hidrógeno',
    unit: 'psi',
    variableString: 'Presión hidrógeno',
    min: 3,
    max: 6,
    step: 1,
    arrayEnabled: false,
  },
  inputCellTemperature: {
    disabled: false,
    value: 32,
    tooltip: 'Temperatura de la celda',
    unit: '°C',
    variableString: 'Temperatura celda',
    min: 25,
    max: 60,
    step: 1,
    arrayEnabled: false,
  },
  inputElectronicLoadCurrent: {
    disabled: false,
    value: 2,
    tooltip: 'Corriente carga electrónica',
    unit: 'A',
    variableString: 'Corriente',
    min: 0,
    max: 10,
    step: 1.0,
    arrayEnabled: false,
  },
  inputElectronicLoadPower: {
    disabled: false,
    value: 40,
    tooltip: 'Potencia carga electrónica',
    unit: 'W',
    variableString: 'Potencia',
    min: 0,
    max: 100,
    step: 1,
    arrayEnabled: false,
  },
  inputElectronicLoadResistance: {
    disabled: false,
    value: 4,
    tooltip: 'Resistencia carga electrónica',
    unit: 'Ohm',
    variableString: 'Resistencia',
    min: 2,
    max: 100,
    step: 1,
    arrayEnabled: false,
  },
  inputCellTemperatureArray: [],
  inputElectronicLoadCurrentArray: [],
  inputElectronicLoadPowerArray: [],
  inputElectronicLoadResistanceArray: [],
  inputHydrogenFlowArray: [],
  inputHydrogenPressureArray: [],
};

export const HYDROGEN_CELL_DIAGRAM_VARIABLES: DiagramVariableType[] = [
  {
    name: 'Flujo de hidrógeno',
    variable: 'hydrogenFlow',
    unit: 'L/min',
    isShown: true,
    diagramName: 'Flujo',
    fixed: 2,
    x: 2000,
    y: 1200,
  },
  {
    name: 'Presión de hidrógeno',
    variable: 'hydrogenPressure',
    unit: 'psi',
    isShown: true,
    diagramName: 'Presión',
    fixed: 2,
    x: 2000,
    y: 1350,
  },
  {
    name: 'Corriente de la celda',
    variable: 'cellCurrent',
    unit: 'A',
    isShown: true,
    diagramName: 'Corriente',
    fixed: 2,
    x: 4000,
    y: 1200,
  },
  {
    name: 'Voltaje de la celda',
    variable: 'cellVoltage',
    unit: 'V',
    isShown: true,
    diagramName: 'Voltaje',
    fixed: 3,
    x: 4000,
    y: 1350,
  },
  {
    name: 'Potencia de la celda',
    variable: 'cellPower',
    unit: 'W',
    isShown: true,
    diagramName: 'Potencia',
    fixed: 2,
    x: 4000,
    y: 1500,
  },
  {
    name: 'Temperatura de la celda',
    variable: 'cellTemperature',
    unit: '°C',
    isShown: true,
    diagramName: 'Temperatura',
    fixed: 2,
    x: 4000,
    y: 1650,
  },
  {
    name: 'Eficiencia de la celda',
    variable: 'cellEfficiency',
    unit: '%',
    isShown: true,
    diagramName: 'Eficiencia',
    fixed: 2,
    x: 4000,
    y: 1800,
  },
  {
    name: 'Energía generada de la celda',
    variable: 'cellGeneratedEnergy',
    unit: 'mWh',
    isShown: true,
    diagramName: 'Energía',
    fixed: 0,
    x: 4000,
    y: 1950,
  },
  {
    name: 'Corriente carga electrónica',
    variable: 'electronicLoadCurrent',
    unit: 'A',
    isShown: true,
    diagramName: 'Corriente',
    fixed: 2,
    x: 4300,
    y: 2600,
  },
  {
    name: 'Voltaje carga electrónica',
    variable: 'electronicLoadVoltage',
    unit: 'V',
    isShown: true,
    diagramName: 'Voltaje',
    fixed: 2,
    x: 4300,
    y: 2750,
  },
  {
    name: 'Potencia carga electrónica',
    variable: 'electronicLoadPower',
    unit: 'W',
    isShown: true,
    diagramName: 'Potencia',
    fixed: 2,
    x: 4300,
    y: 2900,
  },
  {
    name: 'Potencia de autoalimentación de la celda',
    variable: 'cellSelfFeedingPower',
    unit: 'W',
    isShown: true,
    diagramName: 'P. Autoalimentación',
    fixed: 2,
    x: 2000,
    y: 1800,
  },
  {
    name: 'Potencia de las luces',
    variable: 'lightsPower',
    unit: 'W',
    isShown: true,
    diagramName: 'P. Semáforo',
    fixed: 2,
    x: 850,
    y: 3075,
  },
  {
    name: 'Porcentaje de uso ventilador',
    variable: 'fanPercentage',
    unit: '%',
    isShown: true,
    diagramName: 'Ventilador',
    fixed: 2,
    x: 4300,
    y: 200,
    hasAdditionalCondition: 0,
  },
  {
    name: 'Eficiencia del convertidor',
    variable: 'converterEfficiency',
    unit: '%',
    isShown: true,
    diagramName: 'Eficiencia',
    fixed: 1,
    x: 2000,
    y: 3440,
  },
];
