import { AxiosResponse } from 'axios';
import api from './api';
import { SmartSystemParameters } from '../types/scenarios/common';

export const updateScenario = (
  scenario: string,
  body: SmartSystemParameters
): Promise<AxiosResponse<string>> => {
  return api.post(`/scenarios/${scenario}`, body);
};
