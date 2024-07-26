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

    if (newState.inputOfflineOperation && !newState.digitalTwinState)
      newState.queryTime = Config.QUERY_TIME_DIGITAL_TWIN_OFF_OFFLINE_BIOGAS;

    if (newState.inputOfflineOperation && newState.digitalTwinState)
      newState.queryTime = Config.QUERY_TIME_DIGITAL_TWIN_ON_OFFLINE_BIOGAS;

    if (!newState.inputOfflineOperation && !newState.digitalTwinState)
      newState.queryTime = Config.QUERY_TIME_DIGITAL_TWIN_OFF_ONLINE_BIOGAS;

    if (!newState.inputOfflineOperation && newState.digitalTwinState)
      newState.queryTime = Config.QUERY_TIME_DIGITAL_TWIN_ON_ONLINE_BIOGAS;

    newState.queryTime = newState.inputOfflineOperation
      ? Config.QUERY_TIME_DIGITAL_TWIN_ON_OFFLINE_BIOGAS
      : Config.QUERY_TIME_DIGITAL_TWIN_ON_ONLINE_BIOGAS;
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
    newState.digitalTwinState = !newState.digitalTwinState;
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

  if (e.target.name === 'initialAnalysisConditions101.enabled') {
    newState.initialAnalysisConditionsR101.enabled = e.target.checked;
    newState.initialAnalysisConditionsR101.totalSubstrateSolids = {
      ...newState.initialAnalysisConditionsR101.totalSubstrateSolids,
      disabled: !e.target.checked,
    };
    newState.initialAnalysisConditionsR101.volatileSubstrateSolids = {
      ...newState.initialAnalysisConditionsR101.volatileSubstrateSolids,
      disabled: !e.target.checked,
    };
    newState.initialAnalysisConditionsR101.substrateDensity = {
      ...newState.initialAnalysisConditionsR101.substrateDensity,
      disabled: !e.target.checked,
    };
    newState.initialAnalysisConditionsR101.atomicCarbonSubstrateConcetration = {
      ...newState.initialAnalysisConditionsR101
        .atomicCarbonSubstrateConcetration,
      disabled: !e.target.checked,
    };
    newState.initialAnalysisConditionsR101.atomicHydrogenSubstrateConcetration =
      {
        ...newState.initialAnalysisConditionsR101
          .atomicHydrogenSubstrateConcetration,
        disabled: !e.target.checked,
      };
    newState.initialAnalysisConditionsR101.atomicOxygenSubstrateConcetration = {
      ...newState.initialAnalysisConditionsR101
        .atomicOxygenSubstrateConcetration,
      disabled: !e.target.checked,
    };
    newState.initialAnalysisConditionsR101.atomicNitrogenSubstrateConcetration =
      {
        ...newState.initialAnalysisConditionsR101
          .atomicNitrogenSubstrateConcetration,
        disabled: !e.target.checked,
      };
    newState.initialAnalysisConditionsR101.atomicSulfurSubstrateConcetration = {
      ...newState.initialAnalysisConditionsR101
        .atomicSulfurSubstrateConcetration,
      disabled: !e.target.checked,
    };
  }
  if (e.target.name === 'initialAnalysisConditions102.enabled') {
    newState.initialAnalysisConditionsR102.enabled = e.target.checked;
    newState.initialAnalysisConditionsR102.totalSubstrateSolids = {
      ...newState.initialAnalysisConditionsR102.totalSubstrateSolids,
      disabled: !e.target.checked,
    };
    newState.initialAnalysisConditionsR102.volatileSubstrateSolids = {
      ...newState.initialAnalysisConditionsR102.volatileSubstrateSolids,
      disabled: !e.target.checked,
    };
    newState.initialAnalysisConditionsR102.substrateDensity = {
      ...newState.initialAnalysisConditionsR102.substrateDensity,
      disabled: !e.target.checked,
    };
    newState.initialAnalysisConditionsR102.atomicCarbonSubstrateConcetration = {
      ...newState.initialAnalysisConditionsR102
        .atomicCarbonSubstrateConcetration,
      disabled: !e.target.checked,
    };
    newState.initialAnalysisConditionsR102.atomicHydrogenSubstrateConcetration =
      {
        ...newState.initialAnalysisConditionsR102
          .atomicHydrogenSubstrateConcetration,
        disabled: !e.target.checked,
      };
    newState.initialAnalysisConditionsR102.atomicOxygenSubstrateConcetration = {
      ...newState.initialAnalysisConditionsR102
        .atomicOxygenSubstrateConcetration,
      disabled: !e.target.checked,
    };
    newState.initialAnalysisConditionsR102.atomicNitrogenSubstrateConcetration =
      {
        ...newState.initialAnalysisConditionsR102
          .atomicNitrogenSubstrateConcetration,
        disabled: !e.target.checked,
      };
    newState.initialAnalysisConditionsR102.atomicSulfurSubstrateConcetration = {
      ...newState.initialAnalysisConditionsR102
        .atomicSulfurSubstrateConcetration,
      disabled: !e.target.checked,
    };
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
