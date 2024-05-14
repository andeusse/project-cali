import { CommonSystemParameter } from '../common';
import { CommonScenarioParameters, COMMON_SCENARIO } from './common';

export type SmartFactoryParameters = CommonScenarioParameters &
  CommonSystemParameter & {};

export const SMART_FACTORY: SmartFactoryParameters = {
  ...COMMON_SCENARIO,
  biogasSystemNumber: {
    ...COMMON_SCENARIO.biogasSystemNumber,
    max: 1,
  },
};
