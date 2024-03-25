import { InputType } from '../types/models/common';
import { TurbineParameters } from '../types/models/turbine';
import { SolarPanelParameters } from '../types/models/solar';
import { BiogasParameters, OperationModeType } from '../types/models/biogas';
import { SmartCityParameters } from '../types/models/smartCity';
import { getKeyByValue } from './getKeyByValue';

export const setFormState = <
  T extends
    | TurbineParameters
    | SolarPanelParameters
    | BiogasParameters
    | SmartCityParameters
>(
  e: any,
  oldState: T,
  variableName?: string
) => {
  let newState = { ...oldState };
  if (e.target.name === 'controllerCustomize') {
    if ('turbineType' in newState) {
      newState.controllerCustomize = e.target.checked;
      newState.controllerChargeVoltageBulk.disabled = !e.target.checked;
      newState.controllerChargeVoltageFloat.disabled = !e.target.checked;
      newState.controllerChargingMinimunVoltage.disabled = !e.target.checked;
      newState.controllerSinkOffVoltage.disabled = !e.target.checked;
      newState.controllerSinkOnVoltage.disabled = !e.target.checked;
    }
  } else if (e.target.name === 'inputOfflineOperation') {
    if ('turbineType' in newState) {
      newState.inputOfflineOperation = !newState.inputOfflineOperation;
      newState.inputPressure.disabled = !newState.inputOfflineOperation;
      newState.inputFlow.disabled = !newState.inputOfflineOperation;
      newState.inputActivePower.disabled = !newState.inputOfflineOperation;
      newState.inputPowerFactor.disabled = !newState.inputOfflineOperation;
    }
    if ('anaerobicReactorVolume1' in newState) {
      newState.inputOfflineOperation = !newState.inputOfflineOperation;
      newState.inputSubstrateConditions = newState.inputOfflineOperation;

      (newState as BiogasParameters) = setSubstrateConditions(
        newState,
        !newState.inputOfflineOperation
      );
    }
    if ('timeMultiplier' in newState) {
      newState.timeMultiplier.disabled = !newState.inputOfflineOperation;
      if (!newState.inputOfflineOperation) {
        newState.timeMultiplier.value = 1;
      }
    }
  } else if (e.target.name === 'inputDigitalTwin') {
    if ('anaerobicReactorVolume1' in newState) {
      newState.inputDigitalTwin = !newState.inputDigitalTwin;

      newState.inputDigitalTwinTrainingTime.disabled =
        !newState.inputDigitalTwin;
      newState.inputKineticParameterInitialValue.disabled =
        !newState.inputDigitalTwin;

      newState.inputSpeedLawExponentialFactor.disabled =
        newState.inputDigitalTwin;
      newState.inputSpeedLawStartEnergy.disabled = newState.inputDigitalTwin;
    }
  } else if (e.target.name === 'inputSubstrateConditions') {
    if ('anaerobicReactorVolume1' in newState) {
      newState.inputSubstrateConditions = !newState.inputSubstrateConditions;
      (newState as BiogasParameters) = setSubstrateConditions(
        newState,
        !newState.inputSubstrateConditions
      );
    }
  } else if (e.target.name === 'inputPump104') {
    if ('anaerobicReactorVolume1' in newState) {
      newState.inputPump104 = !newState.inputPump104;
      newState.inputPump104HydraulicRetentionTime.disabled =
        !newState.inputPump104;
      newState.inputPump104StartTime.disabled = !newState.inputPump104;
      newState.inputPump104StartsPerDay.disabled = !newState.inputPump104;
    }
  } else if (e.target.name === 'inputPump102') {
    if ('anaerobicReactorVolume1' in newState) {
      newState.inputPump102 = !newState.inputPump102;
      newState.inputPump102Flow.disabled = !newState.inputPump102;
      newState.inputPump102StartTime.disabled = !newState.inputPump102;
      newState.inputPump102StartsPerDay.disabled = !newState.inputPump102;
    }
  } else if (e.target.name === 'inputPump101') {
    if ('anaerobicReactorVolume1' in newState) {
      newState.inputPump101 = !newState.inputPump101;
      newState.inputPump101Flow.disabled = !newState.inputPump101;
      newState.inputPump101StartTime.disabled = !newState.inputPump101;
      newState.inputPump101StartsPerDay.disabled = !newState.inputPump101;
    }
  } else if (e.target.name === 'inputOperationMode') {
    if ('anaerobicReactorVolume1' in newState) {
      newState.inputOperationMode = getKeyByValue(
        OperationModeType,
        e.target.value
      );
    }
  } else if (
    e.target.type === 'checkbox' &&
    e.target.name === 'variableCustomize'
  ) {
    if (variableName) {
      (newState[variableName as keyof T] as InputType).disabled =
        !e.target.checked;
    }
  } else if (typeof oldState[e.target.name as keyof T] === 'object') {
    newState = {
      ...oldState,
      [e.target.name]: {
        ...(oldState[e.target.name as keyof T] as InputType),
        value: parseFloat(e.target.value),
      },
    };
  } else if (e.target.type === 'checkbox') {
    newState = { ...oldState, [e.target.name]: e.target.checked };
  } else {
    newState = { ...oldState, [e.target.name]: e.target.value };
  }
  return newState;
};

function setSubstrateConditions(
  newState: BiogasParameters,
  value: boolean = false
): BiogasParameters {
  newState.inputElementalAnalysisCarbonContent.disabled = value;
  newState.inputElementalAnalysisHydrogenContent.disabled = value;
  newState.inputElementalAnalysisOxygenContent.disabled = value;
  newState.inputElementalAnalysisNitrogenContent.disabled = value;
  newState.inputElementalAnalysisSulfurContent.disabled = value;
  newState.inputProximateAnalysisTotalSolids.disabled = value;
  newState.inputProximateAnalysisVolatileSolids.disabled = value;
  newState.inputProximateAnalysisDensity.disabled = value;

  return newState;
}
