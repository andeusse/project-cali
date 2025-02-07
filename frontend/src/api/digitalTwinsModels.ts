import { AxiosResponse } from 'axios';
import api from './api';
import Config from '../config/config';
import { TrainingDataType } from '../types/trainingData';

const trainingDataMock2: TrainingDataType = {
  names: ['Gallinaza', 'Porquinaza'],
  values: {
    Gallinaza: {
      activationEnergyR101: 0,
      activationEnergyR102: 1,
      exponentialFactorR101: 0,
      exponentialFactorR102: 1,
      lambdaR101: 0,
      lambdaR102: 1,
    },
    Porquinaza: {
      activationEnergyR101: 1,
      activationEnergyR102: 0,
      exponentialFactorR101: 1,
      exponentialFactorR102: 0,
      lambdaR101: 1,
      lambdaR102: 0,
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
  queryModel: string,
  isBiogas: boolean = true
): Promise<S> => {
  const queryParameterName = isBiogas ? 'mode' : 'method';
  return api.get(
    `${
      Config.getInstance().params.apiUrl
    }/models/${model}?${queryParameterName}=${queryMode}&model=${queryModel}`
  );
};

export const trainingDataAPIMock = <R, S = AxiosResponse<R>>(
  model: string,
  queryMode: string,
  queryModel: string,
  isBiogas: boolean = true
): Promise<S> => {
  return new Promise<S>((res, rej) => {
    setTimeout(() => {
      res(trainingDataMock2 as S);
    }, 1000);
  });
};
