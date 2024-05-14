import { InputType } from './inputType';

export type CustomTextFieldType = {
  variable: InputType;
  name?: string;
  handleChange?: (e: any, variableName?: string) => void;
  disabled?: boolean;
  isInteger?: boolean;
  disableKeyDown?: boolean;
};

export type ToggleCustomTextFieldType = CustomTextFieldType & {
  falseText?: string;
  trueText?: string;
  disabled?: boolean;
};
