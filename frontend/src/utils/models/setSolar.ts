import {
  OperationModeType,
  SolarWindParameters,
} from '../../types/models/solar';
import { setFormObjectValue } from '../setFormObjectValue';
import { getKeyByValue } from '../getKeyByValue';

export const setSolar = (
  e: any,
  oldState: SolarWindParameters
): SolarWindParameters => {
  const name = e.target.name as string;
  const type = e.target.type as string;
  const splitName = name.split('.');

  let newState = { ...oldState };
  if (name === 'controller.customize') {
    newState.controller.customize = e.target.checked;
    newState.controller.chargeVoltageBulk.disabled = !e.target.checked;
    newState.controller.chargeVoltageFloat.disabled = !e.target.checked;
    newState.controller.chargingMinimunVoltage.disabled = !e.target.checked;
  }
  if (name === 'inputOfflineOperation') {
    newState.inputOfflineOperation = !newState.inputOfflineOperation;
    newState.solarRadiation1.disabled = !newState.inputOfflineOperation;
    newState.solarRadiation2.disabled = !newState.inputOfflineOperation;
    newState.temperature.disabled = !newState.inputOfflineOperation;
    newState.windSpeed.disabled = !newState.inputOfflineOperation;
    newState.windDensity.disabled = !newState.inputOfflineOperation;
    newState.alternCurrentLoadPower.disabled = !newState.inputOfflineOperation;
    newState.alternCurrentLoadPowerFactor.disabled =
      !newState.inputOfflineOperation;
    newState.directCurrentLoadPower.disabled = !newState.inputOfflineOperation;
  }
  if (name === 'inputOperationMode') {
    const operationMode = getKeyByValue(OperationModeType, e.target.value);
    newState.inputOperationMode = operationMode;
    switch (operationMode) {
      case OperationModeType.Mode1:
        newState.monocrystallinePanel.isConnected = true;
        newState.policrystallinePanel.isConnected = false;
        newState.flexPanel.isConnected = false;
        newState.cadmiumTelluridePanel.isConnected = false;

        newState.monocrystallinePanel.isConnectedDisabled = false;
        newState.policrystallinePanel.isConnectedDisabled = false;
        newState.flexPanel.isConnectedDisabled = false;
        newState.cadmiumTelluridePanel.isConnectedDisabled = false;

        newState.isBattery2 = false;
        break;
      case OperationModeType.Mode2:
        newState.monocrystallinePanel.isConnected = true;
        newState.policrystallinePanel.isConnected = true;
        newState.flexPanel.isConnected = false;
        newState.cadmiumTelluridePanel.isConnected = false;

        newState.monocrystallinePanel.isConnectedDisabled = false;
        newState.policrystallinePanel.isConnectedDisabled = false;
        newState.flexPanel.isConnectedDisabled = true;

        newState.isBattery2 = true;

        newState.offgridInverter.isConnected = false;
        newState.offgridInverter.isConnectedDisabled = true;
        newState.hybridInverter.isConnected = true;
        newState.hybridInverter.isConnectedDisabled = false;
        break;
      case OperationModeType.Mode3:
        newState.monocrystallinePanel.isConnected = true;
        newState.policrystallinePanel.isConnected = true;
        newState.flexPanel.isConnected = false;
        newState.cadmiumTelluridePanel.isConnected = false;

        newState.monocrystallinePanel.isConnectedDisabled = false;
        newState.policrystallinePanel.isConnectedDisabled = false;
        newState.flexPanel.isConnectedDisabled = true;

        newState.isBattery2 = false;
        break;
      case OperationModeType.Mode4:
        newState.monocrystallinePanel.isConnected = false;
        newState.policrystallinePanel.isConnected = false;
        newState.flexPanel.isConnected = false;
        newState.cadmiumTelluridePanel.isConnected = false;

        newState.isBattery2 = false;
        break;
      case OperationModeType.Mode5:
        newState.monocrystallinePanel.isConnected = true;
        newState.policrystallinePanel.isConnected = true;
        newState.flexPanel.isConnected = false;
        newState.cadmiumTelluridePanel.isConnected = false;

        newState.monocrystallinePanel.isConnectedDisabled = false;
        newState.policrystallinePanel.isConnectedDisabled = false;
        newState.flexPanel.isConnectedDisabled = true;

        newState.isBattery2 = false;
        break;
    }
  }
  if (splitName.length !== 1 && splitName[1] === 'isConnected') {
    if (splitName.length === 2) {
      let newValue = e.target.value;
      if (type === 'checkbox') {
        newValue = e.target.checked;
      }
      newState = setFormObjectValue<SolarWindParameters>(
        oldState,
        splitName,
        newValue
      );
      switch (splitName[0]) {
        case 'monocrystallinePanel':
          if (newState.inputOperationMode === OperationModeType.Mode1) {
            newState.policrystallinePanel.isConnected = false;
            newState.flexPanel.isConnected = false;
            newState.cadmiumTelluridePanel.isConnected = false;
            newState.isBattery2 = false;
          } else {
            newState.policrystallinePanel.isConnected = true;
            newState.flexPanel.isConnected = true;

            newState.monocrystallinePanel.isConnectedDisabled = true;
            newState.policrystallinePanel.isConnectedDisabled = false;
            newState.flexPanel.isConnectedDisabled = false;
          }
          break;
        case 'policrystallinePanel':
          if (newState.inputOperationMode === OperationModeType.Mode1) {
            newState.monocrystallinePanel.isConnected = false;
            newState.flexPanel.isConnected = false;
            newState.cadmiumTelluridePanel.isConnected = false;
            newState.isBattery2 = false;
          } else {
            newState.monocrystallinePanel.isConnected = true;
            newState.flexPanel.isConnected = true;

            newState.monocrystallinePanel.isConnectedDisabled = false;
            newState.policrystallinePanel.isConnectedDisabled = true;
            newState.flexPanel.isConnectedDisabled = false;
          }
          break;
        case 'flexPanel':
          if (newState.inputOperationMode === OperationModeType.Mode1) {
            newState.monocrystallinePanel.isConnected = false;
            newState.policrystallinePanel.isConnected = false;
            newState.cadmiumTelluridePanel.isConnected = false;
            newState.isBattery2 = false;
          } else {
            newState.monocrystallinePanel.isConnected = true;
            newState.policrystallinePanel.isConnected = true;

            newState.monocrystallinePanel.isConnectedDisabled = false;
            newState.policrystallinePanel.isConnectedDisabled = false;
            newState.flexPanel.isConnectedDisabled = true;
          }
          break;
        case 'cadmiumTelluridePanel':
          if (newState.inputOperationMode === OperationModeType.Mode1) {
            newState.monocrystallinePanel.isConnected = false;
            newState.policrystallinePanel.isConnected = false;
            newState.flexPanel.isConnected = false;

            newState.isBattery2 = true;
          }
          break;
        case 'offgridInverter':
          newState.offgridInverter.isConnectedDisabled =
            !newState.offgridInverter.isConnected;
          newState.hybridInverter.isConnected = true;
          newState.hybridInverter.isConnectedDisabled = false;
          break;
        case 'hybridInverter':
          newState.hybridInverter.isConnectedDisabled =
            !newState.hybridInverter.isConnectedDisabled;
          newState.offgridInverter.isConnected = true;
          newState.offgridInverter.isConnectedDisabled = false;
          break;
      }
      const allFalse =
        newState.monocrystallinePanel.isConnected ||
        newState.policrystallinePanel.isConnected ||
        newState.flexPanel.isConnected ||
        newState.cadmiumTelluridePanel.isConnected;
      if (!allFalse) {
        newState.monocrystallinePanel.isConnected = true;
      }
    }
  }
  return newState;
};
