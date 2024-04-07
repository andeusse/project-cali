import { CommonGraphType } from '../graph';
import {
  CommonDigitalTwinsParameter,
  CommonSystemParameter,
  DiagramVariableType,
  InputType,
} from './common';

export enum OperationModeType {
  Modo1 = 'Modo1',
  Modo2 = 'Modo2',
  Modo3 = 'Modo3',
  Modo4 = 'Modo4',
}

export enum SpeedLawOrderType {
  Orden1 = 'Orden1',
  Orden2 = 'Orden2',
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
  };

export type BiogasOutput = {};

export type BiogasOutputHistoric = CommonGraphType & {};

export const BIOGAS: BiogasParameters = {
  name: 'Nombre',
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
    value: 1,
    tooltip: 'Temperatura reactor 102',
    unit: '°C',
    variableString: 'Temperatura R-102',
    min: 1,
    max: 10,
  },
};

export const BIOGAS_DIAGRAM_VARIABLES: DiagramVariableType[] = [];
