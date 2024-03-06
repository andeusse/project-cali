import { AxiosResponse } from 'axios';
import api from './api';

export const updateModel = <T, R, S = AxiosResponse<R>>(
  model: string,
  body: T
): Promise<S> => {
  return api.post(`/${model}`, body);
};
