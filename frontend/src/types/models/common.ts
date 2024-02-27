import { TurbineParameters } from './turbine';

export type InputType = {
  disabled: boolean;
  value: number;
  tooltip: string;
  unit: string;
  variableName: string;
  subIndex: string;
};

export type TurbineParamsType = {
  turbine: TurbineParameters;
  handleChange: (e: any) => void;
};
