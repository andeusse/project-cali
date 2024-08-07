export type ConfigType = {
  projectName: string;
  apiUrl: string;
  grafanaUrls: string[];
  electricalUrls: string[];
  windyUrlRadiation: string;
  windyUrlTemperature: string;
  windyUrlWindSpeed: string;
  webServerDmg9000Url: string;
  powerSpoutUrl: string;
  typicalTemperatureProfile: number[];
  typicalRadiationProfile: number[];
  typicalWindSpeedProfile: number[];
  typicalHomeLoadProfile: number[];
  typicalCommercialLoadProfile: number[];
  typicalIndustrialLoadProfile: number[];
};
