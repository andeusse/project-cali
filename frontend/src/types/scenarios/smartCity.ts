import { InputType } from '../inputType';
import { TabType } from '../tab';
import {
  CommonScenarioParameters,
  COMMON_SCENARIO,
  COMMON_TABS,
} from './commons';

export type SmartCityParameters = CommonScenarioParameters & {
  batterySystemNumber: InputType;
  hydraulicSystemNumber: InputType;
  windSystemNumber: InputType;
};

export const SMART_CITY: SmartCityParameters = {
  ...COMMON_SCENARIO,
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
};

export const SMART_CITY_TABS: TabType[] = [
  ...COMMON_TABS,
  {
    title: 'Baterías',
    children: undefined,
  },
  {
    title: 'Hidráulicos',
    children: undefined,
  },
  {
    title: 'Eólicos',
    children: undefined,
  },
];
