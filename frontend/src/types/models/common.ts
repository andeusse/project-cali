import { InputType } from '../inputType';
import {
  SolarPanel as CommonSolarPanel,
  WindTurbine as CommonWindTurbine,
  Battery as CommonBattery,
} from '../common';

export type DiagramVariableType = {
  name: string;
  variable: string;
  unit: string;
  isShown: boolean;
  diagramName?: string;
  fixed?: number;
  x?: number;
  y?: number;
  hasAdditionalCondition?: number;
  scientificNotation?: boolean;
};

export type CommonDigitalTwinsParameter = {
  inputOfflineOperation: boolean;
  timeMultiplier: InputType;
  queryTime: number;
  disableParameters: boolean;
};

export type IsConnected = {
  isConnected: boolean;
  isConnectedDisabled: boolean;
};

export type SolarPanel = IsConnected &
  CommonSolarPanel & {
    peakPower: InputType;
  };

export type WindTurbine = CommonWindTurbine;

export type Battery = CommonBattery;

export type CommonController = {
  customize: boolean;
  efficiency: InputType;
  chargeVoltageBulk: InputType;
  chargeVoltageFloat: InputType;
  chargingMinimunVoltage: InputType;
};

export type Inverter = IsConnected & {
  efficiency: InputType;
  nominalPower: InputType;
};

export type InverterHybrid = IsConnected &
  Inverter & {
    customize: boolean;
    chargeVoltageBulk: InputType;
    chargeVoltageFloat: InputType;
    chargingMinimunVoltage: InputType;
  };
