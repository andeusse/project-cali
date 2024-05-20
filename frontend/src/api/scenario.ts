import { AxiosResponse } from 'axios';
import api from './api';
import jsonFile from './df_mock.json';
import { SmartSystemOutput } from '../types/scenarios/common';

export const updateScenario = <T, R, S = AxiosResponse<R>>(
  scenario: string,
  body: T
): Promise<S> => {
  return api.post(`/scenarios/${scenario}`, body);
};

export const updateScenarioMock = (): Promise<SmartSystemOutput> => {
  return new Promise((res, rej) => {
    const data: SmartSystemOutput = jsonFile;
    res(data);
  });
};
