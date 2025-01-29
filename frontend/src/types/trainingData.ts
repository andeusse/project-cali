export type TrainingDataType = {
  names: string[];
  values: { [k: string]: TrainingDataVariables };
};

export type TrainingDataVariables = {
  activationEnergyR101?: number;
  activationEnergyR102?: number;
  exponentialFactorR101?: number;
  exponentialFactorR102?: number;
  lambdaR101?: number;
  lambdaR102?: number;
};
