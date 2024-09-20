import {
  CommonSystemParameter,
  OperationModelType,
  StepUnitType,
} from '../common';
import { CommonDigitalTwinsParameter, DiagramVariableType } from './common';
import { CommonChartType } from '../graph';
import Config from '../../config/config';
import { InputType } from '../inputType';

export enum PlantOperationType {
  SideA = 'SideA',
  SideB = 'SideB',
}

export enum PlantOperationText {
  SideA = 'Lado A',
  SideB = 'Lado B',
}

export enum MixRuleType {
  Fraction = 'Fraction',
  Volume = 'Volume',
  Weight = 'Weight',
}

export enum MixRuleText {
  Fraction = 'Fracción',
  Volume = 'Volumen',
  Weight = 'Peso',
}

export enum DosageType {
  Time = 'Time',
  Injection = 'Injection',
  NoDosing = 'NoDosing',
}

export enum DosageText {
  Time = 'Tiempo',
  Injection = 'Por inyecciones',
  NoDosing = 'Sin dosificación',
}

export enum DiagramBiogasType {
  Accumulated = 'Accumulated',
  Stored = 'Stored',
}

export enum DiagramBiogasText {
  Accumulated = 'Acumulado',
  Stored = 'Almacenado',
}

export enum DiagramBiogasUnitType {
  NormalVolume = 'NormalVolume',
  Pressure = 'Pressure',
}

export enum DiagramBiogasUnitText {
  NormalVolume = 'Volumen normal',
  Pressure = 'Presión',
}

export enum DiagramCompoundUnitType {
  Concentration = 'Concentration',
  NormalVolume = 'PartialVolume',
  Moles = 'Moles',
}

export enum DiagramCompoundUnitText {
  Concentration = 'Concentración',
  NormalVolume = 'Volumen normal',
  Moles = 'Moles',
}

export enum DiagramBiogasMeasurementMethodType {
  Pressure = 'Pressure',
  VolumeDisplaced = 'VolumeDisplaced',
}

export enum DiagramBiogasMeasurementMethodText {
  Pressure = 'Presión',
  VolumeDisplaced = 'Volumen desplazado',
}

export type BiochemicalMethanePotentialParameters = CommonSystemParameter &
  CommonDigitalTwinsParameter & {
    plantOperation: PlantOperationType;
    measurementMethodSideA: DiagramBiogasMeasurementMethodType;
    modelSelectionSideA: OperationModelType;
    mixRuleSideA: MixRuleType;
    dosificationTypeSideA: DosageType;
    biogasVisualizationSideA: DiagramBiogasType;
    biogasVisualizationUnitsSideA: DiagramBiogasUnitType;
    biogasCompoundsSideA: DiagramCompoundUnitType;
    measurementMethodSideB: DiagramBiogasMeasurementMethodType;
    modelSelectionSideB: OperationModelType;
    mixRuleSideB: MixRuleType;
    dosificationTypeSideB: DosageType;
    biogasVisualizationSideB: DiagramBiogasType;
    biogasVisualizationUnitsSideB: DiagramBiogasUnitType;
    biogasCompoundsSideB: DiagramCompoundUnitType;

    rxnVolumeSideA: InputType;
    freeVolumeSideA: InputType;
    stateSelectionSideA: boolean;
    timeStepSideA: InputType;
    kineticKSideA: InputType;
    kineticEaSideA: InputType;
    kineticLambdaSideA: InputType;
    amountOfSubstratesSideA: InputType;
    nameSubstrate1SideA: string;
    substrate1CompositionSideA: InputType;
    totalSolidsSubstrate1SideA: InputType;
    volatileSolidsSubstrate1SIdeA: InputType;
    densitySubstrate1SideA: InputType;
    carbonContentSubstrate1SideA: InputType;
    hydrogenContentSubstrate1SideA: InputType;
    oxygenContentSubstrate1SideA: InputType;
    nitrogenContentSubstrate1SideA: InputType;
    sulfurContentSubstrate1SideA: InputType;
    nameSubstrate2SideA: string;
    substrate2CompositionSideA: InputType;
    totalSolidsSubstrate2SideA: InputType;
    volatileSolidsSubstrate2SideA: InputType;
    densitySubstrate2SideA: InputType;
    carbonContentSubstrate2SideA: InputType;
    hydrogenContentSubstrate2SideA: InputType;
    oxygenContentSubstrate2SideA: InputType;
    nitrogenContentSubstrate2SideA: InputType;
    sulfurContentSubstrate2SideA: InputType;
    nameSubstrate3SideA: string;
    substrate3CompositionSideA: InputType;
    totalSolidsSubstrate3SideA: InputType;
    volatileSolidsSubstrate3SideA: InputType;
    densitySubstrate3SideA: InputType;
    carbonContentSubstrate3SideA: InputType;
    hydrogenContentSubstrate3SideA: InputType;
    oxygenContentSubstrate3SideA: InputType;
    nitrogenContentSubstrate3SideA: InputType;
    sulfurContentSubstrate3SideA: InputType;
    nameSubstrate4SideA: string;
    substrate4CompositionSideA: InputType;
    totalSolidsSubstrate4SideA: InputType;
    volatileSolidsSubstrate4SIdeA: InputType;
    densitySubstrate4SideA: InputType;
    carbonContentSubstrate4SideA: InputType;
    hydrogenContentSubstrate4SideA: InputType;
    oxygenContentSubstrate4SideA: InputType;
    nitrogenContentSubstrate4SideA: InputType;
    sulfurContentSubstrate4SideA: InputType;
    waterCompositionSideA: InputType;
    manualBiogasCompositionSideA: boolean;
    methaneR101: InputType;
    carbonDioxideR101: InputType;
    oxygenR101: InputType;
    sulfurHydrogenR101: InputType;
    hydrogenR101: InputType;
    methaneR102: InputType;
    carbonDioxideR102: InputType;
    oxygenR102: InputType;
    sulfurHydrogenR102: InputType;
    hydrogenR102: InputType;
    methaneR103: InputType;
    carbonDioxideR103: InputType;
    oxygenR103: InputType;
    sulfurHydrogenR103: InputType;
    hydrogenR103: InputType;
    methaneR104: InputType;
    carbonDioxideR104: InputType;
    oxygenR104: InputType;
    sulfurHydrogenR104: InputType;
    hydrogenR104: InputType;
    methaneR105: InputType;
    carbonDioxideR105: InputType;
    oxygenR105: InputType;
    sulfurHydrogenR105: InputType;
    hydrogenR105: InputType;
    testDurationSideA: InputType;
    TemperatureSideA: InputType;
    pHSideA: InputType;
    mixManualSideA: boolean;
    mixVelocitySideA: InputType;
    mixTimeSideA: InputType;
    mixDailySideA: InputType;
    feefManualSideA: boolean;
    dosificationVolumeSideA: InputType;
    dailyInyectionsByTimeSideA: InputType;
    dailyInyectionsSideA: InputType;

    rxnVolumeSideB: InputType;
    freeVolumeSideB: InputType;
    stateSelectionSideB: boolean;
    timeStepSideB: InputType;
    kineticKSideB: InputType;
    kineticEaSideB: InputType;
    kineticLambdaSideB: InputType;
    amountOfSubstratesSideB: InputType;
    nameSubstrate1SideB: string;
    substrate1CompositionSideB: InputType;
    totalSolidsSubstrate1SideB: InputType;
    volatileSolidsSubstrate1SideB: InputType;
    densitySubstrate1SideB: InputType;
    carbonContentSubstrate1SideB: InputType;
    hydrogenContentSubstrate1SideB: InputType;
    oxygenContentSubstrate1SideB: InputType;
    nitrogenContentSubstrate1SideB: InputType;
    sulfurContentSubstrate1SideB: InputType;
    nameSubstrate2SideB: string;
    substrate2CompositionSideB: InputType;
    totalSolidsSubstrate2SideB: InputType;
    volatileSolidsSubstrate2SideB: InputType;
    densitySubstrate2SideB: InputType;
    carbonContentSubstrate2SideB: InputType;
    hydrogenContentSubstrate2SideB: InputType;
    oxygenContentSubstrate2SideB: InputType;
    nitrogenContentSubstrate2SideB: InputType;
    sulfurContentSubstrate2SideB: InputType;
    nameSubstrate3SideB: string;
    substrate3CompositionSideB: InputType;
    totalSolidsSubstrate3SideB: InputType;
    volatileSolidsSubstrate3SideB: InputType;
    densitySubstrate3SideB: InputType;
    carbonContentSubstrate3SideB: InputType;
    hydrogenContentSubstrate3SideB: InputType;
    oxygenContentSubstrate3SideB: InputType;
    nitrogenContentSubstrate3SideB: InputType;
    sulfurContentSubstrate3SideB: InputType;
    nameSubstrate4SideB: string;
    substrate4CompositionSideB: InputType;
    totalSolidsSubstrate4SideB: InputType;
    volatileSolidsSubstrate4SideB: InputType;
    densitySubstrate4SideB: InputType;
    carbonContentSubstrate4SideB: InputType;
    hydrogenContentSubstrate4SideB: InputType;
    oxygenContentSubstrate4SideB: InputType;
    nitrogenContentSubstrate4SideB: InputType;
    sulfurContentSubstrate4SideB: InputType;
    waterCompositionSideB: InputType;
    manualBiogasCompositionSideB: boolean;
    methaneR106: InputType;
    carbonDioxideR106: InputType;
    oxygenR106: InputType;
    sulfurHydrogenR106: InputType;
    hydrogenR106: InputType;
    methaneR107: InputType;
    carbonDioxideR107: InputType;
    oxygenR107: InputType;
    sulfurHydrogenR107: InputType;
    hydrogenR107: InputType;
    methaneR108: InputType;
    carbonDioxideR108: InputType;
    oxygenR108: InputType;
    sulfurHydrogenR108: InputType;
    hydrogenR108: InputType;
    methaneR109: InputType;
    carbonDioxideR109: InputType;
    oxygenR109: InputType;
    sulfurHydrogenR109: InputType;
    hydrogenR109: InputType;
    methaneR110: InputType;
    carbonDioxideR110: InputType;
    oxygenR110: InputType;
    sulfurHydrogenR110: InputType;
    hydrogenR110: InputType;
    testDurationSideB: InputType;
    TemperatureSideB: InputType;
    pHSideB: InputType;
    mixManualSideB: boolean;
    mixVelocitySideB: InputType;
    mixTimeSideB: InputType;
    mixDailySideB: InputType;
    feefManualSideB: boolean;
    dosificationVolumeSideB: InputType;
    dailyInyectionsByTimeSideB: InputType;
    dailyInyectionsSideB: InputType;
  };

export type BiochemicalMethanePotentialOutput = {
  TempR101: number;
  pHR101: number;
  SVR101: number;
  OCR101: number;
  STR101: number;
  KR101: number;
  EaR101: number;
  lambdaR101: number;
  TempR102: number;
  pHR102: number;
  SVR102: number;
  OCR102: number;
  STR102: number;
  KR102: number;
  EaR102: number;
  lambdaR102: number;
  TempR103: number;
  pHR103: number;
  SVR103: number;
  OCR103: number;
  STR103: number;
  KR103: number;
  EaR103: number;
  lambdaR103: number;
  TempR104: number;
  pHR104: number;
  SVR104: number;
  OCR104: number;
  STR104: number;
  KR104: number;
  EaR104: number;
  lambdaR104: number;
  TempR105: number;
  pHR105: number;
  SVR105: number;
  OCR105: number;
  STR105: number;
  KR105: number;
  EaR105: number;
  lambdaR105: number;
  caudalSideA: number;
  volumeSubstrateSideA: number;
  LHVR101: number;
  EnergyR101: number;
  PBMR101: number;
  mixVelocityR101: number;
  LHVR102: number;
  EnergyR102: number;
  PBMR102: number;
  mixVelocityR102: number;
  LHVR103: number;
  EnergyR103: number;
  PBMR103: number;
  mixVelocityR103: number;
  LHVR104: number;
  EnergyR104: number;
  PBMR104: number;
  mixVelocityR104: number;
  LHVR105: number;
  EnergyR105: number;
  PBMR105: number;
  mixVelocityR105: number;
  poolLevelR101: number;
  poolTempR101: number;
  poolPressureR101: number;
  poolLevelR102: number;
  poolTempR102: number;
  poolPressureR102: number;
  poolLevelR103: number;
  poolTempR103: number;
  poolPressureR103: number;
  poolLevelR104: number;
  poolTempR104: number;
  poolPressureR104: number;
  poolLevelR105: number;
  poolTempR105: number;
  poolPressureR105: number;
  TempR106: number;
  pHR106: number;
  SVR106: number;
  OCR106: number;
  STR106: number;
  KR106: number;
  EaR106: number;
  lambdaR106: number;
  TempR107: number;
  pHR107: number;
  SVR107: number;
  OCR107: number;
  STR107: number;
  KR107: number;
  EaR107: number;
  lambdaR107: number;
  TempR108: number;
  pHR108: number;
  SVR108: number;
  OCR108: number;
  STR108: number;
  KR108: number;
  EaR108: number;
  lambdaR108: number;
  TempR109: number;
  pHR109: number;
  SVR109: number;
  OCR109: number;
  STR109: number;
  KR109: number;
  EaR109: number;
  lambdaR109: number;
  TempR110: number;
  pHR110: number;
  SVR110: number;
  OCR110: number;
  STR110: number;
  KR110: number;
  EaR110: number;
  lambdaR110: number;
  caudalsideB: number;
  volumeSubstratesideB: number;
  LHVR106: number;
  EnergyR106: number;
  PBMR106: number;
  mixVelocityR106: number;
  LHVR107: number;
  EnergyR107: number;
  PBMR107: number;
  mixVelocityR107: number;
  LHVR108: number;
  EnergyR108: number;
  PBMR108: number;
  mixVelocityR108: number;
  LHVR109: number;
  EnergyR109: number;
  PBMR109: number;
  mixVelocityR109: number;
  LHVR110: number;
  EnergyR110: number;
  PBMR110: number;
  mixVelocityR110: number;
  poolLevelR106: number;
  poolTempR106: number;
  poolPressureR106: number;
  poolLevelR107: number;
  poolTempR107: number;
  poolPressureR107: number;
  poolLevelR108: number;
  poolTempR108: number;
  poolPressureR108: number;
  poolLevelR109: number;
  poolTempR109: number;
  poolPressureR109: number;
  poolLevelR110: number;
  poolTempR110: number;
  poolPressureR110: number;
};

export type BiochemicalMethanePotentialOutputHistoric = CommonChartType & {
  TempR101: number[];
  pHR101: number[];
  SVR101: number[];
  OCR101: number[];
  STR101: number[];
  KR101: number[];
  EaR101: number[];
  lambdaR101: number[];
  TempR102: number[];
  pHR102: number[];
  SVR102: number[];
  OCR102: number[];
  STR102: number[];
  KR102: number[];
  EaR102: number[];
  lambdaR102: number[];
  TempR103: number[];
  pHR103: number[];
  SVR103: number[];
  OCR103: number[];
  STR103: number[];
  KR103: number[];
  EaR103: number[];
  lambdaR103: number[];
  TempR104: number[];
  pHR104: number[];
  SVR104: number[];
  OCR104: number[];
  STR104: number[];
  KR104: number[];
  EaR104: number[];
  lambdaR104: number[];
  TempR105: number[];
  pHR105: number[];
  SVR105: number[];
  OCR105: number[];
  STR105: number[];
  KR105: number[];
  EaR105: number[];
  lambdaR105: number[];
  caudalSideA: number[];
  volumeSubstrateSideA: number[];
  LHVR101: number[];
  EnergyR101: number[];
  PBMR101: number[];
  mixVelocityR101: number[];
  LHVR102: number[];
  EnergyR102: number[];
  PBMR102: number[];
  mixVelocityR102: number[];
  LHVR103: number[];
  EnergyR103: number[];
  PBMR103: number[];
  mixVelocityR103: number[];
  LHVR104: number[];
  EnergyR104: number[];
  PBMR104: number[];
  mixVelocityR104: number[];
  LHVR105: number[];
  EnergyR105: number[];
  PBMR105: number[];
  mixVelocityR105: number[];
  poolLevelR101: number[];
  poolTempR101: number[];
  poolPressureR101: number[];
  poolLevelR102: number[];
  poolTempR102: number[];
  poolPressureR102: number[];
  poolLevelR103: number[];
  poolTempR103: number[];
  poolPressureR103: number[];
  poolLevelR104: number[];
  poolTempR104: number[];
  poolPressureR104: number[];
  poolLevelR105: number[];
  poolTempR105: number[];
  poolPressureR105: number[];
  TempR106: number[];
  pHR106: number[];
  SVR106: number[];
  OCR106: number[];
  STR106: number[];
  KR106: number[];
  EaR106: number[];
  lambdaR106: number[];
  TempR107: number[];
  pHR107: number[];
  SVR107: number[];
  OCR107: number[];
  STR107: number[];
  KR107: number[];
  EaR107: number[];
  lambdaR107: number[];
  TempR108: number[];
  pHR108: number[];
  SVR108: number[];
  OCR108: number[];
  STR108: number[];
  KR108: number[];
  EaR108: number[];
  lambdaR108: number[];
  TempR109: number[];
  pHR109: number[];
  SVR109: number[];
  OCR109: number[];
  STR109: number[];
  KR109: number[];
  EaR109: number[];
  lambdaR109: number[];
  TempR110: number[];
  pHR110: number[];
  SVR110: number[];
  OCR110: number[];
  STR110: number[];
  KR110: number[];
  EaR110: number[];
  lambdaR110: number[];
  caudalsideB: number[];
  volumeSubstratesideB: number[];
  LHVR106: number[];
  EnergyR106: number[];
  PBMR106: number[];
  mixVelocityR106: number[];
  LHVR107: number[];
  EnergyR107: number[];
  PBMR107: number[];
  mixVelocityR107: number[];
  LHVR108: number[];
  EnergyR108: number[];
  PBMR108: number[];
  mixVelocityR108: number[];
  LHVR109: number[];
  EnergyR109: number[];
  PBMR109: number[];
  mixVelocityR109: number[];
  LHVR110: number[];
  EnergyR110: number[];
  PBMR110: number[];
  mixVelocityR110: number[];
  poolLevelR106: number[];
  poolTempR106: number[];
  poolPressureR106: number[];
  poolLevelR107: number[];
  poolTempR107: number[];
  poolPressureR107: number[];
  poolLevelR108: number[];
  poolTempR108: number[];
  poolPressureR108: number[];
  poolLevelR109: number[];
  poolTempR109: number[];
  poolPressureR109: number[];
  poolLevelR110: number[];
  poolTempR110: number[];
  poolPressureR110: number[];
};

export const BMP: BiochemicalMethanePotentialParameters = {
  name: 'Nombre',
  iteration: 1,
  steps: {
    disabled: false,
    value: 24,
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
  stepUnit: StepUnitType.Hour,
  queryTime: Config.QUERY_TIME_DIGITAL_TWIN_OFF_OFFLINE_BIOGAS,
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
  inputOfflineOperation: true,
  plantOperation: PlantOperationType.SideA,
  measurementMethodSideA: DiagramBiogasMeasurementMethodType.Pressure,
  modelSelectionSideA: OperationModelType.Arrhenius,
  mixRuleSideA: MixRuleType.Fraction,
  dosificationTypeSideA: DosageType.Time,
  biogasVisualizationSideA: DiagramBiogasType.Stored,
  biogasVisualizationUnitsSideA: DiagramBiogasUnitType.NormalVolume,
  biogasCompoundsSideA: DiagramCompoundUnitType.Concentration,
  measurementMethodSideB: DiagramBiogasMeasurementMethodType.Pressure,
  modelSelectionSideB: OperationModelType.Arrhenius,
  mixRuleSideB: MixRuleType.Fraction,
  dosificationTypeSideB: DosageType.Time,
  biogasVisualizationSideB: DiagramBiogasType.Stored,
  biogasVisualizationUnitsSideB: DiagramBiogasUnitType.NormalVolume,
  biogasCompoundsSideB: DiagramCompoundUnitType.Concentration,
  stateSelectionSideA: true,
  manualBiogasCompositionSideA: true,
  mixManualSideA: true,
  feefManualSideA: true,
  stateSelectionSideB: true,
  manualBiogasCompositionSideB: true,
  mixManualSideB: true,
  feefManualSideB: true,
  nameSubstrate1SideA: '',
  nameSubstrate2SideA: '',
  nameSubstrate3SideA: '',
  nameSubstrate4SideA: '',
  nameSubstrate1SideB: '',
  nameSubstrate2SideB: '',
  nameSubstrate3SideB: '',
  nameSubstrate4SideB: '',
  rxnVolumeSideA: {
    disabled: false,
    value: 750,
    tooltip: 'Volumen de reacción',
    unit: 'mL',
    variableString: 'Volumen reactores',
    min: 100,
    max: 2000,
  },
  freeVolumeSideA: {
    disabled: false,
    value: 750,
    tooltip: 'Volumen libre',
    unit: 'mL',
    variableString: 'Volumen libre reactores',
    min: 100,
    max: 2000,
  },
  timeStepSideA: {
    disabled: false,
    value: 1,
    tooltip: 'paso del tiempo',
    unit: 's',
    variableString: 'Paso de tiempo',
    min: 1,
    max: 3600,
  },
  kineticKSideA: {
    disabled: false,
    value: 100,
    tooltip: 'Factor pre-exponencia',
    unit: 'L/s',
    variableString: 'K',
  },
  kineticEaSideA: {
    disabled: false,
    value: 1000000,
    tooltip: 'Energía de activación',
    unit: 'J/mol',
    variableString: 'Ea',
  },
  kineticLambdaSideA: {
    disabled: true,
    value: -44928,
    tooltip: 'Tiempo de retraso',
    unit: 's',
    variableString: 'λ',
  },
  amountOfSubstratesSideA: {
    disabled: false,
    value: 1,
    tooltip: 'Numero de sustratos',
    unit: '',
    variableString: 'Número de sustratos',
    min: 1,
    max: 4,
  },
  substrate1CompositionSideA: {
    disabled: false,
    value: 0,
    tooltip: 'Fracción, volumen o peso',
    unit: '%',
    variableString: 'Fracción',
    min: 0,
    max: 100,
  },
  totalSolidsSubstrate1SideA: {
    disabled: false,
    value: 10,
    tooltip: 'Sóldios Totales [%]',
    unit: '%',
    variableString: 'Sólidos Totales',
    min: 0,
    max: 100,
  },
  volatileSolidsSubstrate1SIdeA: {
    disabled: false,
    value: 5,
    tooltip: 'Sólidos Volátiles[%]',
    unit: '%',
    variableString: 'Sólidos Volátiles',
    min: 0,
    max: 100,
  },
  densitySubstrate1SideA: {
    disabled: false,
    value: 500,
    tooltip: 'Densidad seco[g/L]',
    unit: 'g/L',
    variableString: 'densidad seco',
    min: 0,
  },
  carbonContentSubstrate1SideA: {
    disabled: false,
    value: 43,
    tooltip: 'Contenido de carbono [%]',
    unit: '%',
    variableString: 'contenido carbono',
    min: 0,
    max: 100,
  },
  hydrogenContentSubstrate1SideA: {
    disabled: false,
    value: 5,
    tooltip: 'Contenido de Hidrógeno [%]',
    unit: '%',
    variableString: 'contenido hidrógeno',
    min: 0,
    max: 100,
  },
  oxygenContentSubstrate1SideA: {
    disabled: false,
    value: 30,
    tooltip: 'Contenido de oxígeno [%]',
    unit: '%',
    variableString: 'contenido oxígeno',
    min: 0,
    max: 100,
  },
  nitrogenContentSubstrate1SideA: {
    disabled: false,
    value: 2,
    tooltip: 'Contenido de nitrógeno [%]',
    unit: '%',
    variableString: 'contenido nitrógeno',
    min: 0,
    max: 100,
  },
  sulfurContentSubstrate1SideA: {
    disabled: false,
    value: 0.21,
    tooltip: 'Contenido de azufre [%]',
    unit: '%',
    variableString: 'contenido azufre',
    min: 0,
    max: 100,
  },
  substrate2CompositionSideA: {
    disabled: false,
    value: 0,
    tooltip: 'Fracción, volumen o peso',
    unit: '%',
    variableString: 'Fracción',
    min: 0,
    max: 100,
  },
  totalSolidsSubstrate2SideA: {
    disabled: false,
    value: 10,
    tooltip: 'Sóldios Totales [%]',
    unit: '%',
    variableString: 'Sólidos Totales',
    min: 0,
    max: 100,
  },
  volatileSolidsSubstrate2SideA: {
    disabled: false,
    value: 5,
    tooltip: 'Sólidos Volátiles[%]',
    unit: '%',
    variableString: 'Sólidos Volátiles',
    min: 0,
    max: 100,
  },
  densitySubstrate2SideA: {
    disabled: false,
    value: 500,
    tooltip: 'densidad seco[g/L]',
    unit: 'g/L',
    variableString: 'densidad seco',
    min: 0,
  },
  carbonContentSubstrate2SideA: {
    disabled: false,
    value: 43,
    tooltip: 'Contenido de carbono [%]',
    unit: '%',
    variableString: 'contenido carbono',
    min: 0,
    max: 100,
  },
  hydrogenContentSubstrate2SideA: {
    disabled: false,
    value: 5,
    tooltip: 'Contenido de Hidrógeno [%]',
    unit: '%',
    variableString: 'contenido hidrógeno',
    min: 0,
    max: 100,
  },
  oxygenContentSubstrate2SideA: {
    disabled: false,
    value: 30,
    tooltip: 'Contenido de oxígeno [%]',
    unit: '%',
    variableString: 'contenido oxígeno',
    min: 0,
    max: 100,
  },
  nitrogenContentSubstrate2SideA: {
    disabled: false,
    value: 2,
    tooltip: 'Contenido de nitrógeno [%]',
    unit: '%',
    variableString: 'contenido nitrógeno',
    min: 0,
    max: 100,
  },
  sulfurContentSubstrate2SideA: {
    disabled: false,
    value: 0.21,
    tooltip: 'Contenido de azufre [%]',
    unit: '%',
    variableString: 'contenido azufre',
    min: 0,
    max: 100,
  },
  substrate3CompositionSideA: {
    disabled: false,
    value: 0,
    tooltip: 'Fracción, volumen o peso',
    unit: '%',
    variableString: 'Fracción',
    min: 0,
    max: 100,
  },
  totalSolidsSubstrate3SideA: {
    disabled: false,
    value: 10,
    tooltip: 'Sóldios Totales [%]',
    unit: '%',
    variableString: 'Sólidos Totales',
    min: 0,
    max: 100,
  },
  volatileSolidsSubstrate3SideA: {
    disabled: false,
    value: 5,
    tooltip: 'Sólidos Volátiles[%]',
    unit: '%',
    variableString: 'Sólidos Volátiles',
    min: 0,
    max: 100,
  },
  densitySubstrate3SideA: {
    disabled: false,
    value: 500,
    tooltip: 'densidad seco[g/L]',
    unit: 'g/L',
    variableString: 'densidad seco',
    min: 0,
  },
  carbonContentSubstrate3SideA: {
    disabled: false,
    value: 43,
    tooltip: 'Contenido de carbono [%]',
    unit: '%',
    variableString: 'contenido carbono',
    min: 0,
    max: 100,
  },
  hydrogenContentSubstrate3SideA: {
    disabled: false,
    value: 5,
    tooltip: 'Contenido de Hidrógeno [%]',
    unit: '%',
    variableString: 'contenido hidrógeno',
    min: 0,
    max: 100,
  },
  oxygenContentSubstrate3SideA: {
    disabled: false,
    value: 30,
    tooltip: 'Contenido de oxígeno [%]',
    unit: '%',
    variableString: 'contenido oxígeno',
    min: 0,
    max: 100,
  },
  nitrogenContentSubstrate3SideA: {
    disabled: false,
    value: 2,
    tooltip: 'Contenido de nitrógeno [%]',
    unit: '%',
    variableString: 'contenido nitrógeno',
    min: 0,
    max: 100,
  },
  sulfurContentSubstrate3SideA: {
    disabled: false,
    value: 0.21,
    tooltip: 'Contenido de azufre [%]',
    unit: '%',
    variableString: 'contenido azufre',
    min: 0,
    max: 100,
  },
  substrate4CompositionSideA: {
    disabled: false,
    value: 0,
    tooltip: 'Fracción, volumen o peso',
    unit: '%',
    variableString: 'Fracción',
    min: 0,
    max: 100,
  },
  totalSolidsSubstrate4SideA: {
    disabled: false,
    value: 10,
    tooltip: 'Sóldios Totales [%]',
    unit: '%',
    variableString: 'Sólidos Totales',
    min: 0,
    max: 100,
  },
  volatileSolidsSubstrate4SIdeA: {
    disabled: false,
    value: 5,
    tooltip: 'Sólidos Volátiles[%]',
    unit: '%',
    variableString: 'Sólidos Volátiles',
    min: 0,
    max: 100,
  },
  densitySubstrate4SideA: {
    disabled: false,
    value: 500,
    tooltip: 'densidad seco[g/L]',
    unit: 'g/L',
    variableString: 'densidad seco',
    min: 0,
  },
  carbonContentSubstrate4SideA: {
    disabled: false,
    value: 43,
    tooltip: 'Contenido de carbono [%]',
    unit: '%',
    variableString: 'contenido carbono',
    min: 0,
    max: 100,
  },
  hydrogenContentSubstrate4SideA: {
    disabled: false,
    value: 5,
    tooltip: 'Contenido de Hidrógeno [%]',
    unit: '%',
    variableString: 'contenido hidrógeno',
    min: 0,
    max: 100,
  },
  oxygenContentSubstrate4SideA: {
    disabled: false,
    value: 30,
    tooltip: 'Contenido de oxígeno [%]',
    unit: '%',
    variableString: 'contenido oxígeno',
    min: 0,
    max: 100,
  },
  nitrogenContentSubstrate4SideA: {
    disabled: false,
    value: 2,
    tooltip: 'Contenido de nitrógeno [%]',
    unit: '%',
    variableString: 'contenido nitrógeno',
    min: 0,
    max: 100,
  },
  sulfurContentSubstrate4SideA: {
    disabled: false,
    value: 0.21,
    tooltip: 'Contenido de azufre [%]',
    unit: '%',
    variableString: 'contenido azufre',
    min: 0,
    max: 100,
  },
  waterCompositionSideA: {
    disabled: false,
    value: 80,
    tooltip: 'Fracción de agua [%]',
    unit: '%',
    variableString: 'Fracción de agua',
    min: 0,
    max: 100,
  },
  methaneR101: {
    disabled: false,
    value: 55,
    tooltip: 'Composición de metano R101 [%]',
    unit: '%',
    variableString: 'CH4',
    min: 0,
    max: 100,
  },
  carbonDioxideR101: {
    disabled: false,
    value: 30,
    tooltip: 'Composición de dióxido de carbono R101 [%]',
    unit: '%',
    variableString: 'CO2',
    min: 0,
    max: 100,
  },
  oxygenR101: {
    disabled: false,
    value: 10,
    tooltip: 'Composición de oxígeno R101 [%]',
    unit: '%',
    variableString: 'O2',
    min: 0,
    max: 100,
  },
  sulfurHydrogenR101: {
    disabled: false,
    value: 100,
    tooltip: 'Composición de sulfuro de hidrógeno R101 [ppm]',
    unit: 'ppm',
    variableString: 'H2S',
    min: 0,
    max: 2000,
  },
  hydrogenR101: {
    disabled: false,
    value: 10,
    tooltip: 'Composición de hidrógeno R101 [ppm] ',
    unit: 'ppm',
    variableString: 'H2',
    min: 0,
    max: 2000,
  },
  methaneR102: {
    disabled: false,
    value: 55,
    tooltip: 'Composición de metano R102 [%]',
    unit: '%',
    variableString: 'CH4',
    min: 0,
    max: 100,
  },
  carbonDioxideR102: {
    disabled: false,
    value: 30,
    tooltip: 'Composición de dióxido de carbono R102 [%]',
    unit: '%',
    variableString: 'CO2',
    min: 0,
    max: 100,
  },
  oxygenR102: {
    disabled: false,
    value: 10,
    tooltip: 'Composición de oxígeno R102 [%]',
    unit: '%',
    variableString: 'O2',
    min: 0,
    max: 100,
  },
  sulfurHydrogenR102: {
    disabled: false,
    value: 100,
    tooltip: 'Composición de sulfuro de hidrógeno R102 [ppm]',
    unit: 'ppm',
    variableString: 'H2S',
    min: 0,
    max: 2000,
  },
  hydrogenR102: {
    disabled: false,
    value: 10,
    tooltip: 'Composición de hidrógeno R102 [ppm] ',
    unit: 'ppm',
    variableString: 'H2',
    min: 0,
    max: 2000,
  },
  methaneR103: {
    disabled: false,
    value: 55,
    tooltip: 'Composición de metano R103 [%]',
    unit: '%',
    variableString: 'CH4',
    min: 0,
    max: 100,
  },
  carbonDioxideR103: {
    disabled: false,
    value: 30,
    tooltip: 'Composición de dióxido de carbono R103 [%]',
    unit: '%',
    variableString: 'CO2',
    min: 0,
    max: 100,
  },
  oxygenR103: {
    disabled: false,
    value: 10,
    tooltip: 'Composición de oxígeno R103 [%]',
    unit: '%',
    variableString: 'O2',
    min: 0,
    max: 100,
  },
  sulfurHydrogenR103: {
    disabled: false,
    value: 100,
    tooltip: 'Composición de sulfuro de hidrógeno R103 [ppm]',
    unit: 'ppm',
    variableString: 'H2S',
    min: 0,
    max: 2000,
  },
  hydrogenR103: {
    disabled: false,
    value: 10,
    tooltip: 'Composición de hidrógeno R103 [ppm] ',
    unit: 'ppm',
    variableString: 'H2',
    min: 0,
    max: 2000,
  },
  methaneR104: {
    disabled: false,
    value: 55,
    tooltip: 'Composición de metano R104 [%]',
    unit: '%',
    variableString: 'CH4',
    min: 0,
    max: 100,
  },
  carbonDioxideR104: {
    disabled: false,
    value: 30,
    tooltip: 'Composición de dióxido de carbono R104 [%]',
    unit: '%',
    variableString: 'CO2',
    min: 0,
    max: 100,
  },
  oxygenR104: {
    disabled: false,
    value: 10,
    tooltip: 'Composición de oxígeno R104 [%]',
    unit: '%',
    variableString: 'O2',
    min: 0,
    max: 100,
  },
  sulfurHydrogenR104: {
    disabled: false,
    value: 100,
    tooltip: 'Composición de sulfuro de hidrógeno R104 [ppm]',
    unit: 'ppm',
    variableString: 'H2S',
    min: 0,
    max: 2000,
  },
  hydrogenR104: {
    disabled: false,
    value: 10,
    tooltip: 'Composición de hidrógeno R104 [ppm] ',
    unit: 'ppm',
    variableString: 'H2',
    min: 0,
    max: 2000,
  },
  methaneR105: {
    disabled: false,
    value: 55,
    tooltip: 'Composición de metano R105 [%]',
    unit: '%',
    variableString: 'CH4',
    min: 0,
    max: 100,
  },
  carbonDioxideR105: {
    disabled: false,
    value: 30,
    tooltip: 'Composición de dióxido de carbono R105 [%]',
    unit: '%',
    variableString: 'CO2',
    min: 0,
    max: 100,
  },
  oxygenR105: {
    disabled: false,
    value: 10,
    tooltip: 'Composición de oxígeno R105 [%]',
    unit: '%',
    variableString: 'O2',
    min: 0,
    max: 100,
  },
  sulfurHydrogenR105: {
    disabled: false,
    value: 100,
    tooltip: 'Composición de sulfuro de hidrógeno R105 [ppm]',
    unit: 'ppm',
    variableString: 'H2S',
    min: 0,
    max: 2000,
  },
  hydrogenR105: {
    disabled: false,
    value: 10,
    tooltip: 'Composición de hidrógeno R105 [ppm] ',
    unit: 'ppm',
    variableString: 'H2',
    min: 0,
    max: 2000,
  },
  testDurationSideA: {
    disabled: false,
    value: 30,
    tooltip: 'Duración de la prueba [días]',
    unit: 'dias',
    variableString: 'Duración de la prueba',
    min: 0,
  },
  TemperatureSideA: {
    disabled: false,
    value: 35,
    tooltip: 'Temperatura Lado A [°c]',
    unit: '°c',
    variableString: 'Temperatura',
    min: 25,
    max: 65,
  },
  pHSideA: {
    disabled: false,
    value: 7,
    tooltip: 'pH',
    unit: '',
    variableString: 'pH',
    min: 0,
    max: 14,
  },
  mixVelocitySideA: {
    disabled: false,
    value: 50,
    tooltip: 'Velocidad de agitación [RPM]',
    unit: 'RPM',
    variableString: 'Velocidad de agitación',
    min: 0,
    max: 300,
  },
  mixTimeSideA: {
    disabled: false,
    value: 30,
    tooltip: 'Tiempo de Agitación [min]',
    unit: 'min',
    variableString: 'Tiempo de agitación',
    min: 0,
    max: 60,
  },
  mixDailySideA: {
    disabled: false,
    value: 10,
    tooltip: 'Agitaciones diarias',
    unit: '',
    variableString: 'Agitaciones diarias',
    min: 0,
    max: 24,
  },
  dosificationVolumeSideA: {
    disabled: false,
    value: 50,
    tooltip: 'Volumen',
    unit: 'mL',
    variableString: 'Volumen',
    min: 0,
    max: 1000,
  },
  dailyInyectionsByTimeSideA: {
    disabled: false,
    value: 4,
    tooltip: 'Tiempo',
    unit: 'horas',
    variableString: 'Tiempo',
    min: 0,
    max: 24,
  },
  dailyInyectionsSideA: {
    disabled: false,
    value: 4,
    tooltip: 'Inyecciones diarias',
    unit: '',
    variableString: 'Inyecciones diarias',
    min: 4,
    max: 12,
  },
  rxnVolumeSideB: {
    disabled: false,
    value: 750,
    tooltip: 'Volumen de reacción',
    unit: 'mL',
    variableString: 'Volumen reactores',
    min: 100,
    max: 2000,
  },
  freeVolumeSideB: {
    disabled: false,
    value: 750,
    tooltip: 'Volumen libre',
    unit: 'mL',
    variableString: 'Volumen libre reactores',
    min: 100,
    max: 2000,
  },
  timeStepSideB: {
    disabled: false,
    value: 1,
    tooltip: 'paso del tiempo',
    unit: 's',
    variableString: 'Paso de tiempo',
    min: 1,
    max: 3600,
  },
  kineticKSideB: {
    disabled: false,
    value: 100,
    tooltip: 'Factor pre-exponencia',
    unit: 'L/s',
    variableString: 'K',
  },
  kineticEaSideB: {
    disabled: false,
    value: 1000000,
    tooltip: 'Energía de activación',
    unit: 'J/mol',
    variableString: 'Ea',
  },
  kineticLambdaSideB: {
    disabled: true,
    value: -44928,
    tooltip: 'Tiempo de retraso',
    unit: 's',
    variableString: 'λ',
  },
  amountOfSubstratesSideB: {
    disabled: false,
    value: 1,
    tooltip: 'Numero de sustratos',
    unit: '',
    variableString: 'Número de sustratos',
    min: 1,
    max: 4,
  },
  substrate1CompositionSideB: {
    disabled: false,
    value: 0,
    tooltip: 'composición, volume o peso',
    unit: '%',
    variableString: 'Composición',
    min: 0,
    max: 100,
  },
  totalSolidsSubstrate1SideB: {
    disabled: false,
    value: 10,
    tooltip: 'Sóldios Totales [%]',
    unit: '%',
    variableString: 'Sólidos Totales',
    min: 0,
    max: 100,
  },
  volatileSolidsSubstrate1SideB: {
    disabled: false,
    value: 5,
    tooltip: 'Sólidos Volátiles[%]',
    unit: '%',
    variableString: 'Sólidos Volátiles',
    min: 0,
    max: 100,
  },
  densitySubstrate1SideB: {
    disabled: false,
    value: 500,
    tooltip: 'densidad seco[g/L]',
    unit: 'g/L',
    variableString: 'densidad seco',
    min: 0,
  },
  carbonContentSubstrate1SideB: {
    disabled: false,
    value: 43,
    tooltip: 'Contenido de carbono [%]',
    unit: '%',
    variableString: 'contenido carbono',
    min: 0,
    max: 100,
  },
  hydrogenContentSubstrate1SideB: {
    disabled: false,
    value: 5,
    tooltip: 'Contenido de Hidrógeno [%]',
    unit: '%',
    variableString: 'contenido hidrógeno',
    min: 0,
    max: 100,
  },
  oxygenContentSubstrate1SideB: {
    disabled: false,
    value: 30,
    tooltip: 'Contenido de oxígeno [%]',
    unit: '%',
    variableString: 'contenido oxígeno',
    min: 0,
    max: 100,
  },
  nitrogenContentSubstrate1SideB: {
    disabled: false,
    value: 2,
    tooltip: 'Contenido de nitrógeno [%]',
    unit: '%',
    variableString: 'contenido nitrógeno',
    min: 0,
    max: 100,
  },
  sulfurContentSubstrate1SideB: {
    disabled: false,
    value: 0.21,
    tooltip: 'Contenido de azufre [%]',
    unit: '%',
    variableString: 'contenido azufre',
    min: 0,
    max: 100,
  },
  substrate2CompositionSideB: {
    disabled: false,
    value: 0,
    tooltip: 'composición, volume o peso',
    unit: '%',
    variableString: 'composición',
    min: 0,
    max: 100,
  },
  totalSolidsSubstrate2SideB: {
    disabled: false,
    value: 10,
    tooltip: 'Sóldios Totales [%]',
    unit: '%',
    variableString: 'Sólidos Totales',
    min: 0,
    max: 100,
  },
  volatileSolidsSubstrate2SideB: {
    disabled: false,
    value: 5,
    tooltip: 'Sólidos Volátiles[%]',
    unit: '%',
    variableString: 'Sólidos Volátiles',
    min: 0,
    max: 100,
  },
  densitySubstrate2SideB: {
    disabled: false,
    value: 500,
    tooltip: 'densidad seco[g/L]',
    unit: 'g/L',
    variableString: 'densidad seco',
    min: 0,
  },
  carbonContentSubstrate2SideB: {
    disabled: false,
    value: 43,
    tooltip: 'Contenido de carbono [%]',
    unit: '%',
    variableString: 'contenido carbono',
    min: 0,
    max: 100,
  },
  hydrogenContentSubstrate2SideB: {
    disabled: false,
    value: 5,
    tooltip: 'Contenido de Hidrógeno [%]',
    unit: '%',
    variableString: 'contenido hidrógeno',
    min: 0,
    max: 100,
  },
  oxygenContentSubstrate2SideB: {
    disabled: false,
    value: 30,
    tooltip: 'Contenido de oxígeno [%]',
    unit: '%',
    variableString: 'contenido oxígeno',
    min: 0,
    max: 100,
  },
  nitrogenContentSubstrate2SideB: {
    disabled: false,
    value: 2,
    tooltip: 'Contenido de nitrógeno [%]',
    unit: '%',
    variableString: 'contenido nitrógeno',
    min: 0,
    max: 100,
  },
  sulfurContentSubstrate2SideB: {
    disabled: false,
    value: 0.21,
    tooltip: 'Contenido de azufre [%]',
    unit: '%',
    variableString: 'contenido azufre',
    min: 0,
    max: 100,
  },
  substrate3CompositionSideB: {
    disabled: false,
    value: 0,
    tooltip: 'composición, volume o peso',
    unit: '%',
    variableString: 'composición',
    min: 0,
    max: 100,
  },
  totalSolidsSubstrate3SideB: {
    disabled: false,
    value: 10,
    tooltip: 'Sóldios Totales [%]',
    unit: '%',
    variableString: 'Sólidos Totales',
    min: 0,
    max: 100,
  },
  volatileSolidsSubstrate3SideB: {
    disabled: false,
    value: 5,
    tooltip: 'Sólidos Volátiles[%]',
    unit: '%',
    variableString: 'Sólidos Volátiles',
    min: 0,
    max: 100,
  },
  densitySubstrate3SideB: {
    disabled: false,
    value: 500,
    tooltip: 'densidad seco[g/L]',
    unit: 'g/L',
    variableString: 'densidad seco',
    min: 0,
  },
  carbonContentSubstrate3SideB: {
    disabled: false,
    value: 43,
    tooltip: 'Contenido de carbono [%]',
    unit: '%',
    variableString: 'contenido carbono',
    min: 0,
    max: 100,
  },
  hydrogenContentSubstrate3SideB: {
    disabled: false,
    value: 5,
    tooltip: 'Contenido de Hidrógeno [%]',
    unit: '%',
    variableString: 'contenido hidrógeno',
    min: 0,
    max: 100,
  },
  oxygenContentSubstrate3SideB: {
    disabled: false,
    value: 30,
    tooltip: 'Contenido de oxígeno [%]',
    unit: '%',
    variableString: 'contenido oxígeno',
    min: 0,
    max: 100,
  },
  nitrogenContentSubstrate3SideB: {
    disabled: false,
    value: 2,
    tooltip: 'Contenido de nitrógeno [%]',
    unit: '%',
    variableString: 'contenido nitrógeno',
    min: 0,
    max: 100,
  },
  sulfurContentSubstrate3SideB: {
    disabled: false,
    value: 0.21,
    tooltip: 'Contenido de azufre [%]',
    unit: '%',
    variableString: 'contenido azufre',
    min: 0,
    max: 100,
  },
  substrate4CompositionSideB: {
    disabled: false,
    value: 0,
    tooltip: 'composición, volume o peso',
    unit: '%',
    variableString: 'composición',
    min: 0,
    max: 100,
  },
  totalSolidsSubstrate4SideB: {
    disabled: false,
    value: 10,
    tooltip: 'Sóldios Totales [%]',
    unit: '%',
    variableString: 'Sólidos Totales',
    min: 0,
    max: 100,
  },
  volatileSolidsSubstrate4SideB: {
    disabled: false,
    value: 5,
    tooltip: 'Sólidos Volátiles[%]',
    unit: '%',
    variableString: 'Sólidos Volátiles',
    min: 0,
    max: 100,
  },
  densitySubstrate4SideB: {
    disabled: false,
    value: 500,
    tooltip: 'densidad seco[g/L]',
    unit: 'g/L',
    variableString: 'densidad seco',
    min: 0,
  },
  carbonContentSubstrate4SideB: {
    disabled: false,
    value: 43,
    tooltip: 'Contenido de carbono [%]',
    unit: '%',
    variableString: 'contenido carbono',
    min: 0,
    max: 100,
  },
  hydrogenContentSubstrate4SideB: {
    disabled: false,
    value: 5,
    tooltip: 'Contenido de Hidrógeno [%]',
    unit: '%',
    variableString: 'contenido hidrógeno',
    min: 0,
    max: 100,
  },
  oxygenContentSubstrate4SideB: {
    disabled: false,
    value: 30,
    tooltip: 'Contenido de oxígeno [%]',
    unit: '%',
    variableString: 'contenido oxígeno',
    min: 0,
    max: 100,
  },
  nitrogenContentSubstrate4SideB: {
    disabled: false,
    value: 2,
    tooltip: 'Contenido de nitrógeno [%]',
    unit: '%',
    variableString: 'contenido nitrógeno',
    min: 0,
    max: 100,
  },
  sulfurContentSubstrate4SideB: {
    disabled: false,
    value: 0.21,
    tooltip: 'Contenido de azufre [%]',
    unit: '%',
    variableString: 'contenido azufre',
    min: 0,
    max: 100,
  },
  waterCompositionSideB: {
    disabled: false,
    value: 80,
    tooltip: 'Fracción de agua [%]',
    unit: '%',
    variableString: 'Fracción',
    min: 0,
    max: 100,
  },
  methaneR106: {
    disabled: false,
    value: 55,
    tooltip: 'Composición de metano R101 [%]',
    unit: '%',
    variableString: 'CH4',
    min: 0,
    max: 100,
  },
  carbonDioxideR106: {
    disabled: false,
    value: 30,
    tooltip: 'Composición de dióxido de carbono R101 [%]',
    unit: '%',
    variableString: 'CO2',
    min: 0,
    max: 100,
  },
  oxygenR106: {
    disabled: false,
    value: 10,
    tooltip: 'Composición de oxígeno R101 [%]',
    unit: '%',
    variableString: 'O2',
    min: 0,
    max: 100,
  },
  sulfurHydrogenR106: {
    disabled: false,
    value: 100,
    tooltip: 'Composición de sulfuro de hidrógeno R101 [ppm]',
    unit: 'ppm',
    variableString: 'H2S',
    min: 0,
    max: 2000,
  },
  hydrogenR106: {
    disabled: false,
    value: 10,
    tooltip: 'Composición de hidrógeno R101 [ppm] ',
    unit: 'ppm',
    variableString: 'H2',
    min: 0,
    max: 2000,
  },
  methaneR107: {
    disabled: false,
    value: 55,
    tooltip: 'Composición de metano R102 [%]',
    unit: '%',
    variableString: 'CH4',
    min: 0,
    max: 100,
  },
  carbonDioxideR107: {
    disabled: false,
    value: 30,
    tooltip: 'Composición de dióxido de carbono R102 [%]',
    unit: '%',
    variableString: 'CO2',
    min: 0,
    max: 100,
  },
  oxygenR107: {
    disabled: false,
    value: 10,
    tooltip: 'Composición de oxígeno R102 [%]',
    unit: '%',
    variableString: 'O2',
    min: 0,
    max: 100,
  },
  sulfurHydrogenR107: {
    disabled: false,
    value: 100,
    tooltip: 'Composición de sulfuro de hidrógeno R102 [ppm]',
    unit: 'ppm',
    variableString: 'H2S',
    min: 0,
    max: 2000,
  },
  hydrogenR107: {
    disabled: false,
    value: 10,
    tooltip: 'Composición de hidrógeno R102 [ppm] ',
    unit: 'ppm',
    variableString: 'H2',
    min: 0,
    max: 2000,
  },
  methaneR108: {
    disabled: false,
    value: 55,
    tooltip: 'Composición de metano R103 [%]',
    unit: '%',
    variableString: 'CH4',
    min: 0,
    max: 100,
  },
  carbonDioxideR108: {
    disabled: false,
    value: 30,
    tooltip: 'Composición de dióxido de carbono R103 [%]',
    unit: '%',
    variableString: 'CO2',
    min: 0,
    max: 100,
  },
  oxygenR108: {
    disabled: false,
    value: 10,
    tooltip: 'Composición de oxígeno R103 [%]',
    unit: '%',
    variableString: 'O2',
    min: 0,
    max: 100,
  },
  sulfurHydrogenR108: {
    disabled: false,
    value: 100,
    tooltip: 'Composición de sulfuro de hidrógeno R103 [ppm]',
    unit: 'ppm',
    variableString: 'H2S',
    min: 0,
    max: 2000,
  },
  hydrogenR108: {
    disabled: false,
    value: 10,
    tooltip: 'Composición de hidrógeno R103 [ppm] ',
    unit: 'ppm',
    variableString: 'H2',
    min: 0,
    max: 2000,
  },
  methaneR109: {
    disabled: false,
    value: 55,
    tooltip: 'Composición de metano R104 [%]',
    unit: '%',
    variableString: 'CH4',
    min: 0,
    max: 100,
  },
  carbonDioxideR109: {
    disabled: false,
    value: 30,
    tooltip: 'Composición de dióxido de carbono R104 [%]',
    unit: '%',
    variableString: 'CO2',
    min: 0,
    max: 100,
  },
  oxygenR109: {
    disabled: false,
    value: 10,
    tooltip: 'Composición de oxígeno R104 [%]',
    unit: '%',
    variableString: 'O2',
    min: 0,
    max: 100,
  },
  sulfurHydrogenR109: {
    disabled: false,
    value: 100,
    tooltip: 'Composición de sulfuro de hidrógeno R104 [ppm]',
    unit: 'ppm',
    variableString: 'H2S',
    min: 0,
    max: 2000,
  },
  hydrogenR109: {
    disabled: false,
    value: 10,
    tooltip: 'Composición de hidrógeno R104 [ppm] ',
    unit: 'ppm',
    variableString: 'H2',
    min: 0,
    max: 2000,
  },
  methaneR110: {
    disabled: false,
    value: 55,
    tooltip: 'Composición de metano R105 [%]',
    unit: '%',
    variableString: 'CH4',
    min: 0,
    max: 100,
  },
  carbonDioxideR110: {
    disabled: false,
    value: 30,
    tooltip: 'Composición de dióxido de carbono R105 [%]',
    unit: '%',
    variableString: 'CO2',
    min: 0,
    max: 100,
  },
  oxygenR110: {
    disabled: false,
    value: 10,
    tooltip: 'Composición de oxígeno R105 [%]',
    unit: '%',
    variableString: 'O2',
    min: 0,
    max: 100,
  },
  sulfurHydrogenR110: {
    disabled: false,
    value: 100,
    tooltip: 'Composición de sulfuro de hidrógeno R105 [ppm]',
    unit: 'ppm',
    variableString: 'H2S',
    min: 0,
    max: 2000,
  },
  hydrogenR110: {
    disabled: false,
    value: 10,
    tooltip: 'Composición de hidrógeno R105 [ppm] ',
    unit: 'ppm',
    variableString: 'H2',
    min: 0,
    max: 2000,
  },
  testDurationSideB: {
    disabled: false,
    value: 30,
    tooltip: 'Duración de la prueba [días]',
    unit: 'dias',
    variableString: 'Duración de la prueba',
    min: 0,
  },
  TemperatureSideB: {
    disabled: false,
    value: 35,
    tooltip: 'Temperatura Lado A [°c]',
    unit: '°c',
    variableString: 'Temperatura',
    min: 25,
    max: 65,
  },
  pHSideB: {
    disabled: false,
    value: 7,
    tooltip: 'pH',
    unit: '',
    variableString: 'pH',
    min: 0,
    max: 14,
  },
  mixVelocitySideB: {
    disabled: false,
    value: 50,
    tooltip: 'Velocidad de agitación [RPM]',
    unit: 'RPM',
    variableString: 'Velocidad de agitación',
    min: 0,
    max: 300,
  },
  mixTimeSideB: {
    disabled: false,
    value: 30,
    tooltip: 'Tiempo de Agitación [min]',
    unit: 'min',
    variableString: 'Tiempo de agitación',
    min: 0,
    max: 60,
  },
  mixDailySideB: {
    disabled: false,
    value: 10,
    tooltip: 'Agitaciones diarias',
    unit: '',
    variableString: 'Agitaciones diarias',
    min: 0,
    max: 24,
  },
  dosificationVolumeSideB: {
    disabled: false,
    value: 50,
    tooltip: 'Volumen',
    unit: 'mL',
    variableString: 'Volumen',
    min: 0,
    max: 1000,
  },
  dailyInyectionsByTimeSideB: {
    disabled: false,
    value: 4,
    tooltip: 'Tiempo',
    unit: 'horas',
    variableString: 'Tiempo',
    min: 0,
    max: 24,
  },
  dailyInyectionsSideB: {
    disabled: false,
    value: 4,
    tooltip: 'Inyecciones diarias',
    unit: '',
    variableString: 'Inyecciones diarias',
    min: 4,
    max: 12,
  },
};

export const BMP_VARIABLES: DiagramVariableType[] = [];
