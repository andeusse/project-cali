import { DiagramVariableType, InputType } from './common';

export enum SolarPanelModulesType {
  Custom = 'Custom',
  Monocrystalline = 'Monocristalino',
  Policrystalline = 'Policristalino',
  MonocrystallineThin = 'Monocristalino película delgada',
  CadmiumTelluride = 'Telururo de Cadmio',
}

export type SolarPanelParameters = {
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

export type SolarParamsType = {
  solarModule: SolarPanelParameters;
  handleChange: (e: any) => void;
};

export const CUSTOM_SOLAR_PANEL: SolarPanelParameters = {
  panelType: SolarPanelModulesType.Custom,
  moduleNumber: {
    disabled: false,
    value: 1,
    tooltip: 'Cantidad de módulos solares',
    unit: '',
    variableName: 'Número de módulos',
    subIndex: '',
    min: 1,
  },
  modulePeakPower: {
    disabled: false,
    value: 100,
    tooltip: 'Potencia pico de cada módulo',
    unit: 'W',
    variableName: 'Potencia pico / módulo',
    subIndex: '',
    min: 0,
  },
  moduleReductionPowerFactor: {
    disabled: false,
    value: 1,
    tooltip:
      'Factor de reducción de la potencia del módulo de acuerdo con los años de operación',
    unit: '',
    variableName: 'f',
    subIndex: 'pu',
    min: 0,
    max: 1,
  },
  moduleEfficiency: {
    disabled: false,
    value: 15.44,
    tooltip: 'Eficiencia eléctrica del módulo',
    unit: '%',
    variableName: 'η',
    subIndex: 'C',
    min: 0.01,
    max: 100,
  },
  moduleStandardTestIrradiation: {
    disabled: false,
    value: 1000,
    tooltip:
      'Irradiancia solar en condiciones estándar de prueba del módulo, típicamente 1000 W/m²',
    unit: 'W / m²',
    variableName: 'G',
    subIndex: 'STC',
    min: 0,
  },
  moduleStantardTestTemperature: {
    disabled: false,
    value: 25,
    tooltip:
      'Temperatura del módulo fotovoltaico en condiciones estándar de prueba, típicamente 25 °C',
    unit: '°C',
    variableName: 'Tc',
    subIndex: 'STC',
    min: 0,
  },
  moduleStandardIrradiation: {
    disabled: false,
    value: 800,
    tooltip: 'Irradiancia normal de operación del módulo, típicamente 800 W/m²',
    unit: 'W / m²',
    variableName: 'G',
    subIndex: 'NOCT',
    min: 0,
  },
  moduleStandardTemperature: {
    disabled: false,
    value: 45,
    tooltip:
      'Temperatura nominal de operación del módulo, típicamente 45-48 °C',
    unit: '°C',
    variableName: 'Tc',
    subIndex: 'NOCT',
    min: 0,
  },
  moduleEnvironmentTemperature: {
    disabled: false,
    value: 20,
    tooltip:
      'Temperatura ambiente normal de operación del módulo, típicamente 20 °C',
    unit: '°C',
    variableName: 'Ta',
    subIndex: 'NOCT',
    min: 0,
  },
  moduleCoefficientPowerVariation: {
    disabled: false,
    value: -0.4,
    tooltip:
      'Coeficiente de variación de la potencia con la temperatura en la condición de extracción de máxima potencia',
    unit: '% / °C',
    variableName: 'μ',
    subIndex: 'pm',
  },
  inputOfflineOperation: false,
  inputIrradiation: {
    disabled: true,
    value: 1000,
    tooltip: 'Irradiancia de los módulos',
    unit: 'W / m²',
    variableName: 'Irradiancia',
    subIndex: '',
    min: 0,
  },
  inputTemperature: {
    disabled: true,
    value: 25,
    tooltip: 'Temperatura de los módulos',
    unit: '°C',
    variableName: 'Temperatura',
    subIndex: '',
    min: 0,
  },
};

export const SOLAR_DIAGRAM_VARIABLES: DiagramVariableType[] = [
  {
    name: 'v1',
    x: 100,
    y: 220,
    printedName: 'Irradiancia',
    unit: 'W / m²',
    fixed: 2,
  },
  {
    name: 'v2',
    x: 655,
    y: 50,
    printedName: 'T_ambiente',
    unit: '°C',
    fixed: 1,
  },
  {
    name: 'v3',
    x: 700,
    y: 150,
    printedName: 'Potencia',
    unit: 'W',
    fixed: 1,
  },
  {
    name: 'v4',
    x: 700,
    y: 175,
    printedName: 'T_modulo',
    unit: '°C',
    fixed: 2,
  },
];
