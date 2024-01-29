import axios from 'axios';
import Config from '../config/config';

const api = axios.create({
  baseURL: Config.getInstance().params.apiUrl,
});

export default api;
