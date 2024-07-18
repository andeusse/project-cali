import {
  OperationModeType,
  SolarWindParameters,
} from '../../types/models/solar';
import { setFormObjectValue } from '../setFormObjectValue';
import { getKeyByValue } from '../getKeyByValue';
import Config from '../../config/config';

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
  if (e.target.name === 'hybridInverter.customize') {
    newState.hybridInverter.customize = e.target.checked;
    newState.hybridInverter.chargeVoltageBulk.disabled = !e.target.checked;
    newState.hybridInverter.chargeVoltageFloat.disabled = !e.target.checked;
    newState.hybridInverter.chargingMinimunVoltage.disabled = !e.target.checked;
  }
  if (name === 'inputOfflineOperation') {
    newState.inputOfflineOperation = !newState.inputOfflineOperation;
    newState.queryTime = newState.inputOfflineOperation
      ? Config.QUERY_TIME_OFFLINE
      : Config.QUERY_TIME_ONLINE;
    newState.solarRadiation1.disabled = !newState.inputOfflineOperation;
    newState.solarRadiation2.disabled = !newState.inputOfflineOperation;
    newState.windSpeed.disabled = !newState.inputOfflineOperation;

    newState.solarRadiation1.arrayDisabled = false;
    newState.solarRadiation2.arrayDisabled = false;
    newState.temperature.arrayDisabled = false;
    newState.windSpeed.arrayDisabled = false;
    newState.windDensity.arrayDisabled = false;

    newState.alternCurrentLoadPower.disabled = !newState.inputOfflineOperation;
    newState.alternCurrentLoadPowerFactor.disabled =
      !newState.inputOfflineOperation;
    newState.directCurrentLoadPower.disabled = !newState.inputOfflineOperation;

    newState.timeMultiplier.disabled = !newState.inputOfflineOperation;
    if (!newState.inputOfflineOperation) {
      newState.timeMultiplier.value = 1;
    }
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
        newState.offgridInverter.isConnectedDisabled = false;
        newState.hybridInverter.isConnected = false;

        newState.controller.chargeVoltageBulk.value = 13.6;
        newState.controller.chargeVoltageFloat.value = 13.9;
        newState.controller.chargingMinimunVoltage.value = 11.5;
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

        newState.offgridInverter.isConnected = true;
        newState.offgridInverter.isConnectedDisabled = false;
        newState.hybridInverter.isConnected = false;
        newState.hybridInverter.isConnectedDisabled = true;

        newState.controller.chargeVoltageBulk.value = 27.2;
        newState.controller.chargeVoltageFloat.value = 27.8;
        newState.controller.chargingMinimunVoltage.value = 23;
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

        newState.hybridInverter.isConnected = false;

        newState.controller.chargeVoltageBulk.value = 13.6;
        newState.controller.chargeVoltageFloat.value = 13.9;
        newState.controller.chargingMinimunVoltage.value = 11.5;
        break;
      case OperationModeType.Mode4:
        newState.monocrystallinePanel.isConnected = false;
        newState.policrystallinePanel.isConnected = false;
        newState.flexPanel.isConnected = false;
        newState.cadmiumTelluridePanel.isConnected = false;

        newState.isBattery2 = false;

        newState.hybridInverter.isConnected = false;

        newState.controller.chargeVoltageBulk.value = 13.6;
        newState.controller.chargeVoltageFloat.value = 13.9;
        newState.controller.chargingMinimunVoltage.value = 11.5;
        break;
      case OperationModeType.Mode5:
        newState.monocrystallinePanel.isConnected = true;
        newState.policrystallinePanel.isConnected = false;
        newState.flexPanel.isConnected = false;
        newState.cadmiumTelluridePanel.isConnected = false;

        newState.monocrystallinePanel.isConnectedDisabled = false;
        newState.policrystallinePanel.isConnectedDisabled = false;
        newState.flexPanel.isConnectedDisabled = false;

        newState.isBattery2 = false;

        newState.hybridInverter.isConnected = false;

        newState.controller.chargeVoltageBulk.value = 13.6;
        newState.controller.chargeVoltageFloat.value = 13.9;
        newState.controller.chargingMinimunVoltage.value = 11.5;
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

            newState.controller.chargeVoltageBulk.value = 13.6;
            newState.controller.chargeVoltageFloat.value = 13.9;
            newState.controller.chargingMinimunVoltage.value = 11.5;
          } else if (newState.inputOperationMode !== OperationModeType.Mode5) {
            newState.policrystallinePanel.isConnected = true;
            newState.flexPanel.isConnected = true;

            newState.monocrystallinePanel.isConnectedDisabled = true;
            newState.policrystallinePanel.isConnectedDisabled = false;
            newState.flexPanel.isConnectedDisabled = false;
          } else {
            if (
              newState.monocrystallinePanel.isConnected &&
              newState.policrystallinePanel.isConnected &&
              newState.flexPanel.isConnected
            ) {
              newState.flexPanel.isConnected = false;
            }
          }
          break;
        case 'policrystallinePanel':
          if (newState.inputOperationMode === OperationModeType.Mode1) {
            newState.monocrystallinePanel.isConnected = false;
            newState.flexPanel.isConnected = false;
            newState.cadmiumTelluridePanel.isConnected = false;
            newState.isBattery2 = false;

            newState.controller.chargeVoltageBulk.value = 13.6;
            newState.controller.chargeVoltageFloat.value = 13.9;
            newState.controller.chargingMinimunVoltage.value = 11.5;
          } else if (newState.inputOperationMode !== OperationModeType.Mode5) {
            newState.monocrystallinePanel.isConnected = true;
            newState.flexPanel.isConnected = true;

            newState.monocrystallinePanel.isConnectedDisabled = false;
            newState.policrystallinePanel.isConnectedDisabled = true;
            newState.flexPanel.isConnectedDisabled = false;
          } else {
            if (
              newState.monocrystallinePanel.isConnected &&
              newState.policrystallinePanel.isConnected &&
              newState.flexPanel.isConnected
            ) {
              newState.flexPanel.isConnected = false;
            }
          }
          break;
        case 'flexPanel':
          if (newState.inputOperationMode === OperationModeType.Mode1) {
            newState.monocrystallinePanel.isConnected = false;
            newState.policrystallinePanel.isConnected = false;
            newState.cadmiumTelluridePanel.isConnected = false;
            newState.isBattery2 = false;

            newState.controller.chargeVoltageBulk.value = 13.6;
            newState.controller.chargeVoltageFloat.value = 13.9;
            newState.controller.chargingMinimunVoltage.value = 11.5;
          } else if (newState.inputOperationMode !== OperationModeType.Mode5) {
            newState.monocrystallinePanel.isConnected = true;
            newState.policrystallinePanel.isConnected = true;

            newState.monocrystallinePanel.isConnectedDisabled = false;
            newState.policrystallinePanel.isConnectedDisabled = false;
            newState.flexPanel.isConnectedDisabled = true;
          } else {
            if (
              newState.monocrystallinePanel.isConnected &&
              newState.policrystallinePanel.isConnected &&
              newState.flexPanel.isConnected
            ) {
              newState.policrystallinePanel.isConnected = false;
            }
          }
          break;
        case 'cadmiumTelluridePanel':
          if (newState.inputOperationMode === OperationModeType.Mode1) {
            newState.monocrystallinePanel.isConnected = false;
            newState.policrystallinePanel.isConnected = false;
            newState.flexPanel.isConnected = false;

            newState.isBattery2 = true;
            newState.controller.chargeVoltageBulk.value = 27.2;
            newState.controller.chargeVoltageFloat.value = 27.8;
            newState.controller.chargingMinimunVoltage.value = 23;
          }
          break;
        case 'offgridInverter':
          if (!newState.offgridInverter.isConnected) {
            newState.offgridInverter.isConnectedDisabled =
              !newState.offgridInverter.isConnectedDisabled;
            newState.hybridInverter.isConnectedDisabled = false;
            newState.offgridInverter.isConnectedDisabled = false;
          } else {
            newState.hybridInverter.isConnectedDisabled = true;
          }
          newState.offgridInverter.isConnected = e.target.checked;
          break;
        case 'hybridInverter':
          if (!newState.hybridInverter.isConnected) {
            newState.hybridInverter.isConnectedDisabled =
              !newState.hybridInverter.isConnectedDisabled;
            newState.offgridInverter.isConnectedDisabled = false;
            newState.hybridInverter.isConnectedDisabled = false;
          } else {
            newState.offgridInverter.isConnectedDisabled = true;
          }
          newState.hybridInverter.isConnected = e.target.checked;
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
