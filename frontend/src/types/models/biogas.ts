import Config from '../../config/config';
import { CommonSystemParameter, StepUnitType } from '../common';
import { CommonChartType } from '../graph';
import { InputType } from '../inputType';
import { CommonDigitalTwinsParameter, DiagramVariableType } from './common';

export enum OperationModeType {
  Modo1 = 'Modo1',
  Modo2 = 'Modo2',
  Modo3 = 'Modo3',
  Modo4 = 'Modo4',
  Modo5 = 'Modo5',
}

export enum OperationModelType {
  Arrhenius = 'Arrhenius',
  ADM1 = 'ADM1',
  Gompertz = 'Gompertz',
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

export type BiogasInitialAnalysisConditions = {
  totalSubstrateSolids: InputType;
  volatileSubstrateSolids: InputType;
  substrateDensity: InputType;
  atomicCarbonSubstrateConcetration: InputType;
  atomicHydrogenSubstrateConcetration: InputType;
  atomicOxygenSubstrateConcetration: InputType;
  atomicNitrogenSubstrateConcetration: InputType;
  atomicSulfurSubstrateConcetration: InputType;
};

export type BiogasParameters = CommonSystemParameter &
  CommonDigitalTwinsParameter & {
    anaerobicReactorVolume1: InputType;
    anaerobicReactorVolume2: InputType;
    inputOperationMode: OperationModeType;
    biogasTankVolume1: InputType;
    biogasTankVolume2: InputType;
    biogasTankVolume3: InputType;
    digitalTwinState: boolean;
    digitalTwinStepTime: InputType;
    digitalTwinForecastTime: InputType;
    operationModelType: OperationModelType;
    exponentialFactorR101: InputType;
    activationEnergyR101: InputType;
    lambdaR101: InputType;
    exponentialFactorR102: InputType;
    activationEnergyR102: InputType;
    lambdaR102: InputType;
    difussionCoefficientTower1: InputType;
    adsorbentWeightTower1: InputType;
    lengthTower1: InputType;
    difussionCoefficientTower2: InputType;
    adsorbentWeightTower2: InputType;
    lengthTower2: InputType;
    difussionCoefficientTower3: InputType;
    adsorbentWeightTower3: InputType;
    lengthTower3: InputType;
    initialAnalysisConditionsR101: BiogasInitialAnalysisConditions;
    initialAnalysisConditionsR102: BiogasInitialAnalysisConditions;
    inputSubstrateConditions: boolean;
    inputProximateAnalysisTotalSolids: InputType;
    inputProximateAnalysisVolatileSolids: InputType;
    inputProximateAnalysisDensity: InputType;
    inputElementalAnalysisCarbonContent: InputType;
    inputElementalAnalysisHydrogenContent: InputType;
    inputElementalAnalysisOxygenContent: InputType;
    inputElementalAnalysisNitrogenContent: InputType;
    inputElementalAnalysisSulfurContent: InputType;
    inputMixTK100: boolean;
    inputSpeedMixTK100: InputType;
    inputStartsPerDayMixTK100: InputType;
    inputStartTimeMixTK100: InputType;
    inputPump104: boolean;
    inputPump104HydraulicRetentionTime: InputType;
    inputPump104StartTime: InputType;
    inputPump104StartsPerDay: InputType;
    inputPump101: boolean;
    inputPump101Flow: InputType;
    inputPump101StartTime: InputType;
    inputPump101StartsPerDay: InputType;
    inputPump102: boolean;
    inputPump102Flow: InputType;
    inputPump102StartTime: InputType;
    inputPump102StartsPerDay: InputType;
    inputMixR101: boolean;
    inputSpeedMixR101: InputType;
    inputStartsPerDayMixR101: InputType;
    inputStartTimeMixR101: InputType;
    inputPHR101: InputType;
    inputTemperatureR101: InputType;
    inputMixR102: boolean;
    inputSpeedMixR102: InputType;
    inputStartsPerDayMixR102: InputType;
    inputStartTimeMixR102: InputType;
    inputPHR102: InputType;
    inputTemperatureR102: InputType;
    diagramBiogas: DiagramBiogasType;
    diagramBiogasUnit: DiagramBiogasUnitType;
    diagramCompound: DiagramCompoundType;
    diagramHumidity: DiagramHumidityType;
    restartFlag: boolean;
  };

export type BiogasOutput = {
  n: number;
  a: number;
  b: number;
  c: number;
  d: number;
  Mix_Velocity_TK100: number;
  C_sv: number;
  SV: number;
  C_st: number;
  ST: number;
  Pump104Flow: number;
  Mix_Velocity_R101: number;
  C_sv_R101: number;
  SV_R101: number;
  C_st_R101: number;
  ST_R101: number;
  Organic_Charge_R101: number;
  pH_R101: number;
  Temp_R101: number;
  x_R101: number;
  K_R101: number;
  Ea_R101: number;
  Lambda_R101: number;
  AcumBiogasVolumenV101: number;
  StorageBiogasVolumeV101: number;
  AcumBiogasPressureV101: number;
  StorageBiogasPressureV101: number;
  StorageCH4_V101Volume: number;
  StorageCH4_V101Concentration: number;
  StorageCH4_V101moles: number;
  StorageCO2_V101Volume: number;
  StorageCO2_V101Concentration: number;
  StorageCO2_V101moles: number;
  StorageH2S_V101Volume: number;
  StorageH2S_V101Concentration: number;
  StorageH2S_V101moles: number;
  StorageO2_V101Volume: number;
  StorageO2_V101Concentration: number;
  StorageO2_V101moles: number;
  StorageH2_V101Volume: number;
  StorageH2_V101Concentration: number;
  StorageH2_V101moles: number;
  StorageNH3_V101Volume: number;
  StorageNH3_V101Concentration: number;
  StorageNH3_V101moles: number;
  moles_humidity_V101: number;
  Relative_humidity_V101: number;
  StorageEnergy_V101: number;
  AcumBiogasVolumenV102: number;
  StorageBiogasVolumeV102: number;
  AcumBiogasPressureV102: number;
  StorageBiogasPressureV102: number;
  StorageCH4_V102Volume: number;
  StorageCH4_V102Concentration: number;
  StorageCH4_V102moles: number;
  StorageCO2_V102Volume: number;
  StorageCO2_V102Concentration: number;
  StorageCO2_V102moles: number;
  StorageH2S_V102Volume: number;
  StorageH2S_V102Concentration: number;
  StorageH2S_V102moles: number;
  StorageO2_V102Volume: number;
  StorageO2_V102Concentration: number;
  StorageO2_V102moles: number;
  StorageH2_V102Volume: number;
  StorageH2_V102Concentration: number;
  StorageH2_V102moles: number;
  StorageNH3_V102Volume: number;
  StorageNH3_V102Concentration: number;
  StorageNH3_V102moles: number;
  moles_humidity_V102: number;
  Relative_humidity_V102: number;
  StorageEnergy_V102: number;
  ads_NH3_bt: number;
  ads_H2S_bt: number;
  ads_H2O_bt: number;
  x_bt: number;
  AcumBiogasVolumenV107: number;
  StorageBiogasVolumeV107: number;
  AcumBiogasPressureV107: number;
  StorageBiogasPressureV107: number;
  StorageCH4_V107Volume: number;
  StorageCH4_V107Concentration: number;
  StorageCH4_V107moles: number;
  StorageCO2_V107Volume: number;
  StorageCO2_V107Concentration: number;
  StorageCO2_V107moles: number;
  StorageH2S_V107Volume: number;
  StorageH2S_V107Concentration: number;
  StorageH2S_V107moles: number;
  StorageO2_V107Volume: number;
  StorageO2_V107Concentration: number;
  StorageO2_V107moles: number;
  StorageH2_V107Volume: number;
  StorageH2_V107Concentration: number;
  StorageH2_V107moles: number;
  StorageNH3_V107Volume: number;
  StorageNH3_V107Concentration: number;
  StorageNH3_V107moles: number;
  moles_humidity_V107: number;
  Relative_humidity_V107: number;
  StorageEnergy_V107: number;
  Pump101Flow: number;
  Mix_Velocity_R102: number;
  pH_R102: number;
  Temp_R102: number;
  K_R102: number;
  Ea_R102: number;
  Lambda_R102: number;
  C_sv_R102: number;
  SV_R102: number;
  C_st_R102: number;
  ST_R102: number;
  Organic_Charge_R102: number;
  x_R102: number;
  Pump102Flow: number;
};

export type BiogasOutputHistoric = CommonChartType & {
  n: number[];
  a: number[];
  b: number[];
  c: number[];
  d: number[];
  Mix_Velocity_TK100: number[];
  C_sv: number[];
  SV: number[];
  C_st: number[];
  ST: number[];
  Pump104Flow: number[];
  Mix_Velocity_R101: number[];
  C_sv_R101: number[];
  SV_R101: number[];
  C_st_R101: number[];
  ST_R101: number[];
  Organic_Charge_R101: number[];
  pH_R101: number[];
  Temp_R101: number[];
  x_R101: number[];
  K_R101: number[];
  Ea_R101: number[];
  Lambda_R101: number[];
  AcumBiogasVolumenV101: number[];
  StorageBiogasVolumeV101: number[];
  AcumBiogasPressureV101: number[];
  StorageBiogasPressureV101: number[];
  StorageCH4_V101Volume: number[];
  StorageCH4_V101Concentration: number[];
  StorageCH4_V101moles: number[];
  StorageCO2_V101Volume: number[];
  StorageCO2_V101Concentration: number[];
  StorageCO2_V101moles: number[];
  StorageH2S_V101Volume: number[];
  StorageH2S_V101Concentration: number[];
  StorageH2S_V101moles: number[];
  StorageO2_V101Volume: number[];
  StorageO2_V101Concentration: number[];
  StorageO2_V101moles: number[];
  StorageH2_V101Volume: number[];
  StorageH2_V101Concentration: number[];
  StorageH2_V101moles: number[];
  StorageNH3_V101Volume: number[];
  StorageNH3_V101Concentration: number[];
  StorageNH3_V101moles: number[];
  moles_humidity_V101: number[];
  Relative_humidity_V101: number[];
  StorageEnergy_V101: number[];
  AcumBiogasVolumenV102: number[];
  StorageBiogasVolumeV102: number[];
  AcumBiogasPressureV102: number[];
  StorageBiogasPressureV102: number[];
  StorageCH4_V102Volume: number[];
  StorageCH4_V102Concentration: number[];
  StorageCH4_V102moles: number[];
  StorageCO2_V102Volume: number[];
  StorageCO2_V102Concentration: number[];
  StorageCO2_V102moles: number[];
  StorageH2S_V102Volume: number[];
  StorageH2S_V102Concentration: number[];
  StorageH2S_V102moles: number[];
  StorageO2_V102Volume: number[];
  StorageO2_V102Concentration: number[];
  StorageO2_V102moles: number[];
  StorageH2_V102Volume: number[];
  StorageH2_V102Concentration: number[];
  StorageH2_V102moles: number[];
  StorageNH3_V102Volume: number[];
  StorageNH3_V102Concentration: number[];
  StorageNH3_V102moles: number[];
  moles_humidity_V102: number[];
  Relative_humidity_V102: number[];
  StorageEnergy_V102: number[];
  ads_NH3_bt: number[];
  ads_H2S_bt: number[];
  ads_H2O_bt: number[];
  x_bt: number[];
  AcumBiogasVolumenV107: number[];
  StorageBiogasVolumeV107: number[];
  AcumBiogasPressureV107: number[];
  StorageBiogasPressureV107: number[];
  StorageCH4_V107Volume: number[];
  StorageCH4_V107Concentration: number[];
  StorageCH4_V107moles: number[];
  StorageCO2_V107Volume: number[];
  StorageCO2_V107Concentration: number[];
  StorageCO2_V107moles: number[];
  StorageH2S_V107Volume: number[];
  StorageH2S_V107Concentration: number[];
  StorageH2S_V107moles: number[];
  StorageO2_V107Volume: number[];
  StorageO2_V107Concentration: number[];
  StorageO2_V107moles: number[];
  StorageH2_V107Volume: number[];
  StorageH2_V107Concentration: number[];
  StorageH2_V107moles: number[];
  StorageNH3_V107Volume: number[];
  StorageNH3_V107Concentration: number[];
  StorageNH3_V107moles: number[];
  moles_humidity_V107: number[];
  Relative_humidity_V107: number[];
  StorageEnergy_V107: number[];
  Pump101Flow: number[];
  Mix_Velocity_R102: number[];
  pH_R102: number[];
  Temp_R102: number[];
  K_R102: number[];
  Ea_R102: number[];
  Lambda_R102: number[];
  C_sv_R102: number[];
  SV_R102: number[];
  C_st_R102: number[];
  ST_R102: number[];
  Organic_Charge_R102: number[];
  x_R102: number[];
  Pump102Flow: number[];
};

export const BIOGAS: BiogasParameters = {
  name: 'Nombre',
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
  anaerobicReactorVolume1: {
    disabled: false,
    value: 30,
    tooltip: 'Volumen del reactor anaerobio 1',
    unit: 'L',
    variableString: 'Volumen reactor 1 R101',

    min: 10,
    max: 30000,
  },
  anaerobicReactorVolume2: {
    disabled: false,
    value: 70,
    tooltip: 'Volumen del reactor anaerobio 2',
    unit: 'L',
    variableString: 'Volumen reactor 2 R102',

    min: 10,
    max: 100000,
  },
  inputOperationMode: OperationModeType.Modo1,
  biogasTankVolume1: {
    disabled: false,
    value: 15,
    tooltip: 'Volumen tanque de biogas 1',
    unit: 'L',
    variableString: 'Volumen tanque 1 V101',

    min: 5,
    max: 15000,
  },
  biogasTankVolume2: {
    disabled: false,
    value: 35,
    tooltip: 'Volumen tanque de biogas 2',
    unit: 'L',
    variableString: 'Volumen tanque 2 V102',

    min: 5,
    max: 50000,
  },
  biogasTankVolume3: {
    disabled: false,
    value: 35,
    tooltip: 'Volumen tanque de biogas 3',
    unit: 'L',
    variableString: 'Volumen tanque 3 V107',

    min: 5,
    max: 50000,
  },
  digitalTwinState: false,
  digitalTwinStepTime: {
    disabled: false,
    value: 30,
    tooltip: 'Paso de tiempo del gemelo digital',
    unit: 's',
    variableString: 'Paso de tiempo',
    min: 1,
    max: 60,
  },
  digitalTwinForecastTime: {
    disabled: false,
    value: 1,
    tooltip: 'Tiempo de predicción del gemelo digital',
    unit: 'h',
    variableString: 'Tiempo de predicción',
    min: 0.1,
    max: 72,
    step: 0.1,
  },
  operationModelType: OperationModelType.Arrhenius,
  exponentialFactorR101: {
    disabled: false,
    value: 100,
    tooltip: 'Factor preexponencial para R101',
    unit: 'L/s',
    variableString: 'K R101',
  },
  activationEnergyR101: {
    disabled: false,
    value: 1000000,
    tooltip: 'Energía de activación R101',
    unit: 'J/mol',
    variableString: 'Ea R101',
  },
  lambdaR101: {
    disabled: true,
    value: -44928,
    tooltip: 'Lambda para R101',
    unit: '',
    variableString: 'λ R101',
  },
  exponentialFactorR102: {
    disabled: false,
    value: 100,
    tooltip: 'Factor preexponencial para R102',
    unit: 'L/s',
    variableString: 'K R102',
  },
  activationEnergyR102: {
    disabled: false,
    value: 1000000,
    tooltip: 'Energía de activación R102',
    unit: 'J/mol',
    variableString: 'Ea R102',
  },
  lambdaR102: {
    disabled: true,
    value: -44928,
    tooltip: 'Lambda para R102',
    unit: '',
    variableString: 'λ R102',
  },
  difussionCoefficientTower1: {
    disabled: false,
    value: 1e-10,
    tooltip: 'Coeficiente de difusión torre 1',
    unit: '',
    variableString: 'Coeficiente difusión 1',
  },
  adsorbentWeightTower1: {
    disabled: false,
    value: 5000,
    tooltip: 'Peso de adsorción torre 1',
    unit: 'g',
    variableString: 'Peso adsorción 1',
    min: 0,
    max: 50000,
  },
  lengthTower1: {
    disabled: false,
    value: 0.2,
    tooltip: 'Altura torre 1',
    unit: 'm',
    variableString: 'Altura 1',
    min: 0.1,
    max: 5,
    step: 0.1,
  },
  difussionCoefficientTower2: {
    disabled: false,
    value: 1e-10,
    tooltip: 'Coeficiente de difusión torre 2',
    unit: '',
    variableString: 'Coeficiente difusión 2',
  },
  adsorbentWeightTower2: {
    disabled: false,
    value: 5000,
    tooltip: 'Peso de adsorción torre 2',
    unit: 'g',
    variableString: 'Peso adsorción 2',
    min: 0,
    max: 50000,
  },
  lengthTower2: {
    disabled: false,
    value: 0.2,
    tooltip: 'Altura torre 2',
    unit: 'm',
    variableString: 'Altura 2',
    min: 0.1,
    max: 5,
    step: 0.1,
  },
  difussionCoefficientTower3: {
    disabled: false,
    value: 1e-10,
    tooltip: 'Coeficiente de difusión torre 3',
    unit: '',
    variableString: 'Coeficiente difusión 3',
  },
  adsorbentWeightTower3: {
    disabled: false,
    value: 5000,
    tooltip: 'Peso de adsorción torre 3',
    unit: 'g',
    variableString: 'Peso adsorción 3',
    min: 0,
    max: 50000,
  },
  lengthTower3: {
    disabled: false,
    value: 0.2,
    tooltip: 'Altura torre 1',
    unit: 'm',
    variableString: 'Altura 3',
    min: 0.1,
    max: 5,
    step: 0.1,
  },
  initialAnalysisConditionsR101: {
    totalSubstrateSolids: {
      disabled: false,
      value: 10,
      tooltip: 'Sólidos totales del sustrato en R101 al inicio',
      unit: '%',
      variableString: 'Sólidos totales',
      min: 0,
      max: 30,
    },
    volatileSubstrateSolids: {
      disabled: false,
      value: 1,
      tooltip: 'Sólidos volátiles del sustrato en R101 al inicio',
      unit: '%',
      variableString: 'Sólidos volátiles',
      min: 0,
      max: 10,
    },
    substrateDensity: {
      disabled: false,
      value: 1000,
      tooltip: 'Densidad del sustrato en R101 al inicio',
      unit: 'g / L',
      variableString: 'Densidad del sustrato',
      min: 200,
      max: 2000,
      step: 10,
    },
    atomicCarbonSubstrateConcetration: {
      disabled: false,
      value: 40.48,
      tooltip:
        'Concentración de carbono atómico en el sustrato en R101 al inicio',
      unit: '%',
      variableString: 'Concentración de carbono atómico',
      min: 0,
      max: 100,
      step: 0.01,
    },
    atomicHydrogenSubstrateConcetration: {
      disabled: false,
      value: 5.29,
      tooltip:
        'Concentración de hidrógeno atómico en el sustrato en R101 al inicio',
      unit: '%',
      variableString: 'Concentración de hidrógeno atómico',
      min: 0,
      max: 100,
      step: 0.01,
    },
    atomicOxygenSubstrateConcetration: {
      disabled: false,
      value: 29.66,
      tooltip:
        'Concentración de oxígeno atómico en el sustrato en R101 al inicio',
      unit: '%',
      variableString: 'Concentración de oxígeno atómico',
      min: 0,
      max: 100,
      step: 0.01,
    },
    atomicNitrogenSubstrateConcetration: {
      disabled: false,
      value: 1.37,
      tooltip:
        'Concentración de nitrógeno atómico en el sustrato en R101 al inicio',
      unit: '%',
      variableString: 'Concentración de nitrógeno atómico',
      min: 0,
      max: 100,
      step: 0.01,
    },
    atomicSulfurSubstrateConcetration: {
      disabled: false,
      value: 0.211,
      tooltip:
        'Concentración de azúfre atómico en el sustrato en R101 al inicio',
      unit: '%',
      variableString: 'Concentración de azúfre atómico',
      min: 0,
      max: 100,
      step: 0.01,
    },
  },
  initialAnalysisConditionsR102: {
    totalSubstrateSolids: {
      disabled: false,
      value: 10,
      tooltip: 'Sólidos totales del sustrato en R102 al inicio',
      unit: '%',
      variableString: 'Sólidos totales',
      min: 0,
      max: 30,
    },
    volatileSubstrateSolids: {
      disabled: false,
      value: 1,
      tooltip: 'Sólidos volátiles del sustrato en R102 al inicio',
      unit: '%',
      variableString: 'Sólidos volátiles',
      min: 0,
      max: 10,
    },
    substrateDensity: {
      disabled: false,
      value: 1000,
      tooltip: 'Densidad del sustrato en R102 al inicio',
      unit: 'g / L',
      variableString: 'Densidad del sustrato',
      min: 200,
      max: 2000,
      step: 10,
    },
    atomicCarbonSubstrateConcetration: {
      disabled: false,
      value: 40.48,
      tooltip:
        'Concentración de carbono atómico en el sustrato en R102 al inicio',
      unit: '%',
      variableString: 'Concentración de carbono atómico',
      min: 0,
      max: 100,
      step: 0.01,
    },
    atomicHydrogenSubstrateConcetration: {
      disabled: false,
      value: 5.29,
      tooltip:
        'Concentración de hidrógeno atómico en el sustrato en R102 al inicio',
      unit: '%',
      variableString: 'Concentración de hidrógeno atómico',
      min: 0,
      max: 100,
      step: 0.01,
    },
    atomicOxygenSubstrateConcetration: {
      disabled: false,
      value: 29.66,
      tooltip:
        'Concentración de oxígeno atómico en el sustrato en R102 al inicio',
      unit: '%',
      variableString: 'Concentración de oxígeno atómico',
      min: 0,
      max: 100,
      step: 0.01,
    },
    atomicNitrogenSubstrateConcetration: {
      disabled: false,
      value: 1.37,
      tooltip:
        'Concentración de nitrógeno atómico en el sustrato en R102 al inicio',
      unit: '%',
      variableString: 'Concentración de nitrógeno atómico',
      min: 0,
      max: 100,
      step: 0.01,
    },
    atomicSulfurSubstrateConcetration: {
      disabled: false,
      value: 0.211,
      tooltip:
        'Concentración de azúfre atómico en el sustrato en R102 al inicio',
      unit: '%',
      variableString: 'Concentración de azúfre atómico',
      min: 0,
      max: 100,
      step: 0.01,
    },
  },
  inputOfflineOperation: true,
  inputSubstrateConditions: true,
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
  inputMixTK100: true,
  inputSpeedMixTK100: {
    disabled: false,
    value: 100,
    tooltip: 'Velocidad de agitación TK100',
    unit: 'RPM',
    variableString: 'Velocidad mezclado TK100',
    min: 0,
    max: 500,
  },
  inputStartsPerDayMixTK100: {
    disabled: false,
    value: 20,
    tooltip: 'Inicio por día TK100',
    unit: '',
    variableString: 'Inicio por día TK100',
    min: 0,
    max: 24,
  },
  inputStartTimeMixTK100: {
    disabled: false,
    value: 10,
    tooltip: 'Tiempo de encendido TK100',
    unit: 'min',
    variableString: 'Tiempo encendido TK100',
    min: 0,
    max: 60,
  },
  inputPump104: true,
  inputPump104HydraulicRetentionTime: {
    disabled: false,
    value: 30,
    tooltip: 'Tiempo de retención hidráulico de la bomba',
    unit: 'días',
    variableString: 'TRH',
    min: 5,
    max: 100,
  },
  inputPump104StartTime: {
    disabled: false,
    value: 10,
    tooltip: 'Tiempo de encendido de la bomba',
    unit: 'min',
    variableString: 'Tiempo de encendido',
    min: 0,
    max: 60,
  },
  inputPump104StartsPerDay: {
    disabled: false,
    value: 5,
    tooltip: 'Encendidos por día de la bomba',
    unit: '',
    variableString: 'Encendido / día',
    min: 0,
    max: 24,
  },
  inputPump101: true,
  inputPump101Flow: {
    disabled: false,
    value: 2.4,
    tooltip: 'Caudal de la bomba',
    unit: 'L/h',
    variableString: 'Caudal',
    min: 0,
    max: 24,
    step: 0.1,
  },
  inputPump101StartTime: {
    disabled: false,
    value: 10,
    tooltip: 'Tiempo de encendido de la bomba',
    unit: 'min',
    variableString: 'Tiempo de encendido',
    min: 0,
    max: 60,
  },
  inputPump101StartsPerDay: {
    disabled: false,
    value: 5,
    tooltip: 'Encendidos por día de la bomba',
    unit: '',
    variableString: 'Encendido / día',
    min: 0,
    max: 24,
  },
  inputPump102: true,
  inputPump102Flow: {
    disabled: false,
    value: 2.4,
    tooltip: 'Caudal de la bomba',
    unit: 'L/h',
    variableString: 'Caudal',
    min: 0,
    max: 24,
    step: 0.1,
  },
  inputPump102StartTime: {
    disabled: false,
    value: 10,
    tooltip: 'Tiempo de encendido de la bomba',
    unit: 'min',
    variableString: 'Tiempo de encendido',
    min: 0,
    max: 60,
  },
  inputPump102StartsPerDay: {
    disabled: false,
    value: 5,
    tooltip: 'Encendidos por día de la bomba',
    unit: '',
    variableString: 'Encendido / día',
    min: 0,
    max: 24,
  },
  inputMixR101: true,
  inputSpeedMixR101: {
    disabled: false,
    value: 100,
    tooltip: 'Velocidad de agitación R101',
    unit: 'RPM',
    variableString: 'Velocidad mezclado R101',
    min: 0,
    max: 500,
  },
  inputStartsPerDayMixR101: {
    disabled: false,
    value: 20,
    tooltip: 'Inicio por día R101',
    unit: '',
    variableString: 'Inicio por día R101',
    min: 0,
    max: 24,
  },
  inputStartTimeMixR101: {
    disabled: false,
    value: 10,
    tooltip: 'Tiempo de encendido R101',
    unit: 'min',
    variableString: 'Tiempo encendido R101',
    min: 0,
    max: 60,
  },
  inputPHR101: {
    disabled: false,
    value: 7,
    tooltip: 'Acidez R101',
    unit: '',
    variableString: 'Acidez R101',
    min: 0,
    max: 14,
  },
  inputTemperatureR101: {
    disabled: false,
    value: 35,
    tooltip: 'Temperatura reactor 101',
    unit: '°C',
    variableString: 'Temperatura R-101',
    min: 15,
    max: 60,
  },
  inputMixR102: true,
  inputSpeedMixR102: {
    disabled: false,
    value: 100,
    tooltip: 'Velocidad de agitación R102',
    unit: 'RPM',
    variableString: 'Velocidad mezclado R102',
    min: 0,
    max: 500,
  },
  inputStartsPerDayMixR102: {
    disabled: false,
    value: 20,
    tooltip: 'Inicio por día R102',
    unit: '',
    variableString: 'Inicio por día R102',
    min: 0,
    max: 24,
  },
  inputStartTimeMixR102: {
    disabled: false,
    value: 10,
    tooltip: 'Tiempo de encendido R102',
    unit: 'min',
    variableString: 'Tiempo encendido R102',
    min: 0,
    max: 60,
  },
  inputPHR102: {
    disabled: false,
    value: 7,
    tooltip: 'Acidez R102',
    unit: '',
    variableString: 'Acidez R102',
    min: 0,
    max: 14,
  },
  inputTemperatureR102: {
    disabled: false,
    value: 35,
    tooltip: 'Temperatura reactor 102',
    unit: '°C',
    variableString: 'Temperatura R-102',
    min: 15,
    max: 60,
  },
  diagramBiogas: DiagramBiogasType.Accumulated,
  diagramBiogasUnit: DiagramBiogasUnitType.NormalVolume,
  diagramCompound: DiagramCompoundType.Concentration,
  diagramHumidity: DiagramHumidityType.Relative,
  restartFlag: false,
};

export const BIOGAS_MODE1: DiagramVariableType[] = [
  {
    name: 'Subindice de carbono formula empírica',
    variable: 'n',
    unit: '',
    isShown: true,
    diagramName: '',
    fixed: 0,
    x: 1200,
    y: 250,
    scientificNotation: false,
  },
  {
    name: 'Subindice de hidrógeno formula empírica',
    variable: 'a',
    unit: '',
    isShown: true,
    diagramName: '',
    fixed: 0,
    x: 1600,
    y: 250,
    scientificNotation: false,
  },
  {
    name: 'Subindice de oxígeno formula empírica',
    variable: 'b',
    unit: '',
    isShown: true,
    diagramName: '',
    fixed: 0,
    x: 2000,
    y: 250,
    scientificNotation: false,
  },
  {
    name: 'Subindice de nitrógeno formula empírica',
    variable: 'c',
    unit: '',
    isShown: true,
    diagramName: '',
    fixed: 0,
    x: 2400,
    y: 250,
    scientificNotation: false,
  },
  {
    name: 'Subindice de azufre formula empírica',
    variable: 'd',
    unit: '',
    isShown: true,
    diagramName: '',
    fixed: 0,
    x: 2800,
    y: 250,
    scientificNotation: false,
  },
  {
    name: 'Velocidad de agitación tanque premezcla',
    variable: 'Mix_Velocity_TK100',
    unit: 'RPM',
    isShown: true,
    diagramName: 'RPM',
    fixed: 0,
    x: 700,
    y: 500,
    scientificNotation: false,
  },
  {
    name: 'Concentración de sólidos volátiles en gSV/L',
    variable: 'C_sv',
    unit: 'gSV/L',
    isShown: true,
    diagramName: 'Csv',
    fixed: 2,
    x: 900,
    y: 1350,
    scientificNotation: true,
  },
  {
    name: 'Concentración de sólidos volátiles en %',
    variable: 'SV',
    unit: '%',
    isShown: true,
    diagramName: 'SV',
    fixed: 2,
    x: 900,
    y: 1500,
    scientificNotation: false,
  },
  {
    name: 'Concentración de sólidos totales en gST/L',
    variable: 'C_st',
    unit: 'gST/L',
    isShown: true,
    diagramName: 'Cst',
    fixed: 2,
    x: 900,
    y: 1650,
    scientificNotation: true,
  },
  {
    name: 'Concentración de sólidos totales en %',
    variable: 'ST',
    unit: '%',
    isShown: true,
    diagramName: 'ST',
    fixed: 2,
    x: 900,
    y: 1800,
    scientificNotation: false,
  },
  {
    name: 'Caudal',
    variable: 'Pump104Flow',
    unit: 'L/h',
    isShown: true,
    diagramName: 'Caudal',
    fixed: 2,
    x: 600,
    y: 3300,
    scientificNotation: false,
  },
  {
    name: 'Velocidad de agitación reactor R101',
    variable: 'Mix_Velocity_R101',
    unit: 'RPM',
    isShown: true,
    diagramName: 'RPM',
    fixed: 0,
    x: 2800,
    y: 3300,
    scientificNotation: false,
  },
  {
    name: 'Concentración de sólidos volátiles en gSV/L',
    variable: 'C_sv_R101',
    unit: 'gSV/L',
    isShown: true,
    diagramName: 'Csv',
    fixed: 2,
    x: 2200,
    y: 6200,
    scientificNotation: true,
  },
  {
    name: 'Concentración de sólidos volátiles en %',
    variable: 'SV_R101',
    unit: '%',
    isShown: true,
    diagramName: 'SV',
    fixed: 2,
    x: 2200,
    y: 6350,
    scientificNotation: false,
  },
  {
    name: 'Concentración de sólidos totales en gST/L',
    variable: 'C_st_R101',
    unit: 'gST/L',
    isShown: true,
    diagramName: 'Cst',
    fixed: 2,
    x: 2200,
    y: 6500,
    scientificNotation: true,
  },
  {
    name: 'Concentración de sólidos totales en %',
    variable: 'ST_R101',
    unit: '%',
    isShown: true,
    diagramName: 'ST',
    fixed: 2,
    x: 2200,
    y: 6650,
    scientificNotation: false,
  },
  {
    name: 'Carga Orgánica en el reactor R101',
    variable: 'Organic_Charge_R101',
    unit: 'gSV/L-dia',
    isShown: true,
    diagramName: 'OC',
    fixed: 2,
    x: 2200,
    y: 6800,
    scientificNotation: true,
  },
  {
    name: 'pH',
    variable: 'pH_R101',
    unit: '',
    isShown: true,
    diagramName: 'pH',
    fixed: 2,
    x: 600,
    y: 4200,
    scientificNotation: false,
  },
  {
    name: 'Temperatura R101',
    variable: 'Temp_R101',
    unit: '°c',
    isShown: true,
    diagramName: 'Temperatura',
    fixed: 2,
    x: 600,
    y: 4350,
    scientificNotation: false,
  },
  {
    name: 'Conversión del reactivo límite',
    variable: 'x_R101',
    unit: '%',
    isShown: true,
    diagramName: 'x',
    fixed: 2,
    x: 2200,
    y: 6950,
    scientificNotation: false,
  },
  {
    name: 'Parámetro cinético preexponencias Arrhenius,  ADM1 y  Gompertz',
    variable: 'K_R101',
    unit: 'L/s',
    isShown: true,
    diagramName: 'K',
    fixed: 2,
    x: 1200,
    y: 6200,
    scientificNotation: true,
    hasAdditionalCondition: 0,
  },
  {
    name: 'Parámetro cinético preexponencias Arrhenius,  ADM1 y  Gompertz',
    variable: 'K_R101',
    unit: 'L / gSV',
    isShown: true,
    diagramName: 'ym',
    fixed: 2,
    x: 1200,
    y: 6200,
    scientificNotation: true,
    hasAdditionalCondition: 1,
  },
  {
    name: 'Parámetro cinético energía de activación',
    variable: 'Ea_R101',
    unit: 'J/mol',
    isShown: true,
    diagramName: 'Ea',
    fixed: 2,
    x: 1200,
    y: 6350,
    scientificNotation: true,
    hasAdditionalCondition: 2,
  },
  {
    name: 'Parámetro cinético energía de activación',
    variable: 'Ea_R101',
    unit: 'L / gSV-s',
    isShown: true,
    diagramName: 'U',
    fixed: 2,
    x: 1200,
    y: 6350,
    scientificNotation: true,
    hasAdditionalCondition: 3,
  },
  {
    name: 'Tiempo de retraso o periodo de tiempo mínimo para producir biogás',
    variable: 'Lambda_R101',
    unit: 's',
    isShown: true,
    diagramName: 'λ',
    fixed: 2,
    x: 1200,
    y: 6500,
    scientificNotation: true,
    hasAdditionalCondition: 3,
  },
  {
    name: 'Volumen normal de biogas acumulado',
    variable: 'AcumBiogasVolumenV101',
    unit: 'NL',
    isShown: true,
    diagramName: 'Vol',
    fixed: 2,
    x: 3000,
    y: 800,
    scientificNotation: false,
    hasAdditionalCondition: 5,
  },
  {
    name: 'Volumen normal de biogas almacenado',
    variable: 'StorageBiogasVolumeV101',
    unit: 'NL',
    isShown: true,
    diagramName: 'Vol',
    fixed: 2,
    x: 3000,
    y: 800,
    scientificNotation: false,
    hasAdditionalCondition: 6,
  },
  {
    name: 'Presión de biogás acumulado',
    variable: 'AcumBiogasPressureV101',
    unit: 'psi',
    isShown: true,
    diagramName: 'pres',
    fixed: 2,
    x: 3000,
    y: 800,
    scientificNotation: false,
    hasAdditionalCondition: 7,
  },
  {
    name: 'Presión de biogás almacenado',
    variable: 'StorageBiogasPressureV101',
    unit: 'psi',
    isShown: true,
    diagramName: 'pres',
    fixed: 2,
    x: 3000,
    y: 800,
    scientificNotation: false,
    hasAdditionalCondition: 8,
  },
  {
    name: 'Metano almacenado en volumen normal en tanque V101',
    variable: 'StorageCH4_V101Volume',
    unit: 'NL',
    isShown: true,
    diagramName: 'CH4',
    fixed: 2,
    x: 3000,
    y: 950,
    scientificNotation: false,
    hasAdditionalCondition: 9,
  },
  {
    name: 'Concentración de metano almacenada en el tanque V101',
    variable: 'StorageCH4_V101Concentration',
    unit: '%',
    isShown: true,
    diagramName: 'CH4',
    fixed: 2,
    x: 3000,
    y: 950,
    scientificNotation: false,
    hasAdditionalCondition: 10,
  },
  {
    name: 'moles de metano almacenada en tanque V101',
    variable: 'StorageCH4_V101moles',
    unit: 'mol',
    isShown: true,
    diagramName: 'CH4',
    fixed: 2,
    x: 3000,
    y: 950,
    scientificNotation: true,
    hasAdditionalCondition: 11,
  },
  {
    name: 'Metano almacenado en volumen normal en tanque V101',
    variable: 'StorageCO2_V101Volume',
    unit: 'NL',
    isShown: true,
    diagramName: 'CO2',
    fixed: 2,
    x: 3000,
    y: 1100,
    scientificNotation: false,
    hasAdditionalCondition: 9,
  },
  {
    name: 'Concentración de metano almacenada en el tanque V101',
    variable: 'StorageCO2_V101Concentration',
    unit: '%',
    isShown: true,
    diagramName: 'CO2',
    fixed: 2,
    x: 3000,
    y: 1100,
    scientificNotation: false,
    hasAdditionalCondition: 10,
  },
  {
    name: 'moles de metano almacenada en tanque V101',
    variable: 'StorageCO2_V101moles',
    unit: 'mol',
    isShown: true,
    diagramName: 'CO2',
    fixed: 2,
    x: 3000,
    y: 1100,
    scientificNotation: true,
    hasAdditionalCondition: 11,
  },
  {
    name: 'Metano almacenado en volumen normal en tanque V101',
    variable: 'StorageH2S_V101Volume',
    unit: 'NL',
    isShown: true,
    diagramName: 'H2S',
    fixed: 2,
    x: 3000,
    y: 1250,
    scientificNotation: false,
    hasAdditionalCondition: 9,
  },
  {
    name: 'Concentración de metano almacenada en el tanque V101',
    variable: 'StorageH2S_V101Concentration',
    unit: 'ppm',
    isShown: true,
    diagramName: 'H2S',
    fixed: 0,
    x: 3000,
    y: 1250,
    scientificNotation: false,
    hasAdditionalCondition: 10,
  },
  {
    name: 'moles de metano almacenada en tanque V101',
    variable: 'StorageH2S_V101moles',
    unit: 'mol',
    isShown: true,
    diagramName: 'H2S',
    fixed: 2,
    x: 3000,
    y: 1250,
    scientificNotation: true,
    hasAdditionalCondition: 11,
  },
  {
    name: 'Metano almacenado en volumen normal en tanque V101',
    variable: 'StorageO2_V101Volume',
    unit: 'NL',
    isShown: true,
    diagramName: 'O2',
    fixed: 2,
    x: 3000,
    y: 1400,
    scientificNotation: false,
    hasAdditionalCondition: 9,
  },
  {
    name: 'Concentración de metano almacenada en el tanque V101',
    variable: 'StorageO2_V101Concentration',
    unit: '%',
    isShown: true,
    diagramName: 'O2',
    fixed: 2,
    x: 3000,
    y: 1400,
    scientificNotation: false,
    hasAdditionalCondition: 10,
  },
  {
    name: 'moles de metano almacenada en tanque V101',
    variable: 'StorageO2_V101moles',
    unit: 'mol',
    isShown: true,
    diagramName: 'O2',
    fixed: 2,
    x: 3000,
    y: 1400,
    scientificNotation: true,
    hasAdditionalCondition: 11,
  },
  {
    name: 'Metano almacenado en volumen normal en tanque V101',
    variable: 'StorageH2_V101Volume',
    unit: 'NL',
    isShown: true,
    diagramName: 'H2',
    fixed: 2,
    x: 3000,
    y: 1550,
    scientificNotation: false,
    hasAdditionalCondition: 9,
  },
  {
    name: 'Concentración de metano almacenada en el tanque V101',
    variable: 'StorageH2_V101Concentration',
    unit: 'ppm',
    isShown: true,
    diagramName: 'H2',
    fixed: 0,
    x: 3000,
    y: 1550,
    scientificNotation: false,
    hasAdditionalCondition: 10,
  },
  {
    name: 'moles de metano almacenada en tanque V101',
    variable: 'StorageH2_V101moles',
    unit: 'mol',
    isShown: true,
    diagramName: 'H2',
    fixed: 2,
    x: 3000,
    y: 1550,
    scientificNotation: true,
    hasAdditionalCondition: 11,
  },
  {
    name: 'Metano almacenado en volumen normal en tanque V101',
    variable: 'StorageNH3_V101Volume',
    unit: 'NL',
    isShown: true,
    diagramName: 'NH3',
    fixed: 2,
    x: 3000,
    y: 1700,
    scientificNotation: false,
    hasAdditionalCondition: 9,
  },
  {
    name: 'Concentración de metano almacenada en el tanque V101',
    variable: 'StorageNH3_V101Concentration',
    unit: 'ppm',
    isShown: true,
    diagramName: 'NH3',
    fixed: 0,
    x: 3000,
    y: 1700,
    scientificNotation: false,
    hasAdditionalCondition: 10,
  },
  {
    name: 'moles de metano almacenada en tanque V101',
    variable: 'StorageNH3_V101moles',
    unit: 'mol',
    isShown: true,
    diagramName: 'NH3',
    fixed: 2,
    x: 3000,
    y: 1700,
    scientificNotation: true,
    hasAdditionalCondition: 11,
  },
  {
    name: 'moles de agua en V101',
    variable: 'moles_humidity_V101',
    unit: 'mol',
    isShown: true,
    diagramName: 'H2O',
    fixed: 2,
    x: 3000,
    y: 1850,
    scientificNotation: true,
    hasAdditionalCondition: 12,
  },
  {
    name: 'Humedad Relativa del biogás en V101',
    variable: 'Relative_humidity_V101',
    unit: '%',
    isShown: true,
    diagramName: 'H2O',
    fixed: 2,
    x: 3000,
    y: 1850,
    scientificNotation: false,
    hasAdditionalCondition: 13,
  },
  {
    name: 'Energía total almacenada_V101',
    variable: 'StorageEnergy_V101',
    unit: 'Wh',
    isShown: true,
    diagramName: 'Energía',
    fixed: 2,
    x: 3000,
    y: 2000,
    scientificNotation: false,
  },
  {
    name: 'Volumen normal de biogas acumulado',
    variable: 'AcumBiogasVolumenV102',
    unit: 'NL',
    isShown: true,
    diagramName: 'Vol',
    fixed: 2,
    x: 5400,
    y: 800,
    scientificNotation: false,
    hasAdditionalCondition: 5,
  },
  {
    name: 'Volumen normal de biogas almacenado',
    variable: 'StorageBiogasVolumeV102',
    unit: 'NL',
    isShown: true,
    diagramName: 'Vol',
    fixed: 2,
    x: 5400,
    y: 800,
    scientificNotation: false,
    hasAdditionalCondition: 6,
  },
  {
    name: 'Presión de biogás acumulado',
    variable: 'AcumBiogasPressureV102',
    unit: 'psi',
    isShown: true,
    diagramName: 'pres',
    fixed: 2,
    x: 5400,
    y: 800,
    scientificNotation: false,
    hasAdditionalCondition: 7,
  },
  {
    name: 'Presión de biogás almacenado',
    variable: 'StorageBiogasPressureV102',
    unit: 'psi',
    isShown: true,
    diagramName: 'pres',
    fixed: 2,
    x: 5400,
    y: 800,
    scientificNotation: false,
    hasAdditionalCondition: 8,
  },
  {
    name: 'Metano almacenado en volumen normal en tanque V102',
    variable: 'StorageCH4_V102Volume',
    unit: 'NL',
    isShown: true,
    diagramName: 'CH4',
    fixed: 2,
    x: 5400,
    y: 950,
    scientificNotation: false,
    hasAdditionalCondition: 9,
  },
  {
    name: 'Concentración de metano almacenada en el tanque V102',
    variable: 'StorageCH4_V102Concentration',
    unit: '%',
    isShown: true,
    diagramName: 'CH4',
    fixed: 2,
    x: 5400,
    y: 950,
    scientificNotation: false,
    hasAdditionalCondition: 10,
  },
  {
    name: 'moles de metano almacenada en tanque V102',
    variable: 'StorageCH4_V102moles',
    unit: 'mol',
    isShown: true,
    diagramName: 'CH4',
    fixed: 2,
    x: 5400,
    y: 950,
    scientificNotation: true,
    hasAdditionalCondition: 11,
  },
  {
    name: 'Metano almacenado en volumen normal en tanque V102',
    variable: 'StorageCO2_V102Volume',
    unit: 'NL',
    isShown: true,
    diagramName: 'CO2',
    fixed: 2,
    x: 5400,
    y: 1100,
    scientificNotation: false,
    hasAdditionalCondition: 9,
  },
  {
    name: 'Concentración de metano almacenada en el tanque V102',
    variable: 'StorageCO2_V102Concentration',
    unit: '%',
    isShown: true,
    diagramName: 'CO2',
    fixed: 2,
    x: 5400,
    y: 1100,
    scientificNotation: false,
    hasAdditionalCondition: 10,
  },
  {
    name: 'moles de metano almacenada en tanque V102',
    variable: 'StorageCO2_V102moles',
    unit: 'mol',
    isShown: true,
    diagramName: 'CO2',
    fixed: 2,
    x: 5400,
    y: 1100,
    scientificNotation: true,
    hasAdditionalCondition: 11,
  },
  {
    name: 'Metano almacenado en volumen normal en tanque V102',
    variable: 'StorageH2S_V102Volume',
    unit: 'NL',
    isShown: true,
    diagramName: 'H2S',
    fixed: 2,
    x: 5400,
    y: 1250,
    scientificNotation: false,
    hasAdditionalCondition: 9,
  },
  {
    name: 'Concentración de metano almacenada en el tanque V102',
    variable: 'StorageH2S_V102Concentration',
    unit: 'ppm',
    isShown: true,
    diagramName: 'H2S',
    fixed: 0,
    x: 5400,
    y: 1250,
    scientificNotation: false,
    hasAdditionalCondition: 10,
  },
  {
    name: 'moles de metano almacenada en tanque V102',
    variable: 'StorageH2S_V102moles',
    unit: 'mol',
    isShown: true,
    diagramName: 'H2S',
    fixed: 2,
    x: 5400,
    y: 1250,
    scientificNotation: true,
    hasAdditionalCondition: 11,
  },
  {
    name: 'Metano almacenado en volumen normal en tanque V102',
    variable: 'StorageO2_V102Volume',
    unit: 'NL',
    isShown: true,
    diagramName: 'O2',
    fixed: 2,
    x: 5400,
    y: 1400,
    scientificNotation: false,
    hasAdditionalCondition: 9,
  },
  {
    name: 'Concentración de metano almacenada en el tanque V102',
    variable: 'StorageO2_V102Concentration',
    unit: '%',
    isShown: true,
    diagramName: 'O2',
    fixed: 2,
    x: 5400,
    y: 1400,
    scientificNotation: false,
    hasAdditionalCondition: 10,
  },
  {
    name: 'moles de metano almacenada en tanque V102',
    variable: 'StorageO2_V102moles',
    unit: 'mol',
    isShown: true,
    diagramName: 'O2',
    fixed: 2,
    x: 5400,
    y: 1400,
    scientificNotation: true,
    hasAdditionalCondition: 11,
  },
  {
    name: 'Metano almacenado en volumen normal en tanque V102',
    variable: 'StorageH2_V102Volume',
    unit: 'NL',
    isShown: true,
    diagramName: 'H2',
    fixed: 2,
    x: 5400,
    y: 1550,
    scientificNotation: false,
    hasAdditionalCondition: 9,
  },
  {
    name: 'Concentración de metano almacenada en el tanque V102',
    variable: 'StorageH2_V102Concentration',
    unit: 'ppm',
    isShown: true,
    diagramName: 'H2',
    fixed: 0,
    x: 5400,
    y: 1550,
    scientificNotation: false,
    hasAdditionalCondition: 10,
  },
  {
    name: 'moles de metano almacenada en tanque V102',
    variable: 'StorageH2_V102moles',
    unit: 'mol',
    isShown: true,
    diagramName: 'H2',
    fixed: 2,
    x: 5400,
    y: 1550,
    scientificNotation: true,
    hasAdditionalCondition: 11,
  },
  {
    name: 'Metano almacenado en volumen normal en tanque V102',
    variable: 'StorageNH3_V102Volume',
    unit: 'NL',
    isShown: true,
    diagramName: 'NH3',
    fixed: 2,
    x: 5400,
    y: 1700,
    scientificNotation: false,
    hasAdditionalCondition: 9,
  },
  {
    name: 'Concentración de metano almacenada en el tanque V102',
    variable: 'StorageNH3_V102Concentration',
    unit: 'ppm',
    isShown: true,
    diagramName: 'NH3',
    fixed: 0,
    x: 5400,
    y: 1700,
    scientificNotation: false,
    hasAdditionalCondition: 10,
  },
  {
    name: 'moles de metano almacenada en tanque V102',
    variable: 'StorageNH3_V102moles',
    unit: 'mol',
    isShown: true,
    diagramName: 'NH3',
    fixed: 2,
    x: 5400,
    y: 1700,
    scientificNotation: true,
    hasAdditionalCondition: 11,
  },
  {
    name: 'moles de agua en V102',
    variable: 'moles_humidity_V102',
    unit: 'mol',
    isShown: true,
    diagramName: 'H2O',
    fixed: 2,
    x: 5400,
    y: 1850,
    scientificNotation: true,
    hasAdditionalCondition: 12,
  },
  {
    name: 'Humedad Relativa del biogás en V102',
    variable: 'Relative_humidity_V102',
    unit: '%',
    isShown: true,
    diagramName: 'H2O',
    fixed: 2,
    x: 5400,
    y: 1850,
    scientificNotation: false,
    hasAdditionalCondition: 13,
  },
  {
    name: 'Energía total almacenada_V102',
    variable: 'StorageEnergy_V102',
    unit: 'Wh',
    isShown: true,
    diagramName: 'Energía',
    fixed: 2,
    x: 5400,
    y: 2000,
    scientificNotation: false,
  },
  {
    name: 'moles de amoniaco adsorbidas',
    variable: 'ads_NH3_bt',
    unit: 'mol',
    isShown: true,
    diagramName: 'NH3',
    fixed: 2,
    x: 8200,
    y: 800,
    scientificNotation: false,
  },
  {
    name: 'moles de sulfuro de hidrógeno adsorbidas',
    variable: 'ads_H2S_bt',
    unit: 'mol',
    isShown: true,
    diagramName: 'H2S',
    fixed: 2,
    x: 8200,
    y: 950,
    scientificNotation: false,
  },
  {
    name: 'moles de agua adsorbidas',
    variable: 'ads_H2O_bt',
    unit: 'mol',
    isShown: true,
    diagramName: 'H2O',
    fixed: 2,
    x: 8200,
    y: 1100,
    scientificNotation: false,
  },
  {
    name: 'Eficiencia de adsorción',
    variable: 'x_bt',
    unit: '%',
    isShown: true,
    diagramName: 'x',
    fixed: 2,
    x: 8200,
    y: 1250,
    scientificNotation: false,
  },
  {
    name: 'Volumen normal de biogas acumulado',
    variable: 'AcumBiogasVolumenV107',
    unit: 'NL',
    isShown: true,
    diagramName: 'Vol',
    fixed: 2,
    x: 8400,
    y: 2500,
    scientificNotation: false,
    hasAdditionalCondition: 5,
  },
  {
    name: 'Volumen normal de biogas almacenado',
    variable: 'StorageBiogasVolumeV107',
    unit: 'NL',
    isShown: true,
    diagramName: 'Vol',
    fixed: 2,
    x: 8400,
    y: 2500,
    scientificNotation: false,
    hasAdditionalCondition: 6,
  },
  {
    name: 'Presión de biogás acumulado',
    variable: 'AcumBiogasPressureV107',
    unit: 'psi',
    isShown: true,
    diagramName: 'pres',
    fixed: 2,
    x: 8400,
    y: 2500,
    scientificNotation: false,
    hasAdditionalCondition: 7,
  },
  {
    name: 'Presión de biogás almacenado',
    variable: 'StorageBiogasPressureV107',
    unit: 'psi',
    isShown: true,
    diagramName: 'pres',
    fixed: 2,
    x: 8400,
    y: 2500,
    scientificNotation: false,
    hasAdditionalCondition: 8,
  },
  {
    name: 'Metano almacenado en volumen normal en tanque V107',
    variable: 'StorageCH4_V107Volume',
    unit: 'NL',
    isShown: true,
    diagramName: 'CH4',
    fixed: 2,
    x: 8400,
    y: 2650,
    scientificNotation: false,
    hasAdditionalCondition: 9,
  },
  {
    name: 'Concentración de metano almacenada en el tanque V107',
    variable: 'StorageCH4_V107Concentration',
    unit: '%',
    isShown: true,
    diagramName: 'CH4',
    fixed: 2,
    x: 8400,
    y: 2650,
    scientificNotation: false,
    hasAdditionalCondition: 10,
  },
  {
    name: 'moles de metano almacenada en tanque V107',
    variable: 'StorageCH4_V107moles',
    unit: 'mol',
    isShown: true,
    diagramName: 'CH4',
    fixed: 2,
    x: 8400,
    y: 2650,
    scientificNotation: true,
    hasAdditionalCondition: 11,
  },
  {
    name: 'Metano almacenado en volumen normal en tanque V107',
    variable: 'StorageCO2_V107Volume',
    unit: 'NL',
    isShown: true,
    diagramName: 'CO2',
    fixed: 2,
    x: 8400,
    y: 2800,
    scientificNotation: false,
    hasAdditionalCondition: 9,
  },
  {
    name: 'Concentración de metano almacenada en el tanque V107',
    variable: 'StorageCO2_V107Concentration',
    unit: '%',
    isShown: true,
    diagramName: 'CO2',
    fixed: 2,
    x: 8400,
    y: 2800,
    scientificNotation: false,
    hasAdditionalCondition: 10,
  },
  {
    name: 'moles de metano almacenada en tanque V107',
    variable: 'StorageCO2_V107moles',
    unit: 'mol',
    isShown: true,
    diagramName: 'CO2',
    fixed: 2,
    x: 8400,
    y: 2800,
    scientificNotation: true,
    hasAdditionalCondition: 11,
  },
  {
    name: 'Metano almacenado en volumen normal en tanque V107',
    variable: 'StorageH2S_V107Volume',
    unit: 'NL',
    isShown: true,
    diagramName: 'H2S',
    fixed: 2,
    x: 8400,
    y: 2950,
    scientificNotation: false,
    hasAdditionalCondition: 9,
  },
  {
    name: 'Concentración de metano almacenada en el tanque V107',
    variable: 'StorageH2S_V107Concentration',
    unit: 'ppm',
    isShown: true,
    diagramName: 'H2S',
    fixed: 0,
    x: 8400,
    y: 2950,
    scientificNotation: false,
    hasAdditionalCondition: 10,
  },
  {
    name: 'moles de metano almacenada en tanque V107',
    variable: 'StorageH2S_V107moles',
    unit: 'mol',
    isShown: true,
    diagramName: 'H2S',
    fixed: 2,
    x: 8400,
    y: 2950,
    scientificNotation: true,
    hasAdditionalCondition: 11,
  },
  {
    name: 'Metano almacenado en volumen normal en tanque V107',
    variable: 'StorageO2_V107Volume',
    unit: 'NL',
    isShown: true,
    diagramName: 'O2',
    fixed: 2,
    x: 8400,
    y: 3100,
    scientificNotation: false,
    hasAdditionalCondition: 9,
  },
  {
    name: 'Concentración de metano almacenada en el tanque V107',
    variable: 'StorageO2_V107Concentration',
    unit: '%',
    isShown: true,
    diagramName: 'O2',
    fixed: 2,
    x: 8400,
    y: 3100,
    scientificNotation: false,
    hasAdditionalCondition: 10,
  },
  {
    name: 'moles de metano almacenada en tanque V107',
    variable: 'StorageO2_V107moles',
    unit: 'mol',
    isShown: true,
    diagramName: 'O2',
    fixed: 2,
    x: 8400,
    y: 3100,
    scientificNotation: true,
    hasAdditionalCondition: 11,
  },
  {
    name: 'Metano almacenado en volumen normal en tanque V107',
    variable: 'StorageH2_V107Volume',
    unit: 'NL',
    isShown: true,
    diagramName: 'H2',
    fixed: 2,
    x: 8400,
    y: 3250,
    scientificNotation: false,
    hasAdditionalCondition: 9,
  },
  {
    name: 'Concentración de metano almacenada en el tanque V107',
    variable: 'StorageH2_V107Concentration',
    unit: 'ppm',
    isShown: true,
    diagramName: 'H2',
    fixed: 0,
    x: 8400,
    y: 3250,
    scientificNotation: false,
    hasAdditionalCondition: 10,
  },
  {
    name: 'moles de metano almacenada en tanque V107',
    variable: 'StorageH2_V107moles',
    unit: 'mol',
    isShown: true,
    diagramName: 'H2',
    fixed: 2,
    x: 8400,
    y: 3250,
    scientificNotation: true,
    hasAdditionalCondition: 11,
  },
  {
    name: 'Metano almacenado en volumen normal en tanque V107',
    variable: 'StorageNH3_V107Volume',
    unit: 'NL',
    isShown: true,
    diagramName: 'NH3',
    fixed: 2,
    x: 8400,
    y: 3400,
    scientificNotation: false,
    hasAdditionalCondition: 9,
  },
  {
    name: 'Concentración de metano almacenada en el tanque V107',
    variable: 'StorageNH3_V107Concentration',
    unit: 'ppm',
    isShown: true,
    diagramName: 'NH3',
    fixed: 0,
    x: 8400,
    y: 3400,
    scientificNotation: false,
    hasAdditionalCondition: 10,
  },
  {
    name: 'moles de metano almacenada en tanque V107',
    variable: 'StorageNH3_V107moles',
    unit: 'mol',
    isShown: true,
    diagramName: 'NH3',
    fixed: 2,
    x: 8400,
    y: 3400,
    scientificNotation: true,
    hasAdditionalCondition: 11,
  },
  {
    name: 'moles de agua en V107',
    variable: 'moles_humidity_V107',
    unit: 'mol',
    isShown: true,
    diagramName: 'H2O',
    fixed: 2,
    x: 8400,
    y: 3550,
    scientificNotation: true,
    hasAdditionalCondition: 12,
  },
  {
    name: 'Humedad Relativa del biogás en V107',
    variable: 'Relative_humidity_V107',
    unit: '%',
    isShown: true,
    diagramName: 'H2O',
    fixed: 2,
    x: 8400,
    y: 3550,
    scientificNotation: false,
    hasAdditionalCondition: 13,
  },
  {
    name: 'Energía total almacenada_V107',
    variable: 'StorageEnergy_V107',
    unit: 'Wh',
    isShown: true,
    diagramName: 'Energía',
    fixed: 2,
    x: 8400,
    y: 3700,
    scientificNotation: false,
  },
];

export const BIOGAS_MODE2: DiagramVariableType[] = [
  ...BIOGAS_MODE1,
  {
    name: 'Flujo volumétrico de la bomba P101',
    variable: 'Pump101Flow',
    unit: 'L/h',
    isShown: true,
    diagramName: 'Caudal',
    fixed: 2,
    x: 3100,
    y: 4600,
    scientificNotation: false,
  },
];

export const BIOGAS_MODE3: DiagramVariableType[] = [
  ...BIOGAS_MODE2,
  {
    name: 'Velocidad de agitación reactor R102',
    variable: 'Mix_Velocity_R102',
    unit: 'RPM',
    isShown: true,
    diagramName: 'RPM',
    fixed: 0,
    x: 6300,
    y: 3800,
    scientificNotation: false,
  },
  {
    name: 'pH',
    variable: 'pH_R102',
    unit: '',
    isShown: true,
    diagramName: 'pH',
    fixed: 2,
    x: 6300,
    y: 3950,
    scientificNotation: false,
  },
  {
    name: 'Temperatura R102',
    variable: 'Temp_R102',
    unit: '°c',
    isShown: true,
    diagramName: 'Temperatura',
    fixed: 2,
    x: 6300,
    y: 4100,
    scientificNotation: false,
  },
  {
    name: 'Parámetro cinético preexponencias Arrhenius,  ADM1 y  Gompertz',
    variable: 'K_R102',
    unit: 'L/s',
    isShown: true,
    diagramName: 'K',
    fixed: 2,
    x: 4500,
    y: 6200,
    scientificNotation: true,
    hasAdditionalCondition: 0,
  },
  {
    name: 'Parámetro cinético preexponencias Arrhenius,  ADM1 y  Gompertz',
    variable: 'K_R102',
    unit: 'L / gSV',
    isShown: true,
    diagramName: 'ym',
    fixed: 2,
    x: 4500,
    y: 6200,
    scientificNotation: true,
    hasAdditionalCondition: 1,
  },
  {
    name: 'Parámetro cinético energía de activación',
    variable: 'Ea_R102',
    unit: 'J/mol',
    isShown: true,
    diagramName: 'Ea',
    fixed: 2,
    x: 4500,
    y: 6350,
    scientificNotation: true,
    hasAdditionalCondition: 2,
  },
  {
    name: 'Parámetro cinético energía de activación',
    variable: 'Ea_R102',
    unit: 'L / gSV-s',
    isShown: true,
    diagramName: 'U',
    fixed: 2,
    x: 4500,
    y: 6350,
    scientificNotation: true,
    hasAdditionalCondition: 3,
  },
  {
    name: 'Tiempo de retraso o periodo de tiempo mínimo para producir biogás',
    variable: 'Lambda_R102',
    unit: 's',
    isShown: true,
    diagramName: 'λ',
    fixed: 2,
    x: 4500,
    y: 6500,
    scientificNotation: true,
    hasAdditionalCondition: 3,
  },
  {
    name: 'Concentración de sólidos volátiles en gSV/L',
    variable: 'C_sv_R102',
    unit: 'gSV/L',
    isShown: true,
    diagramName: 'Csv',
    fixed: 2,
    x: 5500,
    y: 6200,
    scientificNotation: true,
  },
  {
    name: 'Concentración de sólidos volátiles en %',
    variable: 'SV_R102',
    unit: '%',
    isShown: true,
    diagramName: 'SV',
    fixed: 2,
    x: 5500,
    y: 6350,
    scientificNotation: false,
  },
  {
    name: 'Concentración de sólidos totales en gST/L',
    variable: 'C_st_R102',
    unit: 'gST/L',
    isShown: true,
    diagramName: 'Cst',
    fixed: 2,
    x: 5500,
    y: 6500,
    scientificNotation: true,
  },
  {
    name: 'Concentración de sólidos totales en %',
    variable: 'ST_R102',
    unit: '%',
    isShown: true,
    diagramName: 'ST',
    fixed: 2,
    x: 5500,
    y: 6650,
    scientificNotation: false,
  },
  {
    name: 'Carga Orgánica en el reactor R102',
    variable: 'Organic_Charge_R102',
    unit: 'gSV/L-dia',
    isShown: true,
    diagramName: 'OC',
    fixed: 2,
    x: 5500,
    y: 6800,
    scientificNotation: true,
  },
  {
    name: 'Conversión del reactivo límite',
    variable: 'x_R102',
    unit: '%',
    isShown: true,
    diagramName: 'x',
    fixed: 2,
    x: 5500,
    y: 6950,
    scientificNotation: false,
  },
];

export const BIOGAS_MODE4_5: DiagramVariableType[] = [
  ...BIOGAS_MODE3,
  {
    name: 'Flujo volumétrico de la bomba P102',
    variable: 'Pump102Flow',
    unit: 'L/h',
    isShown: true,
    diagramName: 'Caudal',
    fixed: 2,
    x: 6300,
    y: 4600,
    scientificNotation: false,
  },
];
