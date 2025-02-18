import { BiochemicalMethanePotentialParameters } from './models/biochemicalMethanePotential';
import { BiogasParameters } from './models/biogas';
import { CoolingTowerParameters } from './models/coolingTower';
import { HydrogencellParameters } from './models/hydrogenCell';
import { SolarWindParameters } from './models/solar';
import { TurbineParameters } from './models/turbine';

export type digitalTwinsType =
  | TurbineParameters
  | SolarWindParameters
  | BiogasParameters
  | CoolingTowerParameters
  | HydrogencellParameters
  | BiochemicalMethanePotentialParameters;
