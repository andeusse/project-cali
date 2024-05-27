import Config from '../../config/config';
import { CommonSystemParameter } from '../common';
import { CommonGraphType } from '../graph';
import { InputType } from '../inputType';
import { CommonDigitalTwinsParameter, DiagramVariableType } from './common';

export enum OperationModeType {
  Modo1 = 'Modo1',
  Modo2 = 'Modo2',
  Modo3 = 'Modo3',
  Modo4 = 'Modo4',
  Modo5 = 'Modo5',
}

export enum SpeedLawOrderType {
  Orden1 = 'Orden1',
  Orden2 = 'Orden2',
}

export enum DiagramBiogasType {
  Accumulated = 'Accumulated',
  Stored = 'Stored',
}

export enum DiagramBiogasUnitType {
  NormalVolume = 'NormalVolume',
  Pressure = 'Pressure',
}

export enum DiagramCompoundType {
  Concentration = 'Concentration',
  PartialVolume = 'PartialVolume',
  Moles = 'Moles',
}

export enum DiagramHumidityType {
  Relative = 'Relative',
  Moles = 'Moles',
}

export enum DiagramBiogasText {
  Accumulated = 'Acumulado',
  Stored = 'Almacenado',
}

export enum DiagramBiogasUnitText {
  NormalVolume = 'Volumen normal',
  Pressure = 'Presión',
}

export enum DiagramCompoundText {
  Concentration = 'Concentración',
  PartialVolume = 'Volumen parcial',
  Moles = 'Moles',
}

export enum DiagramHumidityText {
  Relative = 'Humedad relativa',
  Moles = 'Moles',
}

export type BiogasParameters = CommonSystemParameter &
  CommonDigitalTwinsParameter & {
    anaerobicReactorVolume1: InputType;
    anaerobicReactorVolume2: InputType;
    biogasTankVolume1: InputType;
    biogasTankVolume2: InputType;
    biogasTankVolume3: InputType;
    inputOperationMode: OperationModeType;
    inputSubstrateConditions: boolean;
    inputElementalAnalysisCarbonContent: InputType;
    inputElementalAnalysisHydrogenContent: InputType;
    inputElementalAnalysisOxygenContent: InputType;
    inputElementalAnalysisNitrogenContent: InputType;
    inputElementalAnalysisSulfurContent: InputType;
    inputProximateAnalysisTotalSolids: InputType;
    inputProximateAnalysisVolatileSolids: InputType;
    inputProximateAnalysisDensity: InputType;
    inputDigitalTwin: boolean;
    inputDigitalTwinStepTime: InputType;
    inputDigitalTwinTrainingTime: InputType;
    inputDigitalTwinForecastTime: InputType;
    inputKineticParameterInitialValue: InputType;
    inputSpeedLawOrder: SpeedLawOrderType;
    inputSpeedLawExponentialFactor: InputType;
    inputSpeedLawStartEnergy: InputType;
    inputPump104: boolean;
    inputPump104HydraulicRetentionTime: InputType;
    inputPump104StartTime: InputType;
    inputPump104StartsPerDay: InputType;
    inputPump102: boolean;
    inputPump102Flow: InputType;
    inputPump102StartTime: InputType;
    inputPump102StartsPerDay: InputType;
    inputPump101: boolean;
    inputPump101Flow: InputType;
    inputPump101StartTime: InputType;
    inputPump101StartsPerDay: InputType;
    inputTemperature101: InputType;
    inputTemperature102: InputType;
    diagramBiogas: DiagramBiogasType;
    diagramBiogasUnit: DiagramBiogasUnitType;
    diagramCompound: DiagramCompoundType;
    diagramHumidity: DiagramHumidityType;
  };

export type BiogasOutput = {
  K_R101: number;
  Ea_R101: number;
  Csus_exp_train_R101: number;
  x_R101: number;
  STsus_R101: number;
  Svsus_R101: number;
  FlowExit_R101: number;
  VolatileSolidsInletR101: number;
  TotalSolidsInletR101: number;
  Mwsus: number;
  n: number;
  a: number;
  b: number;
  c: number;
  d: number;
  Pump104Flow: number;
  StorageBiogasVolumeV101: number;
  AcumBiogasVolumenV101: number;
  StorageBiogasPressureV101: number;
  AcumBiogasPressureV101: number;
  StorageCH4_V101Volume: number;
  StorageCO2_V101Volume: number;
  StorageH2S_V101Volume: number;
  StorageO2_V101Volume: number;
  StorageH2_V101Volume: number;
  StorageCH4_V101Concentration: number;
  StorageCO2_V101Concentration: number;
  StorageH2S_V101Concentration: number;
  StorageO2_V101Concentration: number;
  StorageH2_V101Concentration: number;
  StorageCH4_V101moles: number;
  StorageCO2_V101moles: number;
  StorageH2S_V101moles: number;
  StorageO2_V101moles: number;
  StorageH2_V101moles: number;
  moles_humidity_V101: number;
  Relative_humidity_V101: number;
  StorageEnergy_V101: number;
  StorageBiogasVolumeV102: number;
  AcumBiogasVolumenV102: number;
  StorageBiogasPressureV102: number;
  AcumBiogasPressureV102: number;
  StorageCH4_V102Volume: number;
  StorageCO2_V102Volume: number;
  StorageH2S_V102Volume: number;
  StorageO2_V102Volume: number;
  StorageH2_V102Volume: number;
  StorageCH4_V102Concentration: number;
  StorageCO2_V102Concentration: number;
  StorageH2S_V102Concentration: number;
  StorageO2_V102Concentration: number;
  StorageH2_V102Concentration: number;
  StorageCH4_V102moles: number;
  StorageCO2_V102moles: number;
  StorageH2S_V102moles: number;
  StorageO2_V102moles: number;
  StorageH2_V102moles: number;
  moles_humidity_V102: number;
  Relative_humidity_V102: number;
  StorageEnergy_V102: number;
  StorageBiogasVolumeV107: number;
  AcumBiogasVolumenV107: number;
  StorageBiogasPressureV107: number;
  AcumBiogasPressureV107: number;
  SotrageCH4_V107Volume: number;
  StorageCO2_V107Volume: number;
  StorageH2S_V107Volume: number;
  StorageO2_V107Volume: number;
  StorageH2_V107Volume: number;
  StorageCH4_V107Concentration: number;
  StorageCO2_V107Concentration: number;
  StorageH2S_V107Concentration: number;
  StorageO2_V107Concentration: number;
  StorageH2_V107Concentration: number;
  StorageCH4_V107moles: number;
  StorageCO2_V107moles: number;
  StorageH2S_V107moles: number;
  StorageO2_V107moles: number;
  StorageH2_V107moles: number;
  moles_humidity_V107: number;
  Relative_humidity_V107: number;
  StorageEnergy_V107: number;
};

export type BiogasOutputHistoric = CommonGraphType & {};

export const BIOGAS: BiogasParameters = {
  name: 'Nombre',
  queryTime: Config.QUERY_TIME_OFFLINE,
  diagramBiogas: DiagramBiogasType.Accumulated,
  diagramBiogasUnit: DiagramBiogasUnitType.NormalVolume,
  diagramCompound: DiagramCompoundType.Concentration,
  diagramHumidity: DiagramHumidityType.Relative,
  disableParameters: false,
  timeMultiplier: {
    disabled: false,
    value: 1,
    tooltip: 'Multiplicador de tiempo',
    unit: '',
    variableString: '',

    min: 1,
    max: 10,
  },
  anaerobicReactorVolume1: {
    disabled: false,
    value: 30,
    tooltip: 'Volumen del reactor anaerobio 1',
    unit: 'L',
    variableString: 'Volumen reactor 1',

    min: 10,
    max: 30000,
  },
  anaerobicReactorVolume2: {
    disabled: false,
    value: 70,
    tooltip: 'Volumen del reactor anaerobio 2',
    unit: 'L',
    variableString: 'Volumen reactor 2',

    min: 10,
    max: 100000,
  },
  biogasTankVolume1: {
    disabled: false,
    value: 15,
    tooltip: 'Volumen tanque de biogas 1',
    unit: 'L',
    variableString: 'Volumen tanque 1',

    min: 5,
    max: 15000,
  },
  biogasTankVolume2: {
    disabled: false,
    value: 35,
    tooltip: 'Volumen tanque de biogas 2',
    unit: 'L',
    variableString: 'Volumen tanque 2',

    min: 5,
    max: 50000,
  },
  biogasTankVolume3: {
    disabled: false,
    value: 35,
    tooltip: 'Volumen tanque de biogas 3',
    unit: 'L',
    variableString: 'Volumen tanque 3',

    min: 5,
    max: 50000,
  },
  inputOfflineOperation: true,
  inputOperationMode: OperationModeType.Modo1,
  inputSubstrateConditions: true,
  inputElementalAnalysisCarbonContent: {
    disabled: false,
    value: 40.48,
    tooltip: 'Concentración de carbono atómico en el sustrato',
    unit: '%',
    variableString: 'Contenido de carbono',
    min: 0,
    max: 100,
    step: 0.01,
  },
  inputElementalAnalysisHydrogenContent: {
    disabled: false,
    value: 5.29,
    tooltip: 'Concentración de hidrógeno atómico en el sustrato',
    unit: '%',
    variableString: 'Contenido de hidrógeno',
    min: 0,
    max: 100,
    step: 0.01,
  },
  inputElementalAnalysisOxygenContent: {
    disabled: false,
    value: 29.66,
    tooltip: 'Concentración de oxígeno atómico en el sustrato',
    unit: '%',
    variableString: 'Contenido de oxígeno',
    min: 0,
    max: 100,
    step: 0.01,
  },
  inputElementalAnalysisNitrogenContent: {
    disabled: false,
    value: 1.37,
    tooltip: 'Concentración de nitrógeno atómico en el sustrato',
    unit: '%',
    variableString: 'Contenido de nitrógeno',
    min: 0,
    max: 100,
    step: 0.01,
  },
  inputElementalAnalysisSulfurContent: {
    disabled: false,
    value: 0.211,
    tooltip: 'Concentración de azúfre atómico en el sustrato',
    unit: '%',
    variableString: 'Contenido de azufre',
    min: 0,
    max: 100,
    step: 0.01,
  },
  inputProximateAnalysisTotalSolids: {
    disabled: false,
    value: 10,
    tooltip: 'Sólidos totales del sustrato',
    unit: '%',
    variableString: 'Sólidos totales',
    min: 0,
    max: 30,
  },
  inputProximateAnalysisVolatileSolids: {
    disabled: false,
    value: 1,
    tooltip: 'Sólidos volátiles del sustrato',
    unit: '%',
    variableString: 'Sólidos volátiles',
    min: 0,
    max: 10,
  },
  inputProximateAnalysisDensity: {
    disabled: false,
    value: 1000,
    tooltip: 'Densidad del sustrato',
    unit: 'g / L',
    variableString: 'Densidad',
    min: 200,
    max: 2000,
    step: 10,
  },
  inputDigitalTwin: false,
  inputDigitalTwinStepTime: {
    disabled: false,
    value: 30,
    tooltip: 'Paso de tiempo del gemelo digital',
    unit: 's',
    variableString: 'Paso de tiempo',
    min: 1,
    max: 60,
  },
  inputDigitalTwinTrainingTime: {
    disabled: true,
    value: 0.1,
    tooltip: 'Tiempo de entrenamiento del gemelo digital',
    unit: 'h',
    variableString: 'Tiempo entrenamiento',
    min: 0.1,
    max: 24,
    step: 0.1,
  },
  inputDigitalTwinForecastTime: {
    disabled: false,
    value: 1,
    tooltip: 'Tiempo de predicción del gemelo digital',
    unit: 'h',
    variableString: 'Tiempo de predicción',
    min: 0.1,
    max: 72,
    step: 0.1,
  },
  inputKineticParameterInitialValue: {
    disabled: true,
    value: 1,
    tooltip: 'Valor inicial del parámetro cinético del gemelo digital',
    unit: '',
    variableString: 'Valor inicial',
    min: 0.01,
    max: 100,
  },
  inputSpeedLawOrder: SpeedLawOrderType.Orden1,
  inputSpeedLawExponentialFactor: {
    disabled: false,
    value: 1,
    tooltip: 'Factor pre exponencial de la ley de velocidad del gemelo digital',
    unit: '',
    variableString: 'Factor pre-exponencial',
  },
  inputSpeedLawStartEnergy: {
    disabled: false,
    value: 1,
    tooltip: 'Energía de activación de la ley de velocidad del gemelo digital',
    unit: 'J / mol',
    variableString: 'Energía de activación',
  },
  inputPump104: true,
  inputPump104HydraulicRetentionTime: {
    disabled: false,
    value: 30,
    tooltip: 'Tiempo de retención hidráulico de la bomba',
    unit: 'días',
    variableString: 'TRH',
    min: 10,
    max: 100,
  },
  inputPump104StartTime: {
    disabled: false,
    value: 10,
    tooltip: 'Tiempo de encendido de la bomba',
    unit: 'min',
    variableString: 'Tiempo de encendido',
    min: 1,
    max: 60,
  },
  inputPump104StartsPerDay: {
    disabled: false,
    value: 5,
    tooltip: 'Encendidos por día de la bomba',
    unit: '',
    variableString: 'Encendido / día',
    min: 0,
    max: 20,
  },
  inputPump102: true,
  inputPump102Flow: {
    disabled: false,
    value: 0,
    tooltip: 'Caudal de la bomba',
    unit: 'LPM',
    variableString: 'Caudal',
    min: 0,
    max: 4.2,
    step: 0.01,
  },
  inputPump102StartTime: {
    disabled: false,
    value: 0,
    tooltip: 'Tiempo de encendido de la bomba',
    unit: 'min',
    variableString: 'Tiempo de encendido',
    min: 0,
    max: 1440,
  },
  inputPump102StartsPerDay: {
    disabled: false,
    value: 0,
    tooltip: 'Encendidos por día de la bomba',
    unit: '',
    variableString: 'Encendido / día',
    min: 0,
    max: 100,
  },
  inputPump101: true,
  inputPump101Flow: {
    disabled: false,
    value: 0,
    tooltip: 'Caudal de la bomba',
    unit: 'LPM',
    variableString: 'Caudal',
    min: 0,
    max: 4.2,
    step: 0.01,
  },
  inputPump101StartTime: {
    disabled: false,
    value: 0,
    tooltip: 'Tiempo de encendido de la bomba',
    unit: 'min',
    variableString: 'Tiempo de encendido',
    min: 0,
    max: 1440,
  },
  inputPump101StartsPerDay: {
    disabled: false,
    value: 0,
    tooltip: 'Encendidos por día de la bomba',
    unit: '',
    variableString: 'Encendido / día',
    min: 0,
    max: 100,
  },
  inputTemperature101: {
    disabled: false,
    value: 35,
    tooltip: 'Temperatura reactor 101',
    unit: '°C',
    variableString: 'Temperatura R-101',
    min: 15,
    max: 60,
  },
  inputTemperature102: {
    disabled: false,
    value: 35,
    tooltip: 'Temperatura reactor 102',
    unit: '°C',
    variableString: 'Temperatura R-102',
    min: 1,
    max: 10,
  },
};

export const BIOGAS_MODE1: DiagramVariableType[] = [
  {
    name: 'Parámetro cinético 1 (factor preexpoenencial)',
    variable: 'K_R101',
    unit: '1 / s',
    isShown: true,
    diagramName: 'K_R101',
    fixed: 4,
    x: 4600,
    y: 5000,
    scientificNotation: true,
  },
  {
    name: 'Parámetro cinético 2 (energía de activación)',
    variable: 'Ea_R101',
    unit: 'J / mol',
    isShown: true,
    diagramName: 'Ea_R101',
    fixed: 4,
    x: 4600,
    y: 5150,
    scientificNotation: true,
  },
  {
    name: 'Concentración sustrato a la salida de R101',
    variable: 'Csus_exp_train_R101',
    unit: 'mol / L',
    isShown: true,
    diagramName: 'C_SV',
    fixed: 4,
    x: 400,
    y: 5850,
    scientificNotation: true,
  },
  {
    name: 'Conversión del reactivo limite',
    variable: 'x_R101',
    unit: '%',
    isShown: true,
    diagramName: 'x_R101',
    fixed: 4,
    x: 4600,
    y: 5300,
    scientificNotation: false,
  },
  {
    name: 'Sólidos totales a la salida de R101',
    variable: 'STsus_R101',
    unit: '%',
    isShown: true,
    diagramName: 'ST_R101',
    fixed: 2,
    x: 400,
    y: 5550,
    scientificNotation: false,
  },
  {
    name: 'Sólidos volátiles a la salida de R101',
    variable: 'Svsus_R101',
    unit: '%',
    isShown: true,
    diagramName: 'SV_R101',
    fixed: 2,
    x: 400,
    y: 5700,
    scientificNotation: false,
  },
  {
    name: 'Salida sustrato R101',
    variable: 'FlowExit_R101',
    unit: 'L / h',
    isShown: true,
    diagramName: 'Flujo',
    fixed: 2,
    x: 400,
    y: 5400,
    scientificNotation: false,
  },
  {
    name: 'Concentración de sólidos volatiles a la entrada de R101',
    variable: 'VolatileSolidsInletR101',
    unit: 'mol / L',
    isShown: true,
    diagramName: 'C_SV',
    fixed: 4,
    x: 400,
    y: 4450,
    scientificNotation: true,
  },
  {
    name: 'Concentración de sólidos totales a la entrada de R101',
    variable: 'TotalSolidsInletR101',
    unit: 'mol / L',
    isShown: true,
    diagramName: 'C_ST',
    fixed: 4,
    x: 400,
    y: 4600,
    scientificNotation: true,
  },
  {
    name: 'Peso molecular del sustrato',
    variable: 'Mwsus',
    unit: 'g / mol',
    isShown: true,
    diagramName: 'Mwsus',
    fixed: 2,
    x: 400,
    y: 4300,
    scientificNotation: false,
  },
  {
    name: 'Subíndice de carbono en la ecuación empírica del sustrato',
    variable: 'n',
    unit: '',
    isShown: true,
    diagramName: '',
    fixed: 1,
    x: 1150,
    y: 500,
    scientificNotation: false,
  },
  {
    name: 'Subíndice de hidrógeno en la ecuación empírica del sustrato',
    variable: 'a',
    unit: '',
    isShown: true,
    diagramName: '',
    fixed: 1,
    x: 1650,
    y: 500,
    scientificNotation: false,
  },
  {
    name: 'Subíndice de oxígeno en la ecuación empírica del sustrato',
    variable: 'b',
    unit: '',
    isShown: true,
    diagramName: '',
    fixed: 1,
    x: 2150,
    y: 500,
    scientificNotation: false,
  },
  {
    name: 'Subíndice de nitrógeno en la ecuación empírica del sustrato',
    variable: 'c',
    unit: '',
    isShown: true,
    diagramName: '',
    fixed: 1,
    x: 2700,
    y: 500,
    scientificNotation: false,
  },
  {
    name: 'Subíndice de azufre en la ecuación empírica del sustrato',
    variable: 'd',
    unit: '',
    isShown: true,
    diagramName: '',
    fixed: 1,
    x: 3150,
    y: 500,
    scientificNotation: false,
  },
  {
    name: 'Flujo volumétrico de la bomba P104',
    variable: 'Pump104Flow',
    unit: 'L / h',
    isShown: true,
    diagramName: 'Flujo',
    fixed: 2,
    x: 2000,
    y: 4300,
    scientificNotation: false,
  },
  {
    name: 'Biogas Almacenado en volumen normal en el tanque V101',
    variable: 'StorageBiogasVolumeV101',
    unit: 'LN',
    isShown: true,
    diagramName: 'Volumen',
    fixed: 2,
    x: 1200,
    y: 1000,
    scientificNotation: false,
    hasAdditionalCondition: 0,
  },
  {
    name: 'Biogas Producido en volumen normal por el R101 - V101',
    variable: 'AcumBiogasVolumenV101',
    unit: 'LN',
    isShown: true,
    diagramName: 'Volumen',
    fixed: 2,
    x: 1200,
    y: 1000,
    scientificNotation: false,
    hasAdditionalCondition: 2,
  },
  {
    name: 'Presión de biogas en el tanque V101',
    variable: 'StorageBiogasPressureV101',
    unit: 'psi',
    isShown: true,
    diagramName: 'Presión',
    fixed: 2,
    x: 1200,
    y: 1000,
    scientificNotation: false,
    hasAdditionalCondition: 1,
  },
  {
    name: 'Presión de biogás acumulada en V101',
    variable: 'AcumBiogasPressureV101',
    unit: 'psi',
    isShown: true,
    diagramName: 'Presión',
    fixed: 2,
    x: 1200,
    y: 1000,
    scientificNotation: false,
    hasAdditionalCondition: 3,
  },
  {
    name: 'Metano almacenado en volumen normal en tanque V101',
    variable: 'StorageCH4_V101Volume',
    unit: 'NL',
    isShown: true,
    diagramName: 'CH4',
    fixed: 4,
    x: 1200,
    y: 1150,
    scientificNotation: false,
    hasAdditionalCondition: 6,
  },
  {
    name: 'Dióxido de carbono almacenado en volumen normal en tanque V101',
    variable: 'StorageCO2_V101Volume',
    unit: 'NL',
    isShown: true,
    diagramName: 'CO2',
    fixed: 4,
    x: 1200,
    y: 1300,
    scientificNotation: false,
    hasAdditionalCondition: 6,
  },
  {
    name: 'Sulfuro de hidrógeno almacenado en volumen normal en tanque V101',
    variable: 'StorageH2S_V101Volume',
    unit: 'NL',
    isShown: true,
    diagramName: 'H2S',
    fixed: 4,
    x: 1200,
    y: 1450,
    scientificNotation: true,
    hasAdditionalCondition: 6,
  },
  {
    name: 'Oxígeno almacenado en volumen normal en tanque V101',
    variable: 'StorageO2_V101Volume',
    unit: 'NL',
    isShown: true,
    diagramName: 'O2',
    fixed: 4,
    x: 1200,
    y: 1600,
    scientificNotation: true,
    hasAdditionalCondition: 6,
  },
  {
    name: 'Hidrógeno almacenado en volumen normal en tanque V101',
    variable: 'StorageH2_V101Volume',
    unit: 'NL',
    isShown: true,
    diagramName: 'H2',
    fixed: 4,
    x: 1200,
    y: 1750,
    scientificNotation: true,
    hasAdditionalCondition: 6,
  },
  {
    name: 'Concentración de metano almacenada en el tanque V101',
    variable: 'StorageCH4_V101Concentration',
    unit: '%',
    isShown: true,
    diagramName: 'CH4',
    fixed: 2,
    x: 1200,
    y: 1150,
    scientificNotation: false,
    hasAdditionalCondition: 4,
  },
  {
    name: 'Concentración de dióxido de carbono almacenada en el tanque V101',
    variable: 'StorageCO2_V101Concentration',
    unit: '%',
    isShown: true,
    diagramName: 'CO2',
    fixed: 2,
    x: 1200,
    y: 1300,
    scientificNotation: false,
    hasAdditionalCondition: 4,
  },
  {
    name: 'Concentración de sulfuro de hidrógeno almacenada en el tanque V101',
    variable: 'StorageH2S_V101Concentration',
    unit: 'ppm',
    isShown: true,
    diagramName: 'H2S',
    fixed: 2,
    x: 1200,
    y: 1450,
    scientificNotation: false,
    hasAdditionalCondition: 4,
  },
  {
    name: 'Concentración de oxígeno almacenado en el tanque V-101',
    variable: 'StorageO2_V101Concentration',
    unit: '%',
    isShown: true,
    diagramName: 'O2',
    fixed: 2,
    x: 1200,
    y: 1600,
    scientificNotation: false,
    hasAdditionalCondition: 4,
  },
  {
    name: 'Concentración de hidrógeno almacenado en el tanque V-101',
    variable: 'StorageH2_V101Concentration',
    unit: 'ppm',
    isShown: true,
    diagramName: 'H2',
    fixed: 2,
    x: 1200,
    y: 1750,
    scientificNotation: false,
    hasAdditionalCondition: 4,
  },
  {
    name: 'moles de metano almacenada en tanque V101',
    variable: 'StorageCH4_V101moles',
    unit: 'mol',
    isShown: true,
    diagramName: 'CH4',
    fixed: 4,
    x: 1200,
    y: 1150,
    scientificNotation: true,
    hasAdditionalCondition: 5,
  },
  {
    name: 'moles de dióxido de carbono almacenada en tanque V101',
    variable: 'StorageCO2_V101moles',
    unit: 'mol',
    isShown: true,
    diagramName: 'CO2',
    fixed: 4,
    x: 1200,
    y: 1300,
    scientificNotation: true,
    hasAdditionalCondition: 5,
  },
  {
    name: 'moles de sulfuro de hidrógeno almacenada en tanque V101',
    variable: 'StorageH2S_V101moles',
    unit: 'mol',
    isShown: true,
    diagramName: 'H2S',
    fixed: 4,
    x: 1200,
    y: 1450,
    scientificNotation: true,
    hasAdditionalCondition: 5,
  },
  {
    name: 'moles de oxígeno almacenada en tanque V101',
    variable: 'StorageO2_V101moles',
    unit: 'mol',
    isShown: true,
    diagramName: 'O2',
    fixed: 4,
    x: 1200,
    y: 1600,
    scientificNotation: true,
    hasAdditionalCondition: 5,
  },
  {
    name: 'moles de Hidrógeno almacenada en tanque V101',
    variable: 'StorageH2_V101moles',
    unit: 'mol',
    isShown: true,
    diagramName: 'H2',
    fixed: 4,
    x: 1200,
    y: 1750,
    scientificNotation: true,
    hasAdditionalCondition: 5,
  },
  {
    name: 'moles de agua en V101',
    variable: 'moles_humidity_V101',
    unit: 'mol',
    isShown: true,
    diagramName: 'H2O',
    fixed: 4,
    x: 1200,
    y: 1900,
    scientificNotation: true,
    hasAdditionalCondition: 8,
  },
  {
    name: 'Humedad Relativa del biogás en V101',
    variable: 'Relative_humidity_V101',
    unit: '%',
    isShown: true,
    diagramName: 'H2O',
    fixed: 2,
    x: 1200,
    y: 1900,
    scientificNotation: false,
    hasAdditionalCondition: 7,
  },
  {
    name: 'Energía total almacenada_V101',
    variable: 'StorageEnergy_V101',
    unit: 'Joule',
    isShown: true,
    diagramName: 'Energía',
    fixed: 4,
    x: 1200,
    y: 2050,
    scientificNotation: true,
  },
  {
    name: 'Biogas Almacenado en volumen normal en el tanque V102',
    variable: 'StorageBiogasVolumeV102',
    unit: 'LN',
    isShown: true,
    diagramName: 'Volumen',
    fixed: 2,
    x: 6200,
    y: 1000,
    scientificNotation: false,
    hasAdditionalCondition: 0,
  },
  {
    name: 'Biogas Producido en volumen normal por el R101 - V102',
    variable: 'AcumBiogasVolumenV102',
    unit: 'LN',
    isShown: true,
    diagramName: 'Volumen',
    fixed: 2,
    x: 6200,
    y: 1000,
    scientificNotation: false,
    hasAdditionalCondition: 2,
  },
  {
    name: 'Presión de biogas en el tanque V102',
    variable: 'StorageBiogasPressureV102',
    unit: 'psi',
    isShown: true,
    diagramName: 'Presión',
    fixed: 2,
    x: 6200,
    y: 1000,
    scientificNotation: false,
    hasAdditionalCondition: 1,
  },
  {
    name: 'Presión de biogás acumulada en V102',
    variable: 'AcumBiogasPressureV102',
    unit: 'psi',
    isShown: true,
    diagramName: 'Presión',
    fixed: 2,
    x: 6200,
    y: 1000,
    scientificNotation: false,
    hasAdditionalCondition: 3,
  },
  {
    name: 'Metano almacenado en volumen normal en tanque V102',
    variable: 'StorageCH4_V102Volume',
    unit: 'NL',
    isShown: true,
    diagramName: 'CH4',
    fixed: 4,
    x: 6200,
    y: 1150,
    scientificNotation: false,
    hasAdditionalCondition: 6,
  },
  {
    name: 'Dióxido de carbono almacenado en volumen normal en tanque V102',
    variable: 'StorageCO2_V102Volume',
    unit: 'NL',
    isShown: true,
    diagramName: 'CO2',
    fixed: 4,
    x: 6200,
    y: 1300,
    scientificNotation: false,
    hasAdditionalCondition: 6,
  },
  {
    name: 'Sulfuro de hidrógeno almacenado en volumen normal en tanque V102',
    variable: 'StorageH2S_V102Volume',
    unit: 'NL',
    isShown: true,
    diagramName: 'H2S',
    fixed: 4,
    x: 6200,
    y: 1450,
    scientificNotation: true,
    hasAdditionalCondition: 6,
  },
  {
    name: 'Oxígeno almacenado en volumen normal en tanque V102',
    variable: 'StorageO2_V102Volume',
    unit: 'NL',
    isShown: true,
    diagramName: 'O2',
    fixed: 4,
    x: 6200,
    y: 1600,
    scientificNotation: true,
    hasAdditionalCondition: 6,
  },
  {
    name: 'Hidrógeno almacenado en volumen normal en tanque V102',
    variable: 'StorageH2_V102Volume',
    unit: 'NL',
    isShown: true,
    diagramName: 'H2',
    fixed: 4,
    x: 6200,
    y: 1750,
    scientificNotation: true,
    hasAdditionalCondition: 6,
  },
  {
    name: 'Concentración de metano almacenada en el tanque V102',
    variable: 'StorageCH4_V102Concentration',
    unit: '%',
    isShown: true,
    diagramName: 'CH4',
    fixed: 2,
    x: 6200,
    y: 1150,
    scientificNotation: false,
    hasAdditionalCondition: 4,
  },
  {
    name: 'Concentración de dióxido de carbono almacenada en el tanque V102',
    variable: 'StorageCO2_V102Concentration',
    unit: '%',
    isShown: true,
    diagramName: 'CO2',
    fixed: 2,
    x: 6200,
    y: 1300,
    scientificNotation: false,
    hasAdditionalCondition: 4,
  },
  {
    name: 'Concentración de sulfuro de hidrógeno almacenada en el tanque V102',
    variable: 'StorageH2S_V102Concentration',
    unit: 'ppm',
    isShown: true,
    diagramName: 'H2S',
    fixed: 2,
    x: 6200,
    y: 1450,
    scientificNotation: false,
    hasAdditionalCondition: 4,
  },
  {
    name: 'Concentración de oxígeno almacenado en el tanque V-102',
    variable: 'StorageO2_V102Concentration',
    unit: '%',
    isShown: true,
    diagramName: 'O2',
    fixed: 2,
    x: 6200,
    y: 1600,
    scientificNotation: false,
    hasAdditionalCondition: 4,
  },
  {
    name: 'Concentración de hidrógeno almacenado en el tanque V-102',
    variable: 'StorageH2_V102Concentration',
    unit: 'ppm',
    isShown: true,
    diagramName: 'H2',
    fixed: 2,
    x: 6200,
    y: 1750,
    scientificNotation: false,
    hasAdditionalCondition: 4,
  },
  {
    name: 'moles de metano almacenada en tanque V102',
    variable: 'StorageCH4_V102moles',
    unit: 'mol',
    isShown: true,
    diagramName: 'CH4',
    fixed: 4,
    x: 6200,
    y: 1150,
    scientificNotation: true,
    hasAdditionalCondition: 5,
  },
  {
    name: 'moles de dióxido de carbono almacenada en tanque V102',
    variable: 'StorageCO2_V102moles',
    unit: 'mol',
    isShown: true,
    diagramName: 'CO2',
    fixed: 4,
    x: 6200,
    y: 1300,
    scientificNotation: true,
    hasAdditionalCondition: 5,
  },
  {
    name: 'moles de sulfuro de hidrógeno almacenada en tanque V102',
    variable: 'StorageH2S_V102moles',
    unit: 'mol',
    isShown: true,
    diagramName: 'H2S',
    fixed: 4,
    x: 6200,
    y: 1450,
    scientificNotation: true,
    hasAdditionalCondition: 5,
  },
  {
    name: 'moles de oxígeno almacenada en tanque V102',
    variable: 'StorageO2_V102moles',
    unit: 'mol',
    isShown: true,
    diagramName: 'O2',
    fixed: 4,
    x: 6200,
    y: 1600,
    scientificNotation: true,
    hasAdditionalCondition: 5,
  },
  {
    name: 'moles de Hidrógeno almacenada en tanque V102',
    variable: 'StorageH2_V102moles',
    unit: 'mol',
    isShown: true,
    diagramName: 'H2',
    fixed: 4,
    x: 6200,
    y: 1750,
    scientificNotation: true,
    hasAdditionalCondition: 5,
  },
  {
    name: 'moles de agua en V102',
    variable: 'moles_humidity_V102',
    unit: 'mol',
    isShown: true,
    diagramName: 'H2O',
    fixed: 4,
    x: 6200,
    y: 1900,
    scientificNotation: true,
    hasAdditionalCondition: 8,
  },
  {
    name: 'Humedad Relativa del biogás en V102',
    variable: 'Relative_humidity_V102',
    unit: '%',
    isShown: true,
    diagramName: 'H2O',
    fixed: 2,
    x: 6200,
    y: 1900,
    scientificNotation: false,
    hasAdditionalCondition: 7,
  },
  {
    name: 'Energía total almacenada_V102',
    variable: 'StorageEnergy_V102',
    unit: 'Joule',
    isShown: true,
    diagramName: 'Energía',
    fixed: 4,
    x: 6200,
    y: 2050,
    scientificNotation: true,
  },
  {
    name: 'Biogas Almacenado en volumen normal en el tanque V107',
    variable: 'StorageBiogasVolumeV107',
    unit: 'LN',
    isShown: true,
    diagramName: 'Volumen',
    fixed: 2,
    x: 6200,
    y: 4000,
    scientificNotation: false,
    hasAdditionalCondition: 0,
  },
  {
    name: 'Biogas Producido en volumen normal por el R101 - V107',
    variable: 'AcumBiogasVolumenV107',
    unit: 'LN',
    isShown: true,
    diagramName: 'Volumen',
    fixed: 2,
    x: 6200,
    y: 4000,
    scientificNotation: false,
    hasAdditionalCondition: 2,
  },
  {
    name: 'Presión de biogas en el tanque V107',
    variable: 'StorageBiogasPressureV107',
    unit: 'psi',
    isShown: true,
    diagramName: 'Presión',
    fixed: 2,
    x: 6200,
    y: 4000,
    scientificNotation: false,
    hasAdditionalCondition: 1,
  },
  {
    name: 'Presión de biogás acumulada en V107',
    variable: 'AcumBiogasPressureV107',
    unit: 'psi',
    isShown: true,
    diagramName: 'Presión',
    fixed: 2,
    x: 6200,
    y: 4000,
    scientificNotation: false,
    hasAdditionalCondition: 3,
  },
  {
    name: 'Metano almacenado en volumen normal en tanque V107',
    variable: 'SotrageCH4_V107Volume',
    unit: 'NL',
    isShown: true,
    diagramName: 'CH4',
    fixed: 4,
    x: 6200,
    y: 4150,
    scientificNotation: false,
  },
  {
    name: 'Dióxido de carbono almacenado en volumen normal en tanque V107',
    variable: 'StorageCO2_V107Volume',
    unit: 'NL',
    isShown: true,
    diagramName: 'CO2',
    fixed: 4,
    x: 6200,
    y: 4300,
    scientificNotation: false,
    hasAdditionalCondition: 6,
  },
  {
    name: 'Sulfuro de hidrógeno almacenado en volumen normal en tanque V107',
    variable: 'StorageH2S_V107Volume',
    unit: 'NL',
    isShown: true,
    diagramName: 'H2S',
    fixed: 4,
    x: 6200,
    y: 4450,
    scientificNotation: true,
    hasAdditionalCondition: 6,
  },
  {
    name: 'Oxígeno almacenado en volumen normal en tanque V107',
    variable: 'StorageO2_V107Volume',
    unit: 'NL',
    isShown: true,
    diagramName: 'O2',
    fixed: 4,
    x: 6200,
    y: 4600,
    scientificNotation: true,
    hasAdditionalCondition: 6,
  },
  {
    name: 'Hidrógeno almacenado en volumen normal en tanque V107',
    variable: 'StorageH2_V107Volume',
    unit: 'NL',
    isShown: true,
    diagramName: 'H2',
    fixed: 4,
    x: 6200,
    y: 4750,
    scientificNotation: true,
    hasAdditionalCondition: 6,
  },
  {
    name: 'Concentración de metano almacenada en el tanque V107',
    variable: 'StorageCH4_V107Concentration',
    unit: '%',
    isShown: true,
    diagramName: 'CH4',
    fixed: 2,
    x: 6200,
    y: 4150,
    scientificNotation: false,
    hasAdditionalCondition: 4,
  },
  {
    name: 'Concentración de dióxido de carbono almacenada en el tanque V107',
    variable: 'StorageCO2_V107Concentration',
    unit: '%',
    isShown: true,
    diagramName: 'CO2',
    fixed: 2,
    x: 6200,
    y: 4300,
    scientificNotation: false,
    hasAdditionalCondition: 4,
  },
  {
    name: 'Concentración de sulfuro de hidrógeno almacenada en el tanque V107',
    variable: 'StorageH2S_V107Concentration',
    unit: 'ppm',
    isShown: true,
    diagramName: 'H2S',
    fixed: 2,
    x: 6200,
    y: 4450,
    scientificNotation: false,
    hasAdditionalCondition: 4,
  },
  {
    name: 'Concentración de oxígeno almacenado en el tanque V-101',
    variable: 'StorageO2_V107Concentration',
    unit: '%',
    isShown: true,
    diagramName: 'O2',
    fixed: 2,
    x: 6200,
    y: 4600,
    scientificNotation: false,
    hasAdditionalCondition: 4,
  },
  {
    name: 'Concentración de hidrógeno almacenado en el tanque V-101',
    variable: 'StorageH2_V107Concentration',
    unit: 'ppm',
    isShown: true,
    diagramName: 'H2',
    fixed: 2,
    x: 6200,
    y: 4750,
    scientificNotation: false,
    hasAdditionalCondition: 4,
  },
  {
    name: 'moles de metano almacenada en tanque V107',
    variable: 'StorageCH4_V107moles',
    unit: 'mol',
    isShown: true,
    diagramName: 'CH4',
    fixed: 4,
    x: 6200,
    y: 4150,
    scientificNotation: true,
    hasAdditionalCondition: 5,
  },
  {
    name: 'moles de dióxido de carbono almacenada en tanque V107',
    variable: 'StorageCO2_V107moles',
    unit: 'mol',
    isShown: true,
    diagramName: 'CO2',
    fixed: 4,
    x: 6200,
    y: 4300,
    scientificNotation: true,
    hasAdditionalCondition: 5,
  },
  {
    name: 'moles de sulfuro de hidrógeno almacenada en tanque V107',
    variable: 'StorageH2S_V107moles',
    unit: 'mol',
    isShown: true,
    diagramName: 'H2S',
    fixed: 4,
    x: 6200,
    y: 4450,
    scientificNotation: true,
    hasAdditionalCondition: 5,
  },
  {
    name: 'moles de oxígeno almacenada en tanque V107',
    variable: 'StorageO2_V107moles',
    unit: 'mol',
    isShown: true,
    diagramName: 'O2',
    fixed: 4,
    x: 6200,
    y: 4600,
    scientificNotation: true,
    hasAdditionalCondition: 5,
  },
  {
    name: 'moles de Hidrógeno almacenada en tanque V107',
    variable: 'StorageH2_V107moles',
    unit: 'mol',
    isShown: true,
    diagramName: 'H2',
    fixed: 4,
    x: 6200,
    y: 4750,
    scientificNotation: true,
    hasAdditionalCondition: 5,
  },
  {
    name: 'moles de agua en V107',
    variable: 'moles_humidity_V107',
    unit: 'mol',
    isShown: true,
    diagramName: 'H2O',
    fixed: 4,
    x: 6200,
    y: 4900,
    scientificNotation: true,
    hasAdditionalCondition: 8,
  },
  {
    name: 'Humedad Relativa del biogás en V107',
    variable: 'Relative_humidity_V107',
    unit: '%',
    isShown: true,
    diagramName: 'H2O',
    fixed: 2,
    x: 6200,
    y: 4900,
    scientificNotation: false,
    hasAdditionalCondition: 7,
  },
  {
    name: 'Energía total almacenada_V107',
    variable: 'StorageEnergy_V107',
    unit: 'Joule',
    isShown: true,
    diagramName: 'Energía',
    fixed: 4,
    x: 6200,
    y: 5050,
    scientificNotation: true,
  },
];

export const BIOGAS_MODE2: DiagramVariableType[] = [
  {
    name: 'Mode2',
    variable: 'inputAlternCurrentLoadPower',
    unit: 'W',
    isShown: true,
    diagramName: 'Potencia',
    fixed: 0,
    x: 0,
    y: 0,
  },
];

export const BIOGAS_MODE3: DiagramVariableType[] = [
  {
    name: 'Mode3',
    variable: 'inputAlternCurrentLoadPower',
    unit: 'W',
    isShown: true,
    diagramName: 'Potencia',
    fixed: 0,
    x: 0,
    y: 0,
  },
];

export const BIOGAS_MODE4: DiagramVariableType[] = [
  {
    name: 'Mode4',
    variable: 'inputAlternCurrentLoadPower',
    unit: 'W',
    isShown: true,
    diagramName: 'Potencia',
    fixed: 0,
    x: 0,
    y: 0,
  },
];

export const BIOGAS_MODE5: DiagramVariableType[] = [
  {
    name: 'Mode5',
    variable: 'inputAlternCurrentLoadPower',
    unit: 'W',
    isShown: true,
    diagramName: 'Potencia',
    fixed: 0,
    x: 0,
    y: 0,
  },
];