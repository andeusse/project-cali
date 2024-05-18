import { AxiosResponse } from 'axios';
import api from './api';

export const updateScenario = <T, R, S = AxiosResponse<R>>(
  scenario: string,
  body: T
): Promise<S> => {
  return api.post(`/scenarios/${scenario}`, body);
};
