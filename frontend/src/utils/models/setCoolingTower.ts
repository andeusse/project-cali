import { CellChange } from '@silevis/reactgrid';
import { CoolingTowerParameters } from '../../types/models/coolingTower';
import { CellChange2Array } from '../cellChange2Array';
import Config from '../../config/config';

export const setCoolingTower = (e: any, oldState: CoolingTowerParameters) => {
  let newState = { ...oldState };
  if (e.target.name === 'inputOfflineOperation') {
    newState.inputOfflineOperation = !newState.inputOfflineOperation;
    newState.queryTime = newState.inputOfflineOperation
      ? Config.QUERY_TIME_OFFLINE_TOWER
      : Config.QUERY_TIME_ONLINE_TOWER;

    newState.topWaterFlow.disabled = !newState.inputOfflineOperation;
    newState.topWaterFlow.arrayEnabled = false;
    newState.topWaterTemperature.disabled = !newState.inputOfflineOperation;
    newState.topWaterTemperature.arrayEnabled = false;
    newState.bottomAirFlow.disabled = !newState.inputOfflineOperation;
    newState.bottomAirFlow.arrayEnabled = false;
    newState.bottomAirTemperature.disabled = !newState.inputOfflineOperation;
    newState.bottomAirTemperature.arrayEnabled = false;
    newState.bottomAirHumidity.disabled = !newState.inputOfflineOperation;
    newState.bottomAirHumidity.arrayEnabled = false;

    newState.timeMultiplier.disabled = !newState.inputOfflineOperation;
  }
  if (e.target.name === 'steps') {
    const value: number = parseInt(e.target.value);
    newState.steps.value = value;
    newState.topWaterFlowArray = Array(value ? value : 1).fill(1);
    newState.topWaterTemperatureArray = Array(value ? value : 1).fill(35);
    newState.bottomAirFlowArray = Array(value ? value : 1).fill(2);
    newState.bottomAirTemperatureArray = Array(value ? value : 1).fill(29);
    newState.bottomAirHumidityArray = Array(value ? value : 1).fill(65);
    if (value === 1) {
      newState.topWaterFlow.arrayEnabled = false;
      newState.topWaterTemperature.arrayEnabled = false;
      newState.bottomAirFlow.arrayEnabled = false;
      newState.bottomAirTemperature.arrayEnabled = false;
      newState.bottomAirHumidity.arrayEnabled = false;
    } else {
      newState.timeMultiplier.value = 1;
    }
  }

  return newState;
};

export const setCoolingTowerTable = (
  e: CellChange[],
  oldState: CoolingTowerParameters
) => {
  const newState = { ...oldState };
  let oldArray: number[][] = [];
  oldArray.push(newState.topWaterFlowArray);
  oldArray.push(newState.topWaterTemperatureArray);
  oldArray.push(newState.bottomAirFlowArray);
  oldArray.push(newState.bottomAirTemperatureArray);
  oldArray.push(newState.bottomAirHumidityArray);

  const newArrays = CellChange2Array(e, oldArray);

  if (newState.topWaterFlow.arrayEnabled)
    newState.topWaterFlowArray = newArrays[0].map((v) => {
      v = v < 10 ? v : 10;
      v = v > 0 ? v : 0;
      return v;
    });
  if (newState.topWaterTemperature.arrayEnabled)
    newState.topWaterTemperatureArray = newArrays[1].map((v) => {
      v = v < 100 ? v : 100;
      v = v > 0 ? v : 0;
      return v;
    });
  if (newState.bottomAirFlow.arrayEnabled)
    newState.bottomAirFlowArray = newArrays[2].map((v) => {
      v = v < 40 ? v : 40;
      v = v > -20 ? v : -20;
      return v;
    });
  if (newState.bottomAirTemperature.arrayEnabled)
    newState.bottomAirTemperatureArray = newArrays[3].map((v) => {
      v = v < 100 ? v : 100;
      v = v > 0 ? v : 0;
      return v;
    });
  if (newState.bottomAirHumidity.arrayEnabled)
    newState.bottomAirHumidityArray = newArrays[4].map((v) => {
      v = v < 30 ? v : 30;
      v = v > 0 ? v : 0;
      return v;
    });
  return newState;
};
