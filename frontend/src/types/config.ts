export type ConfigType = {
  apiUrl: string;
  grafanaUrls: string[];
  electricalUrls: string[];
  projectName: string;
  windyUrlRadiation: string;
  windyUrlTemperature: string;
  windyUrlWindSpeed: string;
  typicalTemperatureProfile: number[];
  typicalRadiationProfile: number[];
  typicalWindSpeedProfile: number[];
  typicalHomeLoadProfile: number[];
  typicalCommercialLoadProfile: number[];
  typicalIndustrialLoadProfile: number[];
};
