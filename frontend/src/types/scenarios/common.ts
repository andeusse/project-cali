import {
  CommonSystemParameter,
  SolarPanel as CommonSolarPanel,
  MONOCRYSTALLINE_PANEL,
} from '../common';
import { InputType } from '../inputType';
import { v4 as uuidv4 } from 'uuid';

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

export enum ScenariosSolarPanelMeteorologicalInformationType {
  Custom = 'Custom',
  Fixed = 'Fixed',
  Typical = 'Typical',
}

export enum ScenariosSolarPanelMeteorologicalInformationText {
  Custom = 'Perfil personalizado',
  Fixed = 'Perfil fijo',
  Typical = 'Perfil típico',
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

export type SolarPanel = CommonSystemParameter &
  CommonSolarPanel & {
    id: string;
    modulesNumber: InputType;
    modulePower: InputType;
    meteorologicalInformationMode: ScenariosSolarPanelMeteorologicalInformationType;
    moduleType: SolarPanelModuleType;
    radiation: InputType;
    temperature: InputType;
    radiationArray: number[];
    temperatureArray: number[];
  };

export enum SmartSystemType {
  Solar = 'Solar',
  Biogas = 'Biogas',
  Load = 'Load',
  Battery = 'Battery',
  Hydraulic = 'Hydraulic',
  Wind = 'Wind',
}

export type CommonScenarioParameters = CommonSystemParameter & {
  operationMode: ScenariosModesType;
  steps: InputType;
  stepTime: InputType;
  stepUnit: ScenariosStepUnitType;
  solarSystemNumber: InputType;
  biogasSystemNumber: InputType;
  loadSystemNumber: InputType;
  solarPanels: SolarPanel[];
};

export const COMMON_SOLAR_PANEL: SolarPanel = {
  id: uuidv4(),
  name: 'Sistema solar',
  modulesNumber: {
    disabled: false,
    value: 10,
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
  meteorologicalInformationMode:
    ScenariosSolarPanelMeteorologicalInformationType.Custom,
  moduleType: SolarPanelModuleType.MonocrystallinePanel,
  ...MONOCRYSTALLINE_PANEL,
  radiation: {
    disabled: false,
    value: 800,
    tooltip: 'Radiación solar',
    unit: 'W / m²',
    variableString: 'Radiación solar',
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
  radiationArray: Array(24).fill(0),
  temperatureArray: Array(24).fill(0),
};

export const COMMON_SCENARIO: CommonScenarioParameters = {
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
  stepUnit: ScenariosStepUnitType.Second,
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
  solarPanels: [{ ...COMMON_SOLAR_PANEL }],
};
