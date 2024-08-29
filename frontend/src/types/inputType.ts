export type InputType = {
  disabled: boolean;
  value: number;
  tooltip: string;
  unit: string;
  variableString: string;
  variableSubString?: string;
  min?: number;
  max?: number;
  step?: number;
  stringValue?: string;
};

export type InputArrayType = InputType & {
  arrayEnabled: boolean;
};
