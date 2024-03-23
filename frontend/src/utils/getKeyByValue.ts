export const getKeyByValue = (type: any, value: string) => {
  return type[value as keyof typeof type];
};
