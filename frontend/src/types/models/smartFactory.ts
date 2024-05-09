import { TabType } from '../tab';
import {
  COMMON_SCENARIO,
  COMMON_TABS,
  CommonScenarioParameters,
  CommonSystemParameter,
} from './common';

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
