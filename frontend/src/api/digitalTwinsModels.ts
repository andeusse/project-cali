import { AxiosResponse } from 'axios';
import api from './api';
import Config from '../config/config';

export const updateModel = <T, R, S = AxiosResponse<R>>(
  model: string,
  body: T
): Promise<S> => {
  return api.post(
    `${Config.getInstance().params.apiUrl}/models/${model}`,
    body
  );
};
