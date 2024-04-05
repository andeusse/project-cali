import { InputType } from './common';

export enum SmartCityOperationModesType {
  Manual = 'Manual',
  Automatic = 'Automático',
}

export enum StepUnitType {
  Second = 'Segundo(s)',
  Minute = 'Minutos(s)',
  Hour = 'Hora(s)',
  Day = 'Día(s)',
}

export type SmartCityParameters = {
  operationMode: SmartCityOperationModesType;
  steps: InputType;
  stepTime: InputType;
  stepUnit: StepUnitType;
  solarSystemNumber: InputType;
  batterySystemNumber: InputType;
  BiogasSystemNumber: InputType;
  LoadSystemNumber: InputType;
};

export const SMART_CITY: SmartCityParameters = {
  operationMode: SmartCityOperationModesType.Manual,
  steps: {
    disabled: false,
    value: 1,
    tooltip: 'Número de pasos a simular',
    unit: '',
    variableString: 'Número de pasos',
    min: 1,
  },
  stepTime: {
    disabled: false,
    value: 1,
    tooltip: 'Tiempo por paso',
    unit: '',
    variableString: 'Tiempo por paso',
    min: 1,
  },
  stepUnit: StepUnitType.Second,
  solarSystemNumber: {
    disabled: false,
    value: 1,
    tooltip: 'Número de sistemas solares',
    unit: '',
    variableString: 'Sistemas solares',
    min: 0,
  },
  batterySystemNumber: {
    disabled: false,
    value: 1,
    tooltip: 'Número de sistemas de baterías',
    unit: '',
    variableString: 'Sistemas de baterías',
    min: 0,
  },
  BiogasSystemNumber: {
    disabled: false,
    value: 1,
    tooltip: 'Número de sistemas de biogás',
    unit: '',
    variableString: 'Sistemas de biogás',
    min: 0,
  },
  LoadSystemNumber: {
    disabled: false,
    value: 1,
    tooltip: '',
    unit: '',
    variableString: '',
    min: 0,
  },
};
