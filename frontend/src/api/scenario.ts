import { AxiosResponse } from 'axios';
import api from './api';
import jsonFile from './df_mock.json';
import {
  SmartSystemOutput,
  SmartSystemParameters,
} from '../types/scenarios/common';

export const updateScenario = (
  scenario: string,
  body: SmartSystemParameters
): Promise<AxiosResponse<string>> => {
  return api.post(`/scenarios/${scenario}`, body);
};

export const updateScenarioMock = (): Promise<SmartSystemOutput> => {
  return new Promise((res, rej) => {
    const data: SmartSystemOutput = jsonFile;
    res(data);
  });
};
