import { AxiosResponse } from 'axios';
import api from './api';
import { SmartSystemParameters } from '../types/scenarios/common';
import Config from '../config/config';

export const updateScenario = (
  scenario: string,
  body: SmartSystemParameters
): Promise<AxiosResponse<string>> => {
  return api.post(
    `${Config.getInstance().params.apiUrl}/scenarios/${scenario}`,
    body
  );
};
