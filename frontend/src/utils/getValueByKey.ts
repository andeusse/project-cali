export const getValueByKey = (T: any, value: string) => {
  return T[value as keyof typeof T];
};
