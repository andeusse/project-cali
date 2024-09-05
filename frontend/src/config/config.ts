import axios from 'axios';
import { ConfigType } from '../types/config';

export default class Config {
  private static instance: Config;

  public static QUERY_TIME_OFFLINE: number = 1000;
  public static QUERY_TIME_ONLINE: number = 3000;

  public static QUERY_TIME_DIGITAL_TWIN_OFF_OFFLINE_BIOGAS: number = 3000;
  public static QUERY_TIME_DIGITAL_TWIN_ON_OFFLINE_BIOGAS: number = 30000;
  public static QUERY_TIME_DIGITAL_TWIN_OFF_ONLINE_BIOGAS: number = 3000;
  public static QUERY_TIME_DIGITAL_TWIN_ON_ONLINE_BIOGAS: number = 30000;

  public static TYPICAL_ARRAY_X_AXIS: string[] = Array(24)
    .fill(0)
    .map((_, i) => `P${i + 1}`);

  public params: ConfigType;

  private constructor() {
    this.params = {
      apiUrl: process.env.REACT_APP_DEV_API_URL_PRIVATE
        ? process.env.REACT_APP_DEV_API_URL_PRIVATE
        : '',
      grafanaUrls: process.env.REACT_APP_DEV_GRAFANA_TABS
        ? process.env.REACT_APP_DEV_GRAFANA_TABS.split(' ')
        : [],
      electricalUrls: process.env.REACT_APP_DEV_ELECTRICAL_TABS
        ? process.env.REACT_APP_DEV_ELECTRICAL_TABS.split(' ')
        : [],
      projectName: process.env.REACT_APP_TITLE
        ? process.env.REACT_APP_TITLE
        : 'Project',
      windyUrlRadiation: process.env.REACT_APP_WINDY_URL_RADIATION
        ? process.env.REACT_APP_WINDY_URL_RADIATION
        : '',
      windyUrlTemperature: process.env.REACT_APP_WINDY_URL_TEMPERATURE
        ? process.env.REACT_APP_WINDY_URL_TEMPERATURE
        : '',
      windyUrlWindSpeed: process.env.REACT_APP_WINDY_URL_WIND_SPEED
        ? process.env.REACT_APP_WINDY_URL_WIND_SPEED
        : '',
      webServerDmg9000Url: process.env.REACT_APP_WEB_SERVER_DMG9000_URL
        ? process.env.REACT_APP_WEB_SERVER_DMG9000_URL
        : '',
      powerSpoutUrl: process.env.REACT_APP_POWER_SPOUT_URL
        ? process.env.REACT_APP_POWER_SPOUT_URL
        : '',
      typicalTemperatureProfile: process.env.REACT_APP_TYPICAL_TEMP_PROFILE
        ? process.env.REACT_APP_TYPICAL_TEMP_PROFILE.split(' ').map((n) =>
            parseFloat(n)
          )
        : [],
      typicalRadiationProfile: process.env.REACT_APP_TYPICAL_RADIATION_PROFILE
        ? process.env.REACT_APP_TYPICAL_RADIATION_PROFILE.split(' ').map((n) =>
            parseFloat(n)
          )
        : [],
      typicalWindSpeedProfile: process.env.REACT_APP_TYPICAL_WIND_SPEED_PROFILE
        ? process.env.REACT_APP_TYPICAL_WIND_SPEED_PROFILE.split(' ').map((n) =>
            parseFloat(n)
          )
        : [],
      typicalHomeLoadProfile: process.env.REACT_APP_TYPICAL_HOME_LOAD_PROFILE
        ? process.env.REACT_APP_TYPICAL_HOME_LOAD_PROFILE.split(' ').map((n) =>
            parseFloat(n)
          )
        : [],
      typicalCommercialLoadProfile: process.env
        .REACT_APP_TYPICAL_COMMERCIAL_LOAD_PROFILE
        ? process.env.REACT_APP_TYPICAL_COMMERCIAL_LOAD_PROFILE.split(' ').map(
            (n) => parseFloat(n)
          )
        : [],
      typicalIndustrialLoadProfile: process.env
        .REACT_APP_TYPICAL_INDUSTRIAL_LOAD_PROFILE
        ? process.env.REACT_APP_TYPICAL_INDUSTRIAL_LOAD_PROFILE.split(' ').map(
            (n) => parseFloat(n)
          )
        : [],
    };

    axios
      .get(this.params.apiUrl, { timeout: 1000 })
      .then(() => {
        console.log(this.params.apiUrl);
      })
      .catch(() => {
        this.params.apiUrl = process.env.REACT_APP_DEV_API_URL_PUBLIC
          ? process.env.REACT_APP_DEV_API_URL_PUBLIC
          : '';
        console.log(this.params.apiUrl);
      });
  }

  static getInstance() {
    if (!this.instance) {
      this.instance = new Config();
    }
    return this.instance;
  }
}
