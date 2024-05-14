export const getValueByKey = (type: any, value: string) => {
  return type[value as keyof typeof type];
};
