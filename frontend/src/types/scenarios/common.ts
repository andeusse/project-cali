import {
  CommonSystemParameter,
  SolarPanel as CommonSolarPanel,
  WindTurbine,
  MONOCRYSTALLINE_PANEL,
  GEL_BATTERY,
  PELTON_TURBINE,
  LABORATORY_WIND_TURBINE,
  EXAMPLE_BIOGAS,
} from '../common';
import { InputType } from '../inputType';
import { v4 as uuidv4 } from 'uuid';
import { CellChange } from '@silevis/reactgrid';

export type TabProps = {
  system: SmartSystemParameters;
  handleSystemChange: (e: any, id: string, type: SmartSystemType) => void;
  handleTableChange: (
    e: CellChange[],
    id: string,
    type: SmartSystemType
  ) => void;
};

export type SetSystemArrayType<T> = {
  e: CellChange[];
  oldState: T;
  id: string;
};

export enum SmartSystemType {
  Solar = 'Solar',
  Biogas = 'Biogas',
  Load = 'Load',
  Battery = 'Battery',
  Hydraulic = 'Hydraulic',
  Wind = 'Wind',
}

export enum ScenariosModesType {
  Manual = 'Manual',
  Automatic = 'Automatic',
}

export enum ScenariosModesText {
  Manual = 'Manual',
  Automatic = 'Automático',
}

export enum ScenariosStepUnitType {
  Second = 'Second',
  Minute = 'Minute',
  Hour = 'Hour',
  Day = 'Day',
}

export enum ScenariosStepUnitText {
  Second = 'Segundo(s)',
  Minute = 'Minutos(s)',
  Hour = 'Hora(s)',
  Day = 'Día(s)',
}

export enum ScenariosCommonInputInformationType {
  Custom = 'Custom',
  Fixed = 'Fixed',
}

export enum ScenariosCommonInputInformationText {
  Custom = 'Perfil personalizado',
  Fixed = 'Perfil fijo',
}

export enum ScenariosSolarWindInputInformationType {
  Custom = 'Custom',
  Fixed = 'Fixed',
  Typical = 'Typical',
}

export enum ScenariosSolarWindInputInformationText {
  Custom = 'Perfil personalizado',
  Fixed = 'Perfil fijo',
  Typical = 'Perfil típico',
}

export enum ScenariosLoadInputInformationType {
  Custom = 'Custom',
  Fixed = 'Fixed',
  Residential = 'Residential',
  Commercial = 'Commercial',
  Industrial = 'Industrial',
}

export enum ScenariosLoadInputInformationText {
  Custom = 'Perfil personalizado',
  Fixed = 'Fijo',
  Residential = 'Perfil típico residencial',
  Commercial = 'Perfil típico comercial',
  Industrial = 'Perfil típico industrial',
}

export enum SolarPanelModuleType {
  MonocrystallinePanel = 'MonocrystallinePanel',
  PolicrystallinePanel = 'PolicrystallinePanel',
  FlexPanel = 'FlexPanel',
  CadmiumTelluridePanel = 'CadmiumTelluridePanel',
  Custom = 'Custom',
}

export enum SolarPanelModuleText {
  MonocrystallinePanel = 'Monocristalino',
  PolicrystallinePanel = 'Policristalino',
  FlexPanel = 'Monocristalino flexible',
  CadmiumTelluridePanel = 'Telururo de cadmio',
  Custom = 'Personalizado',
}

export enum BatteryType {
  Gel = 'Gel',
  Custom = 'Custom',
}

export enum BatteryText {
  Gel = 'Gel (Laboratorio)',
  Custom = 'Personalizado',
}

export enum HydraulicType {
  Pelton = 'Pelton',
  Turgo = 'Turgo',
  Custom = 'Custom',
}

export enum HydraulicText {
  Pelton = 'Pelton (Laboratorio)',
  Turgo = 'Turgo (Laboratorio)',
  Custom = 'Personalizado',
}

export enum WindType {
  Laboratory = 'Laboratory',
  Custom = 'Custom',
}

export enum WindText {
  Laboratory = 'Turbina laboratorio',
  Custom = 'Personalizado',
}

export enum BiogasType {
  Laboratory = 'Laboratory',
  Custom = 'Custom',
}

export enum BiogasText {
  Laboratory = 'Planta ejemplo',
  Custom = 'Personalizado',
}

export enum BiogasPhaseType {
  Phase1 = 'Phase1',
  Phase2 = 'Phase2',
}

export enum BiogasPhaseText {
  Phase1 = 'Una etapa',
  Phase2 = 'Dos etapas',
}

export type SolarSystem = CommonSystemParameter &
  CommonSolarPanel & {
    id: string;
    modulesNumber: InputType;
    modulePower: InputType;
    type: SolarPanelModuleType;
    informationMode: ScenariosSolarWindInputInformationType;
    radiation: InputType;
    temperature: InputType;
    radiationArray: number[];
    temperatureArray: number[];
  };

export type BatteryTypeParameters = {
  selfDischargeCoefficient: InputType;
  chargeEfficiency: InputType;
  dischargeEfficiency: InputType;
};

export type BatterySystem = CommonSystemParameter &
  BatteryTypeParameters & {
    id: string;
    storageCapacity: InputType;
    maxChargePower: InputType;
    maxDischargePower: InputType;
    stateOfCharge: InputType;
    type: BatteryType;
    informationMode: ScenariosCommonInputInformationType;
    chargePower: InputType;
    dischargePower: InputType;
    chargePowerArray: number[];
    dischargePowerArray: number[];
  };

export type HydraulicTypeParameters = {
  efficiency: InputType;
  frictionLosses: InputType;
  minimumWaterHead: InputType;
  maximumWaterHead: InputType;
  minimumWaterFlow: InputType;
  maximumWaterFlow: InputType;
};

export type HydraulicSystem = CommonSystemParameter &
  HydraulicTypeParameters & {
    id: string;
    turbineNumber: InputType;
    nominalPower: InputType;
    type: HydraulicType;
    informationMode: ScenariosCommonInputInformationType;
    waterHead: InputType;
    waterFlow: InputType;
    waterHeadArray: number[];
    waterFlowArray: number[];
  };

export type WindTypeParameters = WindTurbine & {
  surfaceRoughnessLength: InputType;
};

export type WindSystem = CommonSystemParameter &
  WindTypeParameters & {
    id: string;
    turbineNumber: InputType;
    nominalPower: InputType;
    airDensity: InputType;
    type: WindType;
    informationMode: ScenariosSolarWindInputInformationType;
    windSpeed: InputType;
    windSpeedArray: number[];
  };

export type BiogasTypeParamenters = {
  reactorVolume1: InputType;
  reactorVolume2: InputType;
  diameterHeightRatio1: InputType;
  diameterHeightRatio2: InputType;
  heatTransferCoefficient1: InputType;
  heatTransferCoefficient2: InputType;
  temperatureSetpoint1: InputType;
  temperatureSetpoint2: InputType;
  controllerTolerance1: InputType;
  controllerTolerance2: InputType;
  carbonConcentration: InputType;
  hydrogenConcentration: InputType;
  oxygenConcentration: InputType;
  sulfurConcentration: InputType;
  totalConcentration: InputType;
  substrateDensity: InputType;
  substrateTemperature: InputType;
  substratePressure: InputType;
  substrateFlow: InputType;
  substratePresurreDrop: InputType;
};

export type BiogasSystem = CommonSystemParameter &
  BiogasTypeParamenters & {
    id: string;
    stabilizationDays: InputType;
    ambientPressure: InputType;
    ambientTemperature: InputType;
    electricGeneratorPower: InputType;
    electricGeneratorEfficiency: InputType;
    type: BiogasType;
    phaseNumber: BiogasPhaseType;
  };

export type LoadSystem = CommonSystemParameter & {
  id: string;
  informationMode: ScenariosLoadInputInformationType;
  power: InputType;
  peakPower: InputType;
  powerArray: number[];
};

export type SortableItemParameter = {
  id: string;
  name: string;
};

export type SmartSystemParameters = CommonSystemParameter & {
  operationMode: ScenariosModesType;
  steps: InputType;
  stepTime: InputType;
  stepUnit: ScenariosStepUnitType;
  solarSystemNumber: InputType;
  biogasSystemNumber: InputType;
  loadSystemNumber: InputType;
  houseArea: InputType;
  batterySystemNumber: InputType;
  hydraulicSystemNumber: InputType;
  windSystemNumber: InputType;
  priorityList: SortableItemParameter[];
  solarSystems: SolarSystem[];
  biogasSystems: BiogasSystem[];
  loadSystems: LoadSystem[];
  batterySystems: BatterySystem[];
  hydraulicSystems: HydraulicSystem[];
  windSystems: WindSystem[];
};

export type SmartSystemOutput = {
  columns: string[];
  index: number[];
  data: number[][];
};

export const COMMON_SOLAR_SYSTEM: SolarSystem = {
  id: uuidv4(),
  name: 'Sistema solar 1',
  modulesNumber: {
    disabled: false,
    value: 100,
    tooltip: 'Número de módulos solares',
    unit: '',
    variableString: 'Módulos solares',
    min: 1,
    max: 100000,
  },
  modulePower: {
    disabled: false,
    value: 500,
    tooltip: 'Potencia pico de cada módulo',
    unit: 'W',
    variableString: 'Potencia pico',
    min: 1,
    max: 1000,
  },
  informationMode: ScenariosSolarWindInputInformationType.Typical,
  type: SolarPanelModuleType.MonocrystallinePanel,
  ...MONOCRYSTALLINE_PANEL,
  radiation: {
    disabled: false,
    value: 1000,
    tooltip: 'Irradiancia solar máxima',
    unit: 'W / m²',
    variableString: 'Irradiancia solar máxima',
    min: 0,
    max: 2000,
    step: 100,
  },
  temperature: {
    disabled: false,
    value: 25,
    tooltip: 'Temperatura ambiente máxima',
    unit: '°C',
    variableString: 'Temperatura ambiente máxima',
    min: 0,
    max: 50,
  },
  radiationArray: Array(24).fill(800),
  temperatureArray: Array(24).fill(23),
};

export const COMMON_BATTERY_SYSTEM: BatterySystem = {
  id: uuidv4(),
  name: 'Sistema de baterías 1',
  storageCapacity: {
    disabled: false,
    value: 10,
    tooltip: 'Capacidad de almacenamiento',
    unit: 'kWh',
    variableString: 'Capacidad almacenamiento',
    min: 0.1,
    max: 10000,
    step: 0.1,
  },
  maxChargePower: {
    disabled: false,
    value: 10,
    tooltip: 'Potencia máxima de carga',
    unit: 'kW',
    variableString: 'Potencia máxima de carga',
    min: 0.1,
    max: 10000,
    step: 0.1,
  },
  maxDischargePower: {
    disabled: false,
    value: 10,
    tooltip: 'Potencia máxima de descarga',
    unit: 'kW',
    variableString: 'Potencia máxima de descarga',
    min: 0.1,
    max: 10000,
    step: 0.1,
  },
  stateOfCharge: {
    disabled: false,
    value: 100,
    tooltip: 'Estado de carga inicial',
    unit: '',
    variableString: 'SOC',
    min: 0,
    max: 100,
  },
  informationMode: ScenariosCommonInputInformationType.Fixed,
  type: BatteryType.Gel,
  ...GEL_BATTERY,
  chargePower: {
    disabled: false,
    value: 5,
    tooltip: 'Potencia de carga',
    unit: 'kW',
    variableString: 'Potencia de carga',
    min: 0,
    max: 10,
  },
  dischargePower: {
    disabled: false,
    value: 5,
    tooltip: 'Potencia de descarga',
    unit: 'kW',
    variableString: 'Potencia de descarga',
    min: 0,
    max: 10,
  },
  chargePowerArray: Array(24).fill(5),
  dischargePowerArray: Array(24).fill(5),
};

export const COMMON_HYDRAULIC_SYSTEM: HydraulicSystem = {
  id: uuidv4(),
  name: 'Sistema de turbinas 1',
  turbineNumber: {
    disabled: false,
    value: 10,
    tooltip: 'Número de turbinas',
    unit: '',
    variableString: 'Número de turbinas',
    min: 1,
    max: 100,
  },
  nominalPower: {
    disabled: false,
    value: 5,
    tooltip: 'Potencia nominal de cada turbina',
    unit: 'kW',
    variableString: 'Potencia nominal',
    min: 0.1,
    max: 100000,
    step: 0.1,
  },
  type: HydraulicType.Pelton,
  informationMode: ScenariosCommonInputInformationType.Fixed,
  ...PELTON_TURBINE,
  waterHead: {
    disabled: false,
    value: 65,
    tooltip: 'Cabeza de agua',
    unit: 'm',
    variableString: 'Cabeza de agua',
    min: 3,
    max: 130,
  },
  waterFlow: {
    disabled: false,
    value: 0.005,
    tooltip: 'Flujo de agua',
    unit: 'm³ / s',
    variableString: 'Flujo de agua',
    min: 0.0001,
    max: 0.01,
  },
  waterHeadArray: Array(24).fill(65),
  waterFlowArray: Array(24).fill(0.005),
};

export const COMMON_WIND_SYSTEM: WindSystem = {
  id: uuidv4(),
  name: 'Sistema eólico 1',
  turbineNumber: {
    disabled: false,
    value: 10,
    tooltip: 'Número de turbinas',
    unit: '',
    variableString: 'Número de turbinas',
    min: 1,
    max: 100,
  },
  nominalPower: {
    disabled: false,
    value: 5,
    tooltip: 'Potencia nominal de cada turbina',
    unit: 'kW',
    variableString: 'Potencia nominal',
    min: 0.1,
    max: 100000,
    step: 0.1,
  },
  airDensity: {
    disabled: false,
    value: 1.112,
    tooltip: 'Densidad del aire',
    unit: 'kg / m³',
    variableString: 'Densidad del aire',
    min: 0.1,
    max: 10,
    step: 0.1,
  },
  type: WindType.Laboratory,
  informationMode: ScenariosSolarWindInputInformationType.Typical,
  ...LABORATORY_WIND_TURBINE,
  windSpeed: {
    disabled: false,
    value: 11.5,
    tooltip: 'Velocidad del viento máxima',
    unit: 'm / s',
    variableString: 'Velocidad del viento máxima',
    min: 2,
    max: 65,
  },
  windSpeedArray: Array(24).fill(11.5),
};

export const COMMON_BIOGAS_SYSTEM: BiogasSystem = {
  id: uuidv4(),
  name: 'Sistema de biogas 1',
  stabilizationDays: {
    disabled: false,
    value: 90,
    tooltip: 'Días de estabilización',
    unit: 'días',
    variableString: 'Días de estabilización',
    min: 1,
    max: 365,
  },
  ambientPressure: {
    disabled: false,
    value: 101.323,
    tooltip: 'Presión ambiente',
    unit: 'kPa',
    variableString: 'Presión ambiente',
    min: 1,
    max: 200,
  },
  ambientTemperature: {
    disabled: false,
    value: 25,
    tooltip: 'Temperatura ambiente',
    unit: '°C',
    variableString: 'Temperatura ambiente',
    min: 5,
    max: 40,
  },
  electricGeneratorPower: {
    disabled: false,
    value: 10,
    tooltip: 'Potencia de generador eléctrico',
    unit: 'kW',
    variableString: 'Potencia de generador eléctrico',
    min: 0.1,
    max: 100000,
    step: 0.1,
  },
  electricGeneratorEfficiency: {
    disabled: false,
    value: 30,
    tooltip: 'Eficiencia de generador eléctrico',
    unit: '%',
    variableString: 'Eficiencia de generador eléctrico',
    min: 1,
    max: 100,
  },
  type: BiogasType.Laboratory,
  phaseNumber: BiogasPhaseType.Phase1,
  ...EXAMPLE_BIOGAS,
};

export const COMMON_LOAD_SYSTEM: LoadSystem = {
  id: uuidv4(),
  name: 'Carga 1',
  informationMode: ScenariosLoadInputInformationType.Commercial,
  power: {
    disabled: false,
    value: 100,
    tooltip: 'Potencia de demanda',
    unit: 'kW',
    variableString: 'Potencia de demanda',
    min: 0.1,
    max: 1000000,
    step: 0.1,
  },
  peakPower: {
    disabled: false,
    value: 100,
    tooltip: 'Potencia de demanda pico',
    unit: 'kW',
    variableString: 'Potencia de demanda pico',
    min: 0.1,
    max: 1000000,
    step: 0.1,
  },
  powerArray: Array(24).fill(100),
};

export const COMMON_SCENARIO: SmartSystemParameters = {
  name: 'Nombre',
  operationMode: ScenariosModesType.Manual,
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
  stepUnit: ScenariosStepUnitType.Hour,
  solarSystemNumber: {
    disabled: false,
    value: 1,
    tooltip: 'Número de sistemas solares',
    unit: '',
    variableString: 'Sistemas solares',
    min: 0,
    max: 100,
  },
  biogasSystemNumber: {
    disabled: false,
    value: 1,
    tooltip: 'Número de sistemas de biogás',
    unit: '',
    variableString: 'Sistemas de biogás',
    min: 0,
    max: 100,
  },
  loadSystemNumber: {
    disabled: false,
    value: 1,
    tooltip: 'Número de cargas',
    unit: '',
    variableString: 'Número de cargas',
    min: 1,
    max: 100,
  },
  houseArea: {
    disabled: false,
    value: 100,
    tooltip: 'Área de la casa',
    unit: 'm²',
    variableString: 'Área de la casa',
    min: 1,
    max: 1000,
  },
  batterySystemNumber: {
    disabled: false,
    value: 1,
    tooltip: 'Número de sistemas de baterías',
    unit: '',
    variableString: 'Sistemas de baterías',
    min: 0,
    max: 100,
  },
  hydraulicSystemNumber: {
    disabled: false,
    value: 1,
    tooltip: 'Número de sistemas hidráulicos',
    unit: '',
    variableString: 'Sistemas hidráulicos',
    min: 0,
    max: 100,
  },
  windSystemNumber: {
    disabled: false,
    value: 1,
    tooltip: 'Número de sistemas de eólicos',
    unit: '',
    variableString: 'Sistemas eólicos',
    min: 0,
    max: 100,
  },
  solarSystems: [{ ...COMMON_SOLAR_SYSTEM }],
  batterySystems: [{ ...COMMON_BATTERY_SYSTEM }],
  hydraulicSystems: [{ ...COMMON_HYDRAULIC_SYSTEM }],
  biogasSystems: [{ ...COMMON_BIOGAS_SYSTEM }],
  loadSystems: [{ ...COMMON_LOAD_SYSTEM }],
  windSystems: [{ ...COMMON_WIND_SYSTEM }],
  priorityList: [
    {
      id: COMMON_SOLAR_SYSTEM.id,
      name: COMMON_SOLAR_SYSTEM.name,
    },
    {
      id: COMMON_HYDRAULIC_SYSTEM.id,
      name: COMMON_HYDRAULIC_SYSTEM.name,
    },
    {
      id: COMMON_BIOGAS_SYSTEM.id,
      name: COMMON_BIOGAS_SYSTEM.name,
    },
    {
      id: COMMON_WIND_SYSTEM.id,
      name: COMMON_WIND_SYSTEM.name,
    },
  ],
};

export const SMART_CITY: SmartSystemParameters = {
  ...COMMON_SCENARIO,
};

export const SMART_FACTORY: SmartSystemParameters = {
  ...SMART_CITY,
};

export const SMART_HOME: SmartSystemParameters = {
  ...SMART_CITY,
  solarSystemNumber: {
    ...SMART_CITY.solarSystemNumber,
    max: 10,
  },
};
