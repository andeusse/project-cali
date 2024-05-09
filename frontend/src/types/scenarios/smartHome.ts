import { TabType } from '../tab';
import { InputType } from '../inputType';
import {
  CommonScenarioParameters,
  COMMON_SCENARIO,
  COMMON_TABS,
} from './commons';
import { CommonSystemParameter } from '../common';

export type SmartHomeParameters = CommonScenarioParameters &
  CommonSystemParameter & {
    batterySystemNumber: InputType;
  };

export const SMART_HOME: SmartHomeParameters = {
  ...COMMON_SCENARIO,
  biogasSystemNumber: {
    ...COMMON_SCENARIO.biogasSystemNumber,
    max: 1,
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
};

export const SMART_FACTORY_TABS: TabType[] = [
  ...COMMON_TABS,
  {
    title: 'Baterías',
    children: undefined,
  },
];
