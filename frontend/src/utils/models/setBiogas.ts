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
      ? Config.QUERY_TIME_OFFLINE_BIOGAS
      : Config.QUERY_TIME_ONLINE_BIOGAS;
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

  if (e.target.name === 'initialAnalysisConditions101.enabled') {
    newState.initialAnalysisConditions101.enabled = e.target.checked;
    newState.initialAnalysisConditions101.totalSubstrateSolids = {
      ...newState.initialAnalysisConditions101.totalSubstrateSolids,
      disabled: !e.target.checked,
    };
    newState.initialAnalysisConditions101.volatileSubstrateSolids = {
      ...newState.initialAnalysisConditions101.volatileSubstrateSolids,
      disabled: !e.target.checked,
    };
    newState.initialAnalysisConditions101.substrateDensity = {
      ...newState.initialAnalysisConditions101.substrateDensity,
      disabled: !e.target.checked,
    };
    newState.initialAnalysisConditions101.atomicCarbonSubstrateConcetration = {
      ...newState.initialAnalysisConditions101
        .atomicCarbonSubstrateConcetration,
      disabled: !e.target.checked,
    };
    newState.initialAnalysisConditions101.atomicHydrogenSubstrateConcetration =
      {
        ...newState.initialAnalysisConditions101
          .atomicHydrogenSubstrateConcetration,
        disabled: !e.target.checked,
      };
    newState.initialAnalysisConditions101.atomicOxygenSubstrateConcetration = {
      ...newState.initialAnalysisConditions101
        .atomicOxygenSubstrateConcetration,
      disabled: !e.target.checked,
    };
    newState.initialAnalysisConditions101.atomicNitrogenSubstrateConcetration =
      {
        ...newState.initialAnalysisConditions101
          .atomicNitrogenSubstrateConcetration,
        disabled: !e.target.checked,
      };
    newState.initialAnalysisConditions101.atomicSulfurSubstrateConcetration = {
      ...newState.initialAnalysisConditions101
        .atomicSulfurSubstrateConcetration,
      disabled: !e.target.checked,
    };
  }
  if (e.target.name === 'initialAnalysisConditions102.enabled') {
    newState.initialAnalysisConditions102.enabled = e.target.checked;
    newState.initialAnalysisConditions102.totalSubstrateSolids = {
      ...newState.initialAnalysisConditions102.totalSubstrateSolids,
      disabled: !e.target.checked,
    };
    newState.initialAnalysisConditions102.volatileSubstrateSolids = {
      ...newState.initialAnalysisConditions102.volatileSubstrateSolids,
      disabled: !e.target.checked,
    };
    newState.initialAnalysisConditions102.substrateDensity = {
      ...newState.initialAnalysisConditions102.substrateDensity,
      disabled: !e.target.checked,
    };
    newState.initialAnalysisConditions102.atomicCarbonSubstrateConcetration = {
      ...newState.initialAnalysisConditions102
        .atomicCarbonSubstrateConcetration,
      disabled: !e.target.checked,
    };
    newState.initialAnalysisConditions102.atomicHydrogenSubstrateConcetration =
      {
        ...newState.initialAnalysisConditions102
          .atomicHydrogenSubstrateConcetration,
        disabled: !e.target.checked,
      };
    newState.initialAnalysisConditions102.atomicOxygenSubstrateConcetration = {
      ...newState.initialAnalysisConditions102
        .atomicOxygenSubstrateConcetration,
      disabled: !e.target.checked,
    };
    newState.initialAnalysisConditions102.atomicNitrogenSubstrateConcetration =
      {
        ...newState.initialAnalysisConditions102
          .atomicNitrogenSubstrateConcetration,
        disabled: !e.target.checked,
      };
    newState.initialAnalysisConditions102.atomicSulfurSubstrateConcetration = {
      ...newState.initialAnalysisConditions102
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
