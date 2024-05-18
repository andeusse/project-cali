import { InputType } from './inputType';
import {
  BatteryTypeParameters,
  TurbineTypeParameters,
} from './scenarios/common';

export type CommonSystemParameter = {
  name: string;
};

export type SolarPanel = {
  deratingFactor: InputType;
  efficiency: InputType;
  nominalIrradiance: InputType;
  testIrradiance: InputType;
  nominalTemperature: InputType;
  testTemperature: InputType;
  operatingTemperature: InputType;
  temperatureVariationCoefficient: InputType;
};

export type WindTurbine = {
  peakPower: InputType;
  rotorHeight: InputType;
  anemometerHeight: InputType;
  ratedWindSpeed: InputType;
  lowerCutoffWindSpeed: InputType;
  upperCutoffWindSpeed: InputType;
};

export type Battery = {
  stateOfCharge: InputType;
  temperatureCoefficient: InputType;
  capacity: InputType;
  selfDischargeCoefficient: InputType;
  chargeDischargeEfficiency: InputType;
  temperatureCompensationCoefficient: InputType;
};

export const MONOCRYSTALLINE_PANEL: SolarPanel = {
  deratingFactor: {
    disabled: false,
    value: 1,
    tooltip: 'Factor de reducción de la potencia',
    unit: '',
    variableString: 'f',
    variableSubString: 'pu',
    min: 0.7,
    max: 1,
    step: 0.01,
  },
  efficiency: {
    disabled: true,
    value: 15.44,
    tooltip: 'Eficiencia del panel',
    unit: '%',
    variableString: 'η',
    variableSubString: 'C',
  },
  nominalIrradiance: {
    disabled: true,
    value: 800,
    tooltip: 'Irradiancia a condiciones nominales de operación',
    unit: 'W / m²',
    variableString: 'G',
    variableSubString: 'NOCT',
  },
  testIrradiance: {
    disabled: true,
    value: 1000,
    tooltip: 'Irradiancia a condiciones estándar de prueba',
    unit: 'W / m²',
    variableString: 'G',
    variableSubString: 'STC',
  },
  nominalTemperature: {
    disabled: true,
    value: 45,
    tooltip: 'Temperatura del módulo en condiciones nominales de operación',
    unit: '°C',
    variableString: 'Tc',
    variableSubString: 'NOCT',
  },
  testTemperature: {
    disabled: true,
    value: 25,
    tooltip: 'Temperatura del módulo en condiciones estándar de prueba',
    unit: '°C',
    variableString: 'Tc',
    variableSubString: 'STC',
  },
  operatingTemperature: {
    disabled: true,
    value: 20,
    tooltip: 'Temperatura ambiente normal de operación',
    unit: '°C',
    variableString: 'Ta',
    variableSubString: 'NOCT',
  },
  temperatureVariationCoefficient: {
    disabled: true,
    value: -0.39,
    tooltip: 'Coeficiente de variación de la potencia con la temperatura',
    unit: '% / °C',
    variableString: 'μ',
    variableSubString: 'pm',
  },
};

export const POLICRYSTALLINE_PANEL: SolarPanel = {
  deratingFactor: {
    disabled: false,
    value: 1,
    tooltip: 'Factor de reducción de la potencia',
    unit: '',
    variableString: 'f',
    variableSubString: 'pu',
    min: 0.7,
    max: 1,
    step: 0.01,
  },
  efficiency: {
    disabled: true,
    value: 15.44,
    tooltip: 'Eficiencia del panel',
    unit: '%',
    variableString: 'η',
    variableSubString: 'C',
  },
  nominalIrradiance: {
    disabled: true,
    value: 800,
    tooltip: 'Irradiancia a condiciones nominales de operación',
    unit: 'W / m²',
    variableString: 'G',
    variableSubString: 'NOCT',
  },
  testIrradiance: {
    disabled: true,
    value: 1000,
    tooltip: 'Irradiancia a condiciones estándar de prueba',
    unit: 'W / m²',
    variableString: 'G',
    variableSubString: 'STC',
  },
  nominalTemperature: {
    disabled: true,
    value: 45,
    tooltip: 'Temperatura del módulo en condiciones nominales de operación',
    unit: '°C',
    variableString: 'Tc',
    variableSubString: 'NOCT',
  },
  testTemperature: {
    disabled: true,
    value: 25,
    tooltip: 'Temperatura del módulo en condiciones estándar de prueba',
    unit: '°C',
    variableString: 'Tc',
    variableSubString: 'STC',
  },
  operatingTemperature: {
    disabled: true,
    value: 20,
    tooltip: 'Temperatura ambiente normal de operación',
    unit: '°C',
    variableString: 'Ta',
    variableSubString: 'NOCT',
  },
  temperatureVariationCoefficient: {
    disabled: true,
    value: -0.39,
    tooltip: 'Coeficiente de variación de la potencia con la temperatura',
    unit: '% / °C',
    variableString: 'μ',
    variableSubString: 'pm',
  },
};

export const FLEX_PANEL: SolarPanel = {
  deratingFactor: {
    disabled: false,
    value: 1,
    tooltip: 'Factor de reducción de la potencia',
    unit: '',
    variableString: 'f',
    variableSubString: 'pu',
    min: 0.7,
    max: 1,
    step: 0.01,
  },
  efficiency: {
    disabled: true,
    value: 15.43,
    tooltip: 'Eficiencia del panel',
    unit: '%',
    variableString: 'η',
    variableSubString: 'C',
  },
  nominalIrradiance: {
    disabled: true,
    value: 800,
    tooltip: 'Irradiancia a condiciones nominales de operación',
    unit: 'W / m²',
    variableString: 'G',
    variableSubString: 'NOCT',
  },
  testIrradiance: {
    disabled: true,
    value: 1000,
    tooltip: 'Irradiancia a condiciones estándar de prueba',
    unit: 'W / m²',
    variableString: 'G',
    variableSubString: 'STC',
  },
  nominalTemperature: {
    disabled: true,
    value: 45,
    tooltip: 'Temperatura del módulo en condiciones nominales de operación',
    unit: '°C',
    variableString: 'Tc',
    variableSubString: 'NOCT',
  },
  testTemperature: {
    disabled: true,
    value: 25,
    tooltip: 'Temperatura del módulo en condiciones estándar de prueba',
    unit: '°C',
    variableString: 'Tc',
    variableSubString: 'STC',
  },
  operatingTemperature: {
    disabled: true,
    value: 20,
    tooltip: 'Temperatura ambiente normal de operación',
    unit: '°C',
    variableString: 'Ta',
    variableSubString: 'NOCT',
  },
  temperatureVariationCoefficient: {
    disabled: true,
    value: -0.42,
    tooltip: 'Coeficiente de variación de la potencia con la temperatura',
    unit: '% / °C',
    variableString: 'μ',
    variableSubString: 'pm',
  },
};

export const CADMIUM_TELLURIDE_PANEL: SolarPanel = {
  deratingFactor: {
    disabled: false,
    value: 1,
    tooltip: 'Factor de reducción de la potencia',
    unit: '',
    variableString: 'f',
    variableSubString: 'pu',
    min: 0.7,
    max: 1,
    step: 0.01,
  },
  efficiency: {
    disabled: true,
    value: 11,
    tooltip: 'Eficiencia del panel',
    unit: '%',
    variableString: 'η',
    variableSubString: 'C',
  },
  nominalIrradiance: {
    disabled: true,
    value: 800,
    tooltip: 'Irradiancia a condiciones nominales de operación',
    unit: 'W / m²',
    variableString: 'G',
    variableSubString: 'NOCT',
  },
  testIrradiance: {
    disabled: true,
    value: 1000,
    tooltip: 'Irradiancia a condiciones estándar de prueba',
    unit: 'W / m²',
    variableString: 'G',
    variableSubString: 'STC',
  },
  nominalTemperature: {
    disabled: true,
    value: 42,
    tooltip: 'Temperatura del módulo en condiciones nominales de operación',
    unit: '°C',
    variableString: 'Tc',
    variableSubString: 'NOCT',
  },
  testTemperature: {
    disabled: true,
    value: 25,
    tooltip: 'Temperatura del módulo en condiciones estándar de prueba',
    unit: '°C',
    variableString: 'Tc',
    variableSubString: 'STC',
  },
  operatingTemperature: {
    disabled: true,
    value: 20,
    tooltip: 'Temperatura ambiente normal de operación',
    unit: '°C',
    variableString: 'Ta',
    variableSubString: 'NOCT',
  },
  temperatureVariationCoefficient: {
    disabled: true,
    value: -0.25,
    tooltip: 'Coeficiente de variación de la potencia con la temperatura',
    unit: '% / °C',
    variableString: 'μ',
    variableSubString: 'pm',
  },
};

export const CUSTOM_PANEL: SolarPanel = {
  deratingFactor: {
    disabled: false,
    value: 1,
    tooltip: 'Factor de reducción de la potencia',
    unit: '',
    variableString: 'f',
    variableSubString: 'pu',
    min: 0,
    max: 1,
    step: 0.01,
  },
  efficiency: {
    disabled: false,
    value: 15.44,
    tooltip: 'Eficiencia del panel',
    unit: '%',
    variableString: 'η',
    variableSubString: 'C',
    min: 0,
    max: 100,
  },
  nominalIrradiance: {
    disabled: false,
    value: 800,
    tooltip: 'Irradiancia a condiciones nominales de operación',
    unit: 'W / m²',
    variableString: 'G',
    variableSubString: 'NOCT',
    min: 0,
    max: 1500,
    step: 100,
  },
  testIrradiance: {
    disabled: false,
    value: 1000,
    tooltip: 'Irradiancia a condiciones estándar de prueba',
    unit: 'W / m²',
    variableString: 'G',
    variableSubString: 'STC',
    min: 0,
    max: 1500,
    step: 100,
  },
  nominalTemperature: {
    disabled: false,
    value: 45,
    tooltip: 'Temperatura del módulo en condiciones nominales de operación',
    unit: '°C',
    variableString: 'Tc',
    variableSubString: 'NOCT',
    min: 0,
    max: 100,
  },
  testTemperature: {
    disabled: false,
    value: 25,
    tooltip: 'Temperatura del módulo en condiciones estándar de prueba',
    unit: '°C',
    variableString: 'Tc',
    variableSubString: 'STC',
    min: 0,
    max: 100,
  },
  operatingTemperature: {
    disabled: false,
    value: 20,
    tooltip: 'Temperatura ambiente normal de operación',
    unit: '°C',
    variableString: 'Ta',
    variableSubString: 'NOCT',
    min: 0,
    max: 100,
  },
  temperatureVariationCoefficient: {
    disabled: false,
    value: -0.39,
    tooltip: 'Coeficiente de variación de la potencia con la temperatura',
    unit: '% / °C',
    variableString: 'μ',
    variableSubString: 'pm',
    min: -10,
    max: 0,
    step: 0.1,
  },
};

export const GEL_BATTERY: BatteryTypeParameters = {
  selfDischargeCoefficient: {
    disabled: true,
    value: 2.5,
    tooltip: 'Coeficiente de autodescarga',
    unit: '%/mes',
    variableString: 'Coeficiente de autodescarga',
  },
  chargeEfficiency: {
    disabled: true,
    value: 98,
    tooltip: 'Eficiencia de carga',
    unit: '%',
    variableString: 'Eficiencia de carga',
  },
  dischargeDischargeEfficiency: {
    disabled: true,
    value: 98,
    tooltip: 'Eficiencia de descarga',
    unit: '%',
    variableString: 'Eficiencia de descarga',
  },
};

export const CUSTOM_BATTERY: BatteryTypeParameters = {
  selfDischargeCoefficient: {
    disabled: false,
    value: 2.5,
    tooltip: 'Coeficiente de autodescarga',
    unit: '%/mes',
    variableString: 'Coeficiente de autodescarga',
    min: 0,
    max: 100,
  },
  chargeEfficiency: {
    disabled: false,
    value: 98,
    tooltip: 'Eficiencia de carga',
    unit: '%',
    variableString: 'Eficiencia de carga',
    min: 0,
    max: 100,
  },
  dischargeDischargeEfficiency: {
    disabled: false,
    value: 98,
    tooltip: 'Eficiencia de descarga',
    unit: '%',
    variableString: 'Eficiencia de descarga',
    min: 0,
    max: 100,
  },
};

export const PELTON_TURBINE: TurbineTypeParameters = {
  efficiency: {
    disabled: true,
    value: 75,
    tooltip: 'Eficiencia de la turbina',
    unit: '%',
    variableString: 'η',
    variableSubString: 't',
  },
  frictionLosses: {
    disabled: true,
    value: 0,
    tooltip: 'Pérdidas por fricción',
    unit: '%',
    variableString: 'F',
    variableSubString: 'h',
  },
  minimumWaterHead: {
    disabled: true,
    value: 3,
    tooltip: 'Mínima cabeza de agua de operación de la turbina',
    unit: 'm',
    variableString: 'H',
    variableSubString: 'min',
  },
  maximumWaterHead: {
    disabled: true,
    value: 130,
    tooltip: 'Máxima cabeza de agua de operación de la turbina',
    unit: 'm',
    variableString: 'H',
    variableSubString: 'max',
  },
  minimumWaterFlow: {
    disabled: true,
    value: 0.0001,
    tooltip: 'Mínimo caudal de operación de la turbina',
    unit: 'm³ / s',
    variableString: 'Q',
    variableSubString: 'min',
  },
  maximumWaterFlow: {
    disabled: true,
    value: 0.01,
    tooltip: 'Máximo caudal de operación de la turbina',
    unit: 'm³ / s',
    variableString: 'Q',
    variableSubString: 'max',
  },
};

export const TURGO_TURBINE: TurbineTypeParameters = {
  efficiency: {
    disabled: true,
    value: 75,
    tooltip: 'Eficiencia de la turbina',
    unit: '%',
    variableString: 'η',
    variableSubString: 't',
  },
  frictionLosses: {
    disabled: true,
    value: 0,
    tooltip: 'Pérdidas por fricción',
    unit: '%',
    variableString: 'F',
    variableSubString: 'h',
  },
  minimumWaterHead: {
    disabled: true,
    value: 2,
    tooltip: 'Mínima cabeza de agua de operación de la turbina',
    unit: 'm',
    variableString: 'H',
    variableSubString: 'min',
  },
  maximumWaterHead: {
    disabled: true,
    value: 30,
    tooltip: 'Máxima cabeza de agua de operación de la turbina',
    unit: 'm',
    variableString: 'H',
    variableSubString: 'max',
  },
  minimumWaterFlow: {
    disabled: true,
    value: 0.008,
    tooltip: 'Mínimo caudal de operación de la turbina',
    unit: 'm³ / s',
    variableString: 'Q',
    variableSubString: 'min',
  },
  maximumWaterFlow: {
    disabled: true,
    value: 0.016,
    tooltip: 'Máximo caudal de operación de la turbina',
    unit: 'm³ / s',
    variableString: 'Q',
    variableSubString: 'max',
  },
};

export const CUSTOM_TURBINE: TurbineTypeParameters = {
  efficiency: {
    disabled: false,
    value: 75,
    tooltip: 'Eficiencia de la turbina',
    unit: '%',
    variableString: 'η',
    variableSubString: 't',
    min: 0,
    max: 1,
    step: 1,
  },
  frictionLosses: {
    disabled: false,
    value: 0,
    tooltip: 'Pérdidas por fricción',
    unit: '%',
    variableString: 'F',
    variableSubString: 'h',
    min: 0,
    max: 1,
    step: 1,
  },
  minimumWaterHead: {
    disabled: false,
    value: 2,
    tooltip: 'Mínima cabeza de agua de operación de la turbina',
    unit: 'm',
    variableString: 'H',
    variableSubString: 'min',
    min: 0,
    max: 1,
    step: 1,
  },
  maximumWaterHead: {
    disabled: false,
    value: 30,
    tooltip: 'Máxima cabeza de agua de operación de la turbina',
    unit: 'm',
    variableString: 'H',
    variableSubString: 'max',
    min: 0,
    max: 1,
    step: 1,
  },
  minimumWaterFlow: {
    disabled: false,
    value: 0.008,
    tooltip: 'Mínimo caudal de operación de la turbina',
    unit: 'm³ / s',
    variableString: 'Q',
    variableSubString: 'min',
    min: 0,
    max: 1,
    step: 1,
  },
  maximumWaterFlow: {
    disabled: false,
    value: 0.016,
    tooltip: 'Máximo caudal de operación de la turbina',
    unit: 'm³ / s',
    variableString: 'Q',
    variableSubString: 'max',
    min: 0,
    max: 1,
    step: 1,
  },
};
