import { InputType } from './inputType';
import {
  BatteryTypeParameters,
  BiogasTypeParamenters,
  HydraulicTypeParameters,
  WindTypeParameters,
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

export const WIND_TURBINE: WindTurbine = {
  peakPower: {
    disabled: true,
    value: 200,
    tooltip: 'Potencia pico del aerogenerador',
    unit: 'W',
    variableString: 'Potencia pico',
  },
  rotorHeight: {
    disabled: false,
    value: 1.5,
    tooltip: 'Altura del rotor del aerogenerador',
    unit: 'm',
    variableString: 'H',
    variableSubString: 'r',
    min: 0,
    max: 10,
    step: 0.1,
  },
  anemometerHeight: {
    disabled: false,
    value: 1.5,
    tooltip: 'Altura del anemómetro',
    unit: 'm',
    variableString: 'H',
    variableSubString: 'a',
    min: 0,
    max: 10,
    step: 0.1,
  },
  ratedWindSpeed: {
    disabled: true,
    value: 11.5,
    tooltip: 'Velocidad de viento nominal',
    unit: 'm / s',
    variableString: 'V',
    variableSubString: 'n',
  },
  lowerCutoffWindSpeed: {
    disabled: true,
    value: 2,
    tooltip: 'Velocidad de viento de corte inferior',
    unit: 'm / s',
    variableString: 'V',
    variableSubString: 'c',
  },
  upperCutoffWindSpeed: {
    disabled: true,
    value: 65,
    tooltip: 'Velocidad de viento de corte superior',
    unit: 'm / s',
    variableString: 'V',
    variableSubString: 'f',
  },
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
  dischargeEfficiency: {
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
  dischargeEfficiency: {
    disabled: false,
    value: 98,
    tooltip: 'Eficiencia de descarga',
    unit: '%',
    variableString: 'Eficiencia de descarga',
    min: 0,
    max: 100,
  },
};

export const PELTON_TURBINE: HydraulicTypeParameters = {
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

export const TURGO_TURBINE: HydraulicTypeParameters = {
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

export const CUSTOM_TURBINE: HydraulicTypeParameters = {
  efficiency: {
    disabled: false,
    value: 75,
    tooltip: 'Eficiencia de la turbina',
    unit: '%',
    variableString: 'η',
    variableSubString: 't',
    min: 0,
    max: 100,
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
    max: 100,
    step: 1,
  },
  minimumWaterHead: {
    disabled: false,
    value: 3,
    tooltip: 'Mínima cabeza de agua de operación de la turbina',
    unit: 'm',
    variableString: 'H',
    variableSubString: 'min',
    min: 1,
    max: 100,
    step: 1,
  },
  maximumWaterHead: {
    disabled: false,
    value: 130,
    tooltip: 'Máxima cabeza de agua de operación de la turbina',
    unit: 'm',
    variableString: 'H',
    variableSubString: 'max',
    min: 10,
    max: 1000,
    step: 10,
  },
  minimumWaterFlow: {
    disabled: false,
    value: 0.0001,
    tooltip: 'Mínimo caudal de operación de la turbina',
    unit: 'm³ / s',
    variableString: 'Q',
    variableSubString: 'min',
    min: 0.0001,
    max: 100,
  },
  maximumWaterFlow: {
    disabled: false,
    value: 0.016,
    tooltip: 'Máximo caudal de operación de la turbina',
    unit: 'm³ / s',
    variableString: 'Q',
    variableSubString: 'max',
    min: 0.01,
    max: 10000,
    step: 0.01,
  },
};

export const LABORATORY_WIND_TURBINE: WindTypeParameters = {
  ...WIND_TURBINE,
  surfaceRoughnessLength: {
    disabled: true,
    value: 2,
    tooltip: 'Longitud de rugosidad superficial',
    unit: 'm',
    variableString: 'Longitud de rugosidad superficial',
  },
};

export const CUSTOM_WIND_TURBINE: WindTypeParameters = {
  peakPower: {
    disabled: true,
    value: 200,
    tooltip: 'Potencia pico del aerogenerador',
    unit: 'W',
    variableString: 'Potencia pico',
  },
  rotorHeight: {
    disabled: false,
    value: 1.5,
    tooltip: 'Altura del rotor del aerogenerador',
    unit: 'm',
    variableString: 'H',
    variableSubString: 'r',
    min: 1,
    max: 300,
  },
  anemometerHeight: {
    disabled: false,
    value: 1.5,
    tooltip: 'Altura del anemómetro',
    unit: 'm',
    variableString: 'H',
    variableSubString: 'a',
    min: 1,
    max: 300,
  },
  ratedWindSpeed: {
    disabled: false,
    value: 11.5,
    tooltip: 'Velocidad de viento nominal',
    unit: 'm / s',
    variableString: 'V',
    variableSubString: 'n',
    min: 1,
    max: 100,
  },
  lowerCutoffWindSpeed: {
    disabled: false,
    value: 2,
    tooltip: 'Velocidad de viento de corte inferior',
    unit: 'm / s',
    variableString: 'V',
    variableSubString: 'c',
    min: 1,
    max: 100,
  },
  upperCutoffWindSpeed: {
    disabled: false,
    value: 65,
    tooltip: 'Velocidad de viento de corte superior',
    unit: 'm / s',
    variableString: 'V',
    variableSubString: 'f',
    min: 10,
    max: 200,
  },
  surfaceRoughnessLength: {
    disabled: false,
    value: 0.03,
    tooltip: 'Longitud de rugosidad superficial',
    unit: 'm',
    variableString: 'Longitud de rugosidad superficial',
    min: 0.0001,
    max: 10,
  },
};

export const EXAMPLE_BIOGAS: BiogasTypeParamenters = {
  reactorVolume1: {
    disabled: true,
    value: 30,
    tooltip: 'Volumen de reactor 1',
    unit: 'L',
    variableString: 'Volumen de reactor 1',
  },
  reactorVolume2: {
    disabled: true,
    value: 70,
    tooltip: 'Volumen de reactor 2',
    unit: 'L',
    variableString: 'Volumen de reactor 2',
  },
  diameterHeightRatio1: {
    disabled: true,
    value: 2,
    tooltip: 'Relación diámetro-altura 1',
    unit: '',
    variableString: 'Relación diámetro-altura 1',
  },
  diameterHeightRatio2: {
    disabled: true,
    value: 2,
    tooltip: 'Relación diámetro-altura 2',
    unit: '',
    variableString: 'Relación diámetro-altura 2',
  },
  heatTransferCoefficient1: {
    disabled: true,
    value: 0.05,
    tooltip: 'Coeficiente transferencia de calor 1',
    unit: 'W / m² * K',
    variableString: 'Coeficiente transferencia de calor 1',
  },
  heatTransferCoefficient2: {
    disabled: true,
    value: 0.05,
    tooltip: 'Coeficiente transferencia de calor 2',
    unit: 'W / m² * K',
    variableString: 'Coeficiente transferencia de calor 2',
  },
  temperatureSetpoint1: {
    disabled: true,
    value: 35,
    tooltip: 'Setpoint temperatura 1',
    unit: '°C',
    variableString: 'Setpoint temperatura 1',
  },
  temperatureSetpoint2: {
    disabled: true,
    value: 35,
    tooltip: 'Setpoint temperatura 2',
    unit: '°C',
    variableString: 'Setpoint temperatura 2',
  },
  controllerTolerance1: {
    disabled: true,
    value: 3,
    tooltip: 'Tolerancia controlador 1',
    unit: '°C',
    variableString: 'Tolerancia controlador 1',
  },
  controllerTolerance2: {
    disabled: true,
    value: 3,
    tooltip: 'Tolerancia controlador 2',
    unit: '°C',
    variableString: 'Tolerancia controlador 2',
  },
  carbonConcentration: {
    disabled: true,
    value: 40,
    tooltip: 'Concentración Carbono en base seca',
    unit: '%',
    variableString: 'Concentración Carbono',
  },
  hydrogenConcentration: {
    disabled: true,
    value: 5,
    tooltip: 'Concentración Hidrógeno en base seca',
    unit: '%',
    variableString: 'Concentración Hidrógeno',
  },
  oxygenConcentration: {
    disabled: true,
    value: 20,
    tooltip: 'Concentración Oxígeno en base seca',
    unit: '%',
    variableString: 'Concentración Oxígeno',
  },
  sulfurConcentration: {
    disabled: true,
    value: 1,
    tooltip: 'Concentración Azufre en base seca',
    unit: '%',
    variableString: 'Concentración Azufre',
  },
  totalConcentration: {
    disabled: true,
    value: 10,
    tooltip: 'Concentración solidos totales',
    unit: '%',
    variableString: 'Concentración solidos totales',
  },
  substrateDensity: {
    disabled: true,
    value: 998,
    tooltip: 'Densidad sustrato',
    unit: 'g / L',
    variableString: 'Densidad sustrato',
  },
  substrateTemperature: {
    disabled: true,
    value: 20,
    tooltip: 'Temperatura entrada sustrato',
    unit: '°C',
    variableString: 'Temperatura entrada sustrato',
  },
  substratePressure: {
    disabled: true,
    value: 350,
    tooltip: 'Presión entrada sustrato',
    unit: 'kPa',
    variableString: 'Presión entrada sustrato',
  },
  substrateFlow: {
    disabled: true,
    value: 0.139,
    tooltip: 'Flujo entrada sustrato',
    unit: 'L / h',
    variableString: 'Flujo entrada sustrato',
  },
  substratePresurreDrop: {
    disabled: true,
    value: 5,
    tooltip: 'Caída de presión sustrato',
    unit: 'kPa',
    variableString: 'Caída de presión sustrato',
  },
};

export const CUSTOM_BIOGAS: BiogasTypeParamenters = {
  reactorVolume1: {
    disabled: false,
    value: 30,
    tooltip: 'Volumen de reactor 1',
    unit: 'L',
    variableString: 'Volumen de reactor 1',
    variableSubString: undefined,
    min: 30,
    max: 3000,
    step: 10,
  },
  reactorVolume2: {
    disabled: false,
    value: 70,
    tooltip: 'Volumen de reactor 2',
    unit: 'L',
    variableString: 'Volumen de reactor 2',
    variableSubString: undefined,
    min: 30,
    max: 3000,
    step: 10,
  },
  diameterHeightRatio1: {
    disabled: false,
    value: 2,
    tooltip: 'Relación diámetro-altura 1',
    unit: '',
    variableString: 'Relación diámetro-altura 1',
    variableSubString: undefined,
    min: 1.5,
    max: 2.5,
    step: 0.1,
  },
  diameterHeightRatio2: {
    disabled: false,
    value: 2,
    tooltip: 'Relación diámetro-altura 2',
    unit: '',
    variableString: 'Relación diámetro-altura 2',
    variableSubString: undefined,
    min: 1.5,
    max: 2.5,
    step: 0.1,
  },
  heatTransferCoefficient1: {
    disabled: false,
    value: 0.05,
    tooltip: 'Coeficiente transferencia de calor 1',
    unit: 'W / m² * K',
    variableString: 'Coeficiente transferencia de calor 1',
    variableSubString: undefined,
    min: 0.01,
    max: 1,
    step: 0.01,
  },
  heatTransferCoefficient2: {
    disabled: false,
    value: 0.05,
    tooltip: 'Coeficiente transferencia de calor 2',
    unit: 'W / m² * K',
    variableString: 'Coeficiente transferencia de calor 2',
    variableSubString: undefined,
    min: 0.01,
    max: 1,
    step: 0.01,
  },
  temperatureSetpoint1: {
    disabled: false,
    value: 35,
    tooltip: 'Setpoint temperatura 1',
    unit: '°C',
    variableString: 'Setpoint temperatura 1',
    variableSubString: undefined,
    min: 25,
    max: 55,
  },
  temperatureSetpoint2: {
    disabled: false,
    value: 35,
    tooltip: 'Setpoint temperatura 2',
    unit: '°C',
    variableString: 'Setpoint temperatura 2',
    variableSubString: undefined,
    min: 25,
    max: 55,
  },
  controllerTolerance1: {
    disabled: false,
    value: 3,
    tooltip: 'Tolerancia controlador 1',
    unit: '°C',
    variableString: 'Tolerancia controlador 1',
    variableSubString: undefined,
    min: 2,
    max: 5,
    step: 0.1,
  },
  controllerTolerance2: {
    disabled: false,
    value: 3,
    tooltip: 'Tolerancia controlador 2',
    unit: '°C',
    variableString: 'Tolerancia controlador 2',
    variableSubString: undefined,
    min: 2,
    max: 5,
    step: 0.1,
  },
  carbonConcentration: {
    disabled: false,
    value: 40,
    tooltip: 'Concentración Carbono en base seca',
    unit: '%',
    variableString: 'Concentración Carbono',
    variableSubString: undefined,
    min: 0.1,
    max: 100,
    step: 0.1,
  },
  hydrogenConcentration: {
    disabled: false,
    value: 5,
    tooltip: 'Concentración Hidrógeno en base seca',
    unit: '%',
    variableString: 'Concentración Hidrógeno',
    variableSubString: undefined,
    min: 0.1,
    max: 100,
    step: 0.1,
  },
  oxygenConcentration: {
    disabled: false,
    value: 20,
    tooltip: 'Concentración Oxígeno en base seca',
    unit: '%',
    variableString: 'Concentración Oxígeno',
    variableSubString: undefined,
    min: 0.1,
    max: 100,
    step: 0.1,
  },
  sulfurConcentration: {
    disabled: false,
    value: 1,
    tooltip: 'Concentración Azufre en base seca',
    unit: '%',
    variableString: 'Concentración Azufre',
    variableSubString: undefined,
    min: 0.1,
    max: 100,
    step: 0.1,
  },
  totalConcentration: {
    disabled: false,
    value: 10,
    tooltip: 'Concentración solidos totales',
    unit: '%',
    variableString: 'Concentración solidos totales',
    variableSubString: undefined,
    min: 0.1,
    max: 100,
    step: 0.1,
  },
  substrateDensity: {
    disabled: false,
    value: 998,
    tooltip: 'Densidad sustrato',
    unit: 'g / L',
    variableString: 'Densidad sustrato',
    variableSubString: undefined,
    min: 100,
    max: 2000,
    step: 10,
  },
  substrateTemperature: {
    disabled: false,
    value: 20,
    tooltip: 'Temperatura entrada sustrato',
    unit: '°C',
    variableString: 'Temperatura entrada sustrato',
    variableSubString: undefined,
    min: 10,
    max: 40,
  },
  substratePressure: {
    disabled: false,
    value: 350,
    tooltip: 'Presión entrada sustrato',
    unit: 'kPa',
    variableString: 'Presión entrada sustrato',
    variableSubString: undefined,
    min: 100,
    max: 1000,
    step: 10,
  },
  substrateFlow: {
    disabled: false,
    value: 0.139,
    tooltip: 'Flujo entrada sustrato',
    unit: 'L / h',
    variableString: 'Flujo entrada sustrato',
    variableSubString: undefined,
    min: 0,
    max: 1000,
  },
  substratePresurreDrop: {
    disabled: false,
    value: 5,
    tooltip: 'Caída de presión sustrato',
    unit: 'kPa',
    variableString: 'Caída de presión sustrato',
    variableSubString: undefined,
    min: 0,
    max: 100,
  },
};