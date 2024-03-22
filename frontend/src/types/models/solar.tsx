import {
  CommonDigitalTwinsParameter,
  CommonSystemParameter,
  DiagramVariableType,
  InputType,
} from './common';

export enum SolarPanelModulesType {
  Custom = 'Custom',
  Monocrystalline = 'Monocristalino',
  Policrystalline = 'Policristalino',
  MonocrystallineThin = 'Monocristalino película delgada',
  CadmiumTelluride = 'Telururo de Cadmio',
}

export type SolarPanelParameters = CommonSystemParameter &
  CommonDigitalTwinsParameter & {
    panelType: SolarPanelModulesType;
    moduleNumber: InputType;
    modulePeakPower: InputType;
    moduleReductionPowerFactor: InputType;
    moduleEfficiency: InputType;
    moduleStandardTestIrradiation: InputType;
    moduleStantardTestTemperature: InputType;
    moduleStandardIrradiation: InputType;
    moduleStandardTemperature: InputType;
    moduleEnvironmentTemperature: InputType;
    moduleCoefficientPowerVariation: InputType;
    inputOfflineOperation: boolean;
    inputIrradiation: InputType;
    inputTemperature: InputType;
  };

export const SOLAR_PANEL: SolarPanelParameters = {
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
  panelType: SolarPanelModulesType.Custom,
  moduleNumber: {
    disabled: false,
    value: 1,
    tooltip: 'Cantidad de módulos solares',
    unit: '',
    variableString: 'Número de módulos',
    min: 1,
  },
  modulePeakPower: {
    disabled: false,
    value: 100,
    tooltip: 'Potencia pico de cada módulo',
    unit: 'W',
    variableString: 'Potencia pico / módulo',
    min: 0,
    step: 10,
  },
  moduleReductionPowerFactor: {
    disabled: false,
    value: 1,
    tooltip:
      'Factor de reducción de la potencia del módulo de acuerdo con los años de operación',
    unit: '',
    variableString: 'f',
    variableSubString: 'pu',
    min: 0,
    max: 1,
    step: 0.01,
  },
  moduleEfficiency: {
    disabled: false,
    value: 15.44,
    tooltip: 'Eficiencia eléctrica del módulo',
    unit: '%',
    variableString: 'η',
    variableSubString: 'C',
    min: 0.01,
    max: 100,
    step: 0.01,
  },
  moduleStandardTestIrradiation: {
    disabled: false,
    value: 1000,
    tooltip:
      'Irradiancia solar en condiciones estándar de prueba del módulo, típicamente 1000 W/m²',
    unit: 'W / m²',
    variableString: 'G',
    variableSubString: 'STC',
    min: 0,
    step: 10,
  },
  moduleStantardTestTemperature: {
    disabled: false,
    value: 25,
    tooltip:
      'Temperatura del módulo fotovoltaico en condiciones estándar de prueba, típicamente 25 °C',
    unit: '°C',
    variableString: 'Tc',
    variableSubString: 'STC',
    min: 0,
    step: 0.01,
  },
  moduleStandardIrradiation: {
    disabled: false,
    value: 800,
    tooltip: 'Irradiancia normal de operación del módulo, típicamente 800 W/m²',
    unit: 'W / m²',
    variableString: 'G',
    variableSubString: 'NOCT',
    min: 0,
    step: 10,
  },
  moduleStandardTemperature: {
    disabled: false,
    value: 45,
    tooltip:
      'Temperatura nominal de operación del módulo, típicamente 45-48 °C',
    unit: '°C',
    variableString: 'Tc',
    variableSubString: 'NOCT',
    min: 0,
    step: 0.01,
  },
  moduleEnvironmentTemperature: {
    disabled: false,
    value: 20,
    tooltip:
      'Temperatura ambiente normal de operación del módulo, típicamente 20 °C',
    unit: '°C',
    variableString: 'Ta',
    variableSubString: 'NOCT',
    min: 0,
    step: 0.01,
  },
  moduleCoefficientPowerVariation: {
    disabled: false,
    value: -0.4,
    tooltip:
      'Coeficiente de variación de la potencia con la temperatura en la condición de extracción de máxima potencia',
    unit: '% / °C',
    variableString: 'μ',
    variableSubString: 'pm',
    step: 0.01,
  },
  inputOfflineOperation: false,
  inputIrradiation: {
    disabled: true,
    value: 1000,
    tooltip: 'Irradiancia de los módulos',
    unit: 'W / m²',
    variableString: 'Irradiancia',
    min: 0,
  },
  inputTemperature: {
    disabled: true,
    value: 25,
    tooltip: 'Temperatura de los módulos',
    unit: '°C',
    variableString: 'Temperatura',
    min: 0,
  },
};

export const SOLAR_DIAGRAM_VARIABLES: DiagramVariableType[] = [
  {
    name: '',
    variable: 'v1',
    x: 100,
    y: 220,
    diagramName: 'Irradiancia',
    unit: 'W / m²',
    fixed: 2,
    isShown: true,
  },
  {
    name: '',
    variable: 'v2',
    x: 655,
    y: 50,
    diagramName: 'T_ambiente',
    unit: '°C',
    fixed: 1,
    isShown: true,
  },
  {
    name: '',
    variable: 'v3',
    x: 700,
    y: 150,
    diagramName: 'Potencia',
    unit: 'W',
    fixed: 1,
    isShown: true,
  },
  {
    name: '',
    variable: 'v4',
    x: 700,
    y: 175,
    diagramName: 'T_modulo',
    unit: '°C',
    fixed: 2,
    isShown: true,
  },
];
