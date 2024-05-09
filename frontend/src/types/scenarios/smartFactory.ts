import { CommonSystemParameter } from '../common';
import { TabType } from '../tab';
import {
  CommonScenarioParameters,
  COMMON_SCENARIO,
  COMMON_TABS,
} from './commons';

export type SmartFactoryParameters = CommonScenarioParameters &
  CommonSystemParameter & {};

export const SMART_FACTORY: SmartFactoryParameters = {
  ...COMMON_SCENARIO,
  biogasSystemNumber: {
    ...COMMON_SCENARIO.biogasSystemNumber,
    max: 1,
  },
};

export const SMART_FACTORY_TABS: TabType[] = [...COMMON_TABS];
