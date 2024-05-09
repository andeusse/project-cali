import { CommonSystemParameter } from '../common';
import { InputType } from '../inputType';
import { TabType } from '../tab';

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

export type CommonScenarioParameters = CommonSystemParameter & {
  operationMode: ScenariosModesType;
  steps: InputType;
  stepTime: InputType;
  stepUnit: ScenariosStepUnitType;
  solarSystemNumber: InputType;
  biogasSystemNumber: InputType;
  loadSystemNumber: InputType;
};

export const COMMON_SCENARIO: CommonScenarioParameters = {
  name: 'Nombre',
  operationMode: ScenariosModesType.Manual,
  steps: {
    disabled: false,
    value: 1,
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
};

export const COMMON_TABS: TabType[] = [
  {
    title: 'Solar',
    children: undefined,
  },
  {
    title: 'Biogás',
    children: undefined,
  },
  {
    title: 'Demanda',
    children: undefined,
  },
];
