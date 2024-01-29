import { ConfigType } from '../types/config';

export default class Config {
  private static instance: Config;

  public params: ConfigType;

  private constructor() {
    this.params = {
      apiUrl:
        process.env.REACT_APP_STATUS === 'dev'
          ? process.env.REACT_APP_DEV_API_URL
            ? process.env.REACT_APP_DEV_API_URL
            : ''
          : process.env.REACT_APP_PROD_API_URL
          ? process.env.REACT_APP_PROD_API_URL
          : '',
    };
  }

  static getInstance() {
    if (!this.instance) {
      this.instance = new Config();
    }
    return this.instance;
  }
}
