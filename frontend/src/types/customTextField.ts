import { InputType } from './models/common';

export type CustomTextFieldType = {
  variable: InputType;
  name?: string;
  step?: number;
  handleChange?: (e: any, variableName?: string) => void;
};

export type ToggleCustomTextFieldType = {};
