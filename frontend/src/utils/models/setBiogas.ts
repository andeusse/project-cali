import Config from '../../config/config';
import { BiogasParameters, OperationModeType } from '../../types/models/biogas';
import { getKeyByValue } from '../getKeyByValue';

export const setBiogas = (
  e: any,
  oldState: BiogasParameters
): BiogasParameters => {
  let newState = { ...oldState };

  if (e.target.name === 'inputOfflineOperation') {
    newState.inputOfflineOperation = !newState.inputOfflineOperation;
    newState.queryTime = newState.inputOfflineOperation
      ? Config.QUERY_TIME_OFFLINE
      : Config.QUERY_TIME_ONLINE;
    newState.inputSubstrateConditions = newState.inputOfflineOperation;

    (newState as BiogasParameters) = setSubstrateConditions(
      newState,
      !newState.inputOfflineOperation
    );

    newState.timeMultiplier.disabled = !newState.inputOfflineOperation;
    if (!newState.inputOfflineOperation) {
      newState.timeMultiplier.value = 1;
    }
  }

  if (e.target.name === 'inputDigitalTwin') {
    newState.inputDigitalTwin = !newState.inputDigitalTwin;

    newState.inputDigitalTwinTrainingTime.disabled = !newState.inputDigitalTwin;
    newState.inputKineticParameterInitialValue.disabled =
      !newState.inputDigitalTwin;

    newState.inputSpeedLawExponentialFactor.disabled =
      newState.inputDigitalTwin;
    newState.inputSpeedLawStartEnergy.disabled = newState.inputDigitalTwin;
  }

  if (e.target.name === 'inputSubstrateConditions') {
    newState.inputSubstrateConditions = !newState.inputSubstrateConditions;
    (newState as BiogasParameters) = setSubstrateConditions(
      newState,
      !newState.inputSubstrateConditions
    );
  }

  if (e.target.name === 'inputPump104') {
    newState.inputPump104 = !newState.inputPump104;
    newState.inputPump104HydraulicRetentionTime.disabled =
      !newState.inputPump104;
    newState.inputPump104StartTime.disabled = !newState.inputPump104;
    newState.inputPump104StartsPerDay.disabled = !newState.inputPump104;
  }

  if (e.target.name === 'inputPump102') {
    newState.inputPump102 = !newState.inputPump102;
    newState.inputPump102Flow.disabled = !newState.inputPump102;
    newState.inputPump102StartTime.disabled = !newState.inputPump102;
    newState.inputPump102StartsPerDay.disabled = !newState.inputPump102;
  }

  if (e.target.name === 'inputPump101') {
    newState.inputPump101 = !newState.inputPump101;
    newState.inputPump101Flow.disabled = !newState.inputPump101;
    newState.inputPump101StartTime.disabled = !newState.inputPump101;
    newState.inputPump101StartsPerDay.disabled = !newState.inputPump101;
  }

  if (e.target.name === 'inputOperationMode') {
    newState.inputOperationMode = getKeyByValue(
      OperationModeType,
      e.target.value
    );
    if (
      newState.inputOperationMode === OperationModeType.Modo3 ||
      newState.inputOperationMode === OperationModeType.Modo4
    ) {
      newState.inputPump101Flow.disabled = true;
      newState.inputPump101StartTime.disabled = true;
      newState.inputPump101StartsPerDay.disabled = true;
    } else {
      newState.inputPump101Flow.disabled = false;
      newState.inputPump101StartTime.disabled = false;
      newState.inputPump101StartsPerDay.disabled = false;
    }
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
