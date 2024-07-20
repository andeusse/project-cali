import { CellChange } from '@silevis/reactgrid';
import Config from '../../config/config';
import {
  PELTON_TURBINE_CONST,
  TURGO_TURBINE_CONST,
  TurbineParameters,
  TurbineType,
} from '../../types/models/turbine';
import { getKeyByValue } from '../getKeyByValue';
import { CellChange2Array } from '../cellChange2Array';

export const setTurbine = (
  e: any,
  oldState: TurbineParameters
): TurbineParameters => {
  let newState = { ...oldState };
  if (e.target.name === 'turbineType') {
    const turbineType = getKeyByValue(
      TurbineType,
      e.target.value
    ) as TurbineType;
    newState.turbineType = turbineType;
    if (turbineType === TurbineType.Pelton) {
      newState.inputPressure = PELTON_TURBINE_CONST.inputPressure;
      newState.inputFlow = PELTON_TURBINE_CONST.inputFlow;
    } else {
      newState.inputPressure = TURGO_TURBINE_CONST.inputPressure;
      newState.inputFlow = TURGO_TURBINE_CONST.inputFlow;
    }
  }
  if (e.target.name === 'controller.customize') {
    newState.controller.customize = e.target.checked;
    newState.controller.chargeVoltageBulk.disabled = !e.target.checked;
    newState.controller.chargeVoltageFloat.disabled = !e.target.checked;
    newState.controller.chargingMinimunVoltage.disabled = !e.target.checked;
    newState.controller.sinkOffVoltage.disabled = !e.target.checked;
    newState.controller.sinkOnVoltage.disabled = !e.target.checked;
  }
  if (e.target.name === 'inputOfflineOperation') {
    newState.inputOfflineOperation = !newState.inputOfflineOperation;
    newState.queryTime = newState.inputOfflineOperation
      ? Config.QUERY_TIME_OFFLINE
      : Config.QUERY_TIME_ONLINE;
    newState.inputPressure.disabled = !newState.inputOfflineOperation;
    newState.inputPressure.arrayEnabled = false;
    newState.inputFlow.disabled = !newState.inputOfflineOperation;
    newState.inputFlow.arrayEnabled = false;
    newState.inputActivePower.disabled = !newState.inputOfflineOperation;
    newState.inputActivePower.arrayEnabled = false;
    newState.inputPowerFactor.disabled = !newState.inputOfflineOperation;
    newState.inputPowerFactor.arrayEnabled = false;

    newState.timeMultiplier.disabled = !newState.inputOfflineOperation;
    if (!newState.inputOfflineOperation) {
      newState.timeMultiplier.value = 1;
    }
  }
  if (e.target.name === 'steps') {
    const value: number = parseInt(e.target.value);
    newState.steps.value = value;
    newState.inputPressureArray = Array(value ? value : 1).fill(22);
    newState.inputFlowArray = Array(value ? value : 1).fill(6);
    newState.inputActivePowerArray = Array(value ? value : 1).fill(200);
    newState.inputPowerFactorArray = Array(value ? value : 1).fill(1);
    if (value === 1) {
      newState.inputPressure.arrayEnabled = false;
      newState.inputFlow.arrayEnabled = false;
      newState.inputActivePower.arrayEnabled = false;
      newState.inputPowerFactor.arrayEnabled = false;
    }
  }
  return newState;
};

export const setTurbineTable = (
  e: CellChange[],
  oldState: TurbineParameters
) => {
  const newState = { ...oldState };
  let oldArray: number[][] = [];
  oldArray.push(newState.inputPressureArray);
  oldArray.push(newState.inputFlowArray);
  oldArray.push(newState.inputActivePowerArray);
  oldArray.push(newState.inputPowerFactorArray);

  const newArrays = CellChange2Array(e, oldArray);
  if (newState.inputPressure.arrayEnabled)
    newState.inputPressureArray = newArrays[0].map((v) => {
      v = v < 30 ? v : 30;
      v = v > 0 ? v : 0;
      return v;
    });
  if (newState.inputFlow.arrayEnabled)
    newState.inputFlowArray = newArrays[1].map((v) => {
      v = v < 15 ? v : 15;
      v = v > 0 ? v : 0;
      return v;
    });
  if (newState.inputActivePower.arrayEnabled)
    newState.inputActivePowerArray = newArrays[2].map((v) => {
      v = v < 100000 ? v : 100000;
      v = v > 0 ? v : 0;
      return v;
    });
  if (newState.inputPowerFactor.arrayEnabled)
    newState.inputPowerFactorArray = newArrays[3].map((v) => {
      v = v < 1 ? v : 1;
      v = v > -1 ? v : -1;
      return v;
    });
  return newState;
};
