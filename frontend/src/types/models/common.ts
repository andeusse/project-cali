import { TurbineParameters } from './turbine';

export type InputType = {
  disabled: boolean;
  value: number;
  tooltip: string;
  unit: string;
  variableName: string;
  subIndex: string;
  min?: number;
  max?: number;
};

export type DiagramVariableType = {
  name: string;
  x: number;
  y: number;
  printedName: string;
  unit: string;
  fixed: number;
};

export type TurbineParamsType = {
  turbine: TurbineParameters;
  handleChange: (e: any) => void;
};
