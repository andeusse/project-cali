import { TurbineParameters } from './turbine';

export type InputType = {
  disabled: boolean;
  value: number;
  tooltip: string;
  unit: string;
  variableString: string;
  variableSubString: string;
  min?: number;
  max?: number;
};

export type DiagramVariableType = {
  name: string;
  variable: string;
  x?: number;
  y?: number;
  diagramName?: string;
  unit: string;
  fixed?: number;
  isShown: boolean;
};

export type CommonSystemParameter = {
  name: string;
  timeMultiplier?: InputType;
};

export type SolarSystem = CommonSystemParameter & {};

export type BatterySystem = CommonSystemParameter & {};

export type BiogasSystem = CommonSystemParameter & {};

export type LoadSystem = CommonSystemParameter & {};

export type TurbineParamsType = {
  turbine: TurbineParameters;
  handleChange: (e: any) => void;
};
