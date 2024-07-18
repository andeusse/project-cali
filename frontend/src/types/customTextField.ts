import { InputArrayType, InputType } from './inputType';

export type CustomTextFieldType = {
  variable: InputType | InputArrayType;
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

export type ToggleArrayCustomTextFieldType = ToggleCustomTextFieldType & {
  variableName: string;
  arrayDisabled: boolean;
  showToggle?: boolean;
};
