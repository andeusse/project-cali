import { InputType } from '../types/models/common';
import { formType } from './setFormState';

export const setFormObjectValue = <T extends formType>(
  oldState: T,
  splitName: Array<string>,
  newValue: any
): T => {
  let newState = { ...oldState };
  const s: any = oldState[splitName[0] as keyof T];
  if (typeof s[splitName[1]] === 'object') {
    newState = {
      ...oldState,
      [splitName[0]]: {
        ...s,
        [splitName[1]]: {
          ...(s[splitName[1]] as InputType),
          value: parseFloat(newValue),
        },
      },
    };
  } else {
    newState = {
      ...oldState,
      [splitName[0]]: {
        ...s,
        [splitName[1]]: newValue,
      },
    };
  }
  return newState;
};
