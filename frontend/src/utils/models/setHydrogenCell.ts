import { CellChange } from '@silevis/reactgrid';
import {
  ElectronicLoadModeType,
  HydrogencellParameters,
} from '../../types/models/hydrogenCell';
import { CellChange2Array } from '../cellChange2Array';
import Config from '../../config/config';

export const setHydrogenCell = (
  e: any,
  oldState: HydrogencellParameters
): HydrogencellParameters => {
  let newState = { ...oldState };
  if (e.target.name === 'inputOfflineOperation') {
    newState.inputOfflineOperation = !newState.inputOfflineOperation;
    newState.queryTime = newState.inputOfflineOperation
      ? Config.QUERY_TIME_OFFLINE
      : Config.QUERY_TIME_ONLINE;
    newState.inputHydrogenFlow.disabled = !newState.inputOfflineOperation;
    newState.inputHydrogenFlow.arrayEnabled = false;
    newState.inputHydrogenPressure.disabled = !newState.inputOfflineOperation;
    newState.inputHydrogenPressure.arrayEnabled = false;
    newState.inputCellTemperature.disabled = !newState.inputOfflineOperation;
    newState.inputCellTemperature.arrayEnabled = false;
    newState.inputElectronicLoadCurrent.disabled =
      !newState.inputOfflineOperation;
    newState.inputElectronicLoadCurrent.arrayEnabled = false;
    newState.inputElectronicLoadPower.disabled =
      !newState.inputOfflineOperation;
    newState.inputElectronicLoadPower.arrayEnabled = false;
    newState.inputElectronicLoadResistance.disabled =
      !newState.inputOfflineOperation;
    newState.inputElectronicLoadResistance.arrayEnabled = false;
    newState.inputFanPercentage.disabled = !newState.inputOfflineOperation;
    newState.inputFanPercentage.arrayEnabled = false;

    newState.timeMultiplier.disabled = !newState.inputOfflineOperation;
    if (!newState.inputOfflineOperation) {
      newState.timeMultiplier.value = 1;
    }
  }
  if (e.target.name === 'steps') {
    const value: number = parseInt(e.target.value);
    newState.steps.value = value;
    newState.inputHydrogenFlowArray = Array(value ? value : 1).fill(0.4);
    newState.inputHydrogenPressureArray = Array(value ? value : 1).fill(5);
    newState.inputCellTemperatureArray = Array(value ? value : 1).fill(30);
    newState.inputElectronicLoadCurrentArray = Array(value ? value : 1).fill(3);
    newState.inputElectronicLoadPowerArray = Array(value ? value : 1).fill(20);
    newState.inputElectronicLoadResistanceArray = Array(value ? value : 1).fill(
      4
    );
    newState.inputFanPercentageArray = Array(value ? value : 1).fill(100);
    if (value === 1) {
      newState.inputHydrogenFlow.arrayEnabled = false;
      newState.inputHydrogenPressure.arrayEnabled = false;
      newState.inputCellTemperature.arrayEnabled = false;
      newState.inputElectronicLoadCurrent.arrayEnabled = false;
      newState.inputElectronicLoadPower.arrayEnabled = false;
      newState.inputElectronicLoadResistance.arrayEnabled = false;
    } else {
      newState.timeMultiplier.value = 1;
    }
  }
  return newState;
};

export const setHydrogenCellTable = (
  e: CellChange[],
  oldState: HydrogencellParameters
) => {
  const newState = { ...oldState };
  let oldArray: number[][] = [];
  oldArray.push(newState.inputHydrogenFlowArray);
  oldArray.push(newState.inputHydrogenPressureArray);
  oldArray.push(newState.inputCellTemperatureArray);
  oldArray.push(newState.inputElectronicLoadCurrentArray);
  oldArray.push(newState.inputElectronicLoadPowerArray);
  oldArray.push(newState.inputElectronicLoadResistanceArray);
  oldArray.push(newState.inputFanPercentageArray);

  const newArrays = CellChange2Array(e, oldArray);
  if (newState.inputHydrogenFlow.arrayEnabled)
    newState.inputHydrogenFlowArray = newArrays[0].map((v) => {
      v = v < 1 ? v : 1;
      v = v > 0 ? v : 0;
      return v;
    });
  if (newState.inputHydrogenPressure.arrayEnabled)
    newState.inputHydrogenPressureArray = newArrays[1].map((v) => {
      v = v < 6 ? v : 6;
      v = v > 3 ? v : 3;
      return v;
    });
  if (newState.inputCellTemperature.arrayEnabled)
    newState.inputCellTemperatureArray = newArrays[2].map((v) => {
      v = v < 50 ? v : 50;
      v = v > 0 ? v : 0;
      return v;
    });
  if (
    newState.inputElectronicLoadCurrent.arrayEnabled &&
    newState.electronicLoadMode === ElectronicLoadModeType.Current
  )
    newState.inputElectronicLoadCurrentArray = newArrays[3].map((v) => {
      v = v < 10 ? v : 10;
      v = v > 0 ? v : 0;
      return v;
    });
  if (
    newState.inputElectronicLoadPower.arrayEnabled &&
    newState.electronicLoadMode === ElectronicLoadModeType.Power
  )
    newState.inputElectronicLoadPowerArray = newArrays[4].map((v) => {
      v = v < 100 ? v : 100;
      v = v > 0 ? v : 0;
      return v;
    });
  if (
    newState.inputElectronicLoadResistance.arrayEnabled &&
    newState.electronicLoadMode === ElectronicLoadModeType.Resistance
  )
    newState.inputElectronicLoadResistanceArray = newArrays[5].map((v) => {
      v = v < 100 ? v : 100;
      v = v > 2 ? v : 2;
      return v;
    });
  if (newState.inputFanPercentage.arrayEnabled)
    newState.inputFanPercentageArray = newArrays[6].map((v) => {
      v = v < 100 ? v : 100;
      v = v > 0 ? v : 0;
      return v;
    });
  return newState;
};
