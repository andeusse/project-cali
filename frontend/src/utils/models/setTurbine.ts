import Config from '../../config/config';
import {
  PELTON_TURBINE_CONST,
  TURGO_TURBINE_CONST,
  TurbineParameters,
  TurbineType,
} from '../../types/models/turbine';
import { getKeyByValue } from '../getKeyByValue';

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
    newState.inputPressure.arrayDisabled = false;
    newState.inputFlow.disabled = !newState.inputOfflineOperation;
    newState.inputFlow.arrayDisabled = false;
    newState.inputActivePower.disabled = !newState.inputOfflineOperation;
    newState.inputActivePower.arrayDisabled = false;
    newState.inputPowerFactor.disabled = !newState.inputOfflineOperation;
    newState.inputPowerFactor.arrayDisabled = false;

    newState.timeMultiplier.disabled = !newState.inputOfflineOperation;
    if (!newState.inputOfflineOperation) {
      newState.timeMultiplier.value = 1;
    }
  }
  return newState;
};
