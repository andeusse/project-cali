import { AxiosResponse } from 'axios';
import api from './api';
import Config from '../config/config';
import { TrainingDataType } from '../types/trainingData';

const trainingDataMock1: TrainingDataType = {
  names: ['Frijoles'],
  values: {
    Frijoles: {
      activationEnergyR101: 2.59e-9,
      activationEnergyR102: 2.59e-9,
      exponentialFactorR101: 0.00329,
      exponentialFactorR102: 0.00329,
      lambdaR101: -44928.0,
      lambdaR102: -44928.0,
    },
  },
};

const trainingDataMock2: TrainingDataType = {
  names: ['Gallinaza', 'Porquinaza'],
  values: {
    Gallinaza: {
      activationEnergyR101: 2.59e-9,
      exponentialFactorR101: 0.00329,
      lambdaR101: -44928.0,
    },
    Porquinaza: {
      activationEnergyR101: 0,
      exponentialFactorR101: 0,
      lambdaR101: 0,
    },
  },
};

export const modelsAPI = <T, R, S = AxiosResponse<R>>(
  model: string,
  body: T
): Promise<S> => {
  return api.post(
    `${Config.getInstance().params.apiUrl}/models/${model}`,
    body
  );
};

export const trainingDataAPI = <R, S = AxiosResponse<R>>(
  model: string,
  queryMode: string,
  queryModel: string
): Promise<S> => {
  return api.get(
    `${
      Config.getInstance().params.apiUrl
    }/models/${model}?mode=${queryMode}&model=${queryModel}`
  );
};

export const trainingDataAPIMock = <R, S = AxiosResponse<R>>(
  model: string,
  queryMode: string,
  queryModel: string
): Promise<S> => {
  return new Promise<S>((res, rej) => {
    setTimeout(() => {
      if (model === 'biogas') {
        res(trainingDataMock1 as S);
      }
      res(trainingDataMock2 as S);
    }, 1000);
  });
};
