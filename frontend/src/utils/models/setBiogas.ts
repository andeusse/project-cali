import Config from '../../config/config';
import { OperationModelType } from '../../types/common';
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

    newState.inputMixTK100 = newState.inputOfflineOperation;
    newState.inputSpeedMixTK100.disabled = !newState.inputOfflineOperation;
    newState.inputStartsPerDayMixTK100.disabled =
      !newState.inputOfflineOperation;
    newState.inputStartTimeMixTK100.disabled = !newState.inputOfflineOperation;

    newState.inputPump104 = newState.inputOfflineOperation;
    newState.inputPump104HydraulicRetentionTime.disabled =
      !newState.inputOfflineOperation;
    newState.inputPump104StartsPerDay.disabled =
      !newState.inputOfflineOperation;
    newState.inputPump104StartTime.disabled = !newState.inputOfflineOperation;

    newState.inputPump101 = newState.inputOfflineOperation;
    newState.inputPump101Flow.disabled = !newState.inputOfflineOperation;
    newState.inputPump101StartsPerDay.disabled =
      !newState.inputOfflineOperation;
    newState.inputPump101StartTime.disabled = !newState.inputOfflineOperation;

    newState.inputPump102 = newState.inputOfflineOperation;
    newState.inputPump102Flow.disabled = !newState.inputOfflineOperation;
    newState.inputPump102StartsPerDay.disabled =
      !newState.inputOfflineOperation;
    newState.inputPump102StartTime.disabled = !newState.inputOfflineOperation;

    newState.inputMixR101 = newState.inputOfflineOperation;
    newState.inputSpeedMixR101.disabled = !newState.inputOfflineOperation;
    newState.inputStartsPerDayMixR101.disabled =
      !newState.inputOfflineOperation;
    newState.inputStartTimeMixR101.disabled = !newState.inputOfflineOperation;
    newState.inputPHR101.disabled = !newState.inputOfflineOperation;
    newState.inputTemperatureR101.disabled = !newState.inputOfflineOperation;

    newState.inputMixR102 = newState.inputOfflineOperation;
    newState.inputSpeedMixR102.disabled = !newState.inputOfflineOperation;
    newState.inputStartsPerDayMixR102.disabled =
      !newState.inputOfflineOperation;
    newState.inputStartTimeMixR102.disabled = !newState.inputOfflineOperation;
    newState.inputPHR102.disabled = !newState.inputOfflineOperation;
    newState.inputTemperatureR102.disabled = !newState.inputOfflineOperation;

    newState.timeMultiplier.disabled = !newState.inputOfflineOperation;
    if (!newState.inputOfflineOperation) {
      newState.timeMultiplier.value = 1;
    }
  }

  if (e.target.name === 'digitalTwinState') {
    newState.digitalTwinState = !newState.digitalTwinState;
    newState.digitalTwinStepTime.disabled = newState.digitalTwinState;
    newState.digitalTwinForecastTime.disabled = !newState.digitalTwinState;

    newState.inputOfflineOperation = true;

    switch (newState.operationModelType) {
      case OperationModelType.Arrhenius:
        newState.exponentialFactorR101.variableString = 'K R101';
        newState.exponentialFactorR101.unit = '[L / s]';
        newState.exponentialFactorR101.value = 100;
        newState.exponentialFactorR101.disabled = newState.digitalTwinState;

        newState.activationEnergyR101.variableString = 'Ea R101';
        newState.activationEnergyR101.unit = '[J / mol]';
        newState.activationEnergyR101.value = 1000000;
        newState.activationEnergyR101.disabled = newState.digitalTwinState
          ? true
          : false;

        newState.lambdaR101.disabled = true;

        newState.exponentialFactorR102.variableString = 'K R101';
        newState.exponentialFactorR102.unit = '[L / s]';
        newState.exponentialFactorR102.value = 100;
        newState.exponentialFactorR102.disabled = newState.digitalTwinState;

        newState.activationEnergyR102.variableString = 'Ea R101';
        newState.activationEnergyR102.unit = '[J / mol]';
        newState.activationEnergyR102.value = 1000000;
        newState.activationEnergyR102.disabled = newState.digitalTwinState
          ? true
          : false;

        newState.lambdaR102.disabled = true;
        break;
      case OperationModelType.ADM1:
        newState.exponentialFactorR101.variableString = 'K R101';
        newState.exponentialFactorR101.unit = '[L / s]';
        newState.exponentialFactorR101.value = 1e-15;
        newState.exponentialFactorR101.disabled = newState.digitalTwinState;

        newState.activationEnergyR101.disabled = true;

        newState.lambdaR101.disabled = true;

        newState.exponentialFactorR102.variableString = 'K R101';
        newState.exponentialFactorR102.unit = '[L / s]';
        newState.exponentialFactorR102.value = 1e-15;
        newState.exponentialFactorR102.disabled = newState.digitalTwinState;

        newState.activationEnergyR102.disabled = true;

        newState.lambdaR102.disabled = true;
        break;
      case OperationModelType.Gompertz:
        newState.exponentialFactorR101.variableString = 'ym R101';
        newState.exponentialFactorR101.unit = '[L / s SV]';
        newState.exponentialFactorR101.value = 0.00329;
        newState.exponentialFactorR101.disabled = newState.digitalTwinState;

        newState.activationEnergyR101.variableString = 'U R101';
        newState.activationEnergyR101.unit = '[L / g SVs]';
        newState.activationEnergyR101.value = 2.59e-9;
        newState.activationEnergyR101.disabled = newState.digitalTwinState
          ? true
          : false;

        newState.lambdaR101.disabled = newState.digitalTwinState ? true : false;

        newState.exponentialFactorR102.variableString = 'ym R101';
        newState.exponentialFactorR102.unit = '[L / s SV]';
        newState.exponentialFactorR102.value = 0.00329;
        newState.exponentialFactorR102.disabled = newState.digitalTwinState;

        newState.activationEnergyR102.variableString = 'U R101';
        newState.activationEnergyR102.unit = '[L / g SVs]';
        newState.activationEnergyR102.value = 2.59e-9;
        newState.activationEnergyR102.disabled = newState.digitalTwinState
          ? true
          : false;

        newState.lambdaR102.disabled = newState.digitalTwinState ? true : false;
        break;
      default:
        newState.exponentialFactorR101.variableString = 'K R101';
        newState.exponentialFactorR101.unit = '[L / s]';
        newState.exponentialFactorR101.value = 100;
        newState.exponentialFactorR101.disabled = newState.digitalTwinState;

        newState.activationEnergyR101.variableString = 'Ea R101';
        newState.activationEnergyR101.unit = '[J / mol]';
        newState.activationEnergyR101.value = 1000000;
        newState.activationEnergyR101.disabled = newState.digitalTwinState
          ? true
          : false;

        newState.lambdaR101.disabled = true;

        newState.exponentialFactorR102.variableString = 'K R101';
        newState.exponentialFactorR102.unit = '[L / s]';
        newState.exponentialFactorR102.value = 100;
        newState.exponentialFactorR102.disabled = newState.digitalTwinState;

        newState.activationEnergyR102.variableString = 'Ea R101';
        newState.activationEnergyR102.unit = '[J / mol]';
        newState.activationEnergyR102.value = 1000000;
        newState.activationEnergyR102.disabled = newState.digitalTwinState
          ? true
          : false;

        newState.lambdaR102.disabled = true;
        break;
    }

    newState.difussionCoefficientTower1.disabled = newState.digitalTwinState;
    newState.adsorbentWeightTower1.disabled = newState.digitalTwinState;
    newState.lengthTower1.disabled = newState.digitalTwinState;
    newState.difussionCoefficientTower2.disabled = newState.digitalTwinState;
    newState.adsorbentWeightTower2.disabled = newState.digitalTwinState;
    newState.lengthTower2.disabled = newState.digitalTwinState;
    newState.difussionCoefficientTower3.disabled = newState.digitalTwinState;
    newState.adsorbentWeightTower3.disabled = newState.digitalTwinState;
    newState.lengthTower3.disabled = newState.digitalTwinState;
  }

  if (e.target.name === 'operationModelType') {
    newState.operationModelType = getKeyByValue(
      OperationModelType,
      e.target.value
    );
    switch (newState.operationModelType) {
      case OperationModelType.Arrhenius:
        newState.exponentialFactorR101.variableString = 'K R101';
        newState.exponentialFactorR101.unit = '[L / s]';
        newState.exponentialFactorR101.value = 100;

        newState.activationEnergyR101.variableString = 'Ea R101';
        newState.activationEnergyR101.unit = '[J / mol]';
        newState.activationEnergyR101.value = 1000000;
        newState.activationEnergyR101.disabled = newState.digitalTwinState
          ? true
          : false;

        newState.lambdaR101.disabled = true;

        newState.exponentialFactorR102.variableString = 'K R102';
        newState.exponentialFactorR102.unit = '[L / s]';
        newState.exponentialFactorR102.value = 100;

        newState.activationEnergyR102.variableString = 'Ea R102';
        newState.activationEnergyR102.unit = '[J / mol]';
        newState.activationEnergyR102.value = 1000000;
        newState.activationEnergyR102.disabled = newState.digitalTwinState
          ? true
          : false;

        newState.lambdaR102.disabled = true;
        break;
      case OperationModelType.ADM1:
        newState.exponentialFactorR101.variableString = 'K R101';
        newState.exponentialFactorR101.unit = '[L / s]';
        newState.exponentialFactorR101.value = 1e-15;

        newState.activationEnergyR101.disabled = true;

        newState.lambdaR101.disabled = true;

        newState.exponentialFactorR102.variableString = 'K R102';
        newState.exponentialFactorR102.unit = '[L / s]';
        newState.exponentialFactorR102.value = 1e-15;

        newState.activationEnergyR102.disabled = true;

        newState.lambdaR102.disabled = true;
        break;
      case OperationModelType.Gompertz:
        newState.exponentialFactorR101.variableString = 'ym R101';
        newState.exponentialFactorR101.unit = '[L / s SV]';
        newState.exponentialFactorR101.value = 0.00329;

        newState.activationEnergyR101.variableString = 'U R101';
        newState.activationEnergyR101.unit = '[L / g SVs]';
        newState.activationEnergyR101.value = 2.59e-9;
        newState.activationEnergyR101.disabled = newState.digitalTwinState
          ? true
          : false;

        newState.lambdaR101.disabled = newState.digitalTwinState ? true : false;

        newState.exponentialFactorR102.variableString = 'ym R102';
        newState.exponentialFactorR102.unit = '[L / s SV]';
        newState.exponentialFactorR102.value = 0.00329;

        newState.activationEnergyR102.variableString = 'U R102';
        newState.activationEnergyR102.unit = '[L / g SVs]';
        newState.activationEnergyR102.value = 2.59e-9;
        newState.activationEnergyR102.disabled = newState.digitalTwinState
          ? true
          : false;

        newState.lambdaR102.disabled = newState.digitalTwinState ? true : false;
        break;
      default:
        newState.exponentialFactorR101.variableString = 'K R101';
        newState.exponentialFactorR101.unit = '[L / s]';
        newState.exponentialFactorR101.value = 100;

        newState.activationEnergyR101.variableString = 'Ea R101';
        newState.activationEnergyR101.unit = '[J / mol]';
        newState.activationEnergyR101.value = 1000000;
        newState.activationEnergyR101.disabled = newState.digitalTwinState
          ? true
          : false;

        newState.lambdaR101.disabled = true;

        newState.exponentialFactorR102.variableString = 'K R101';
        newState.exponentialFactorR102.unit = '[L / s]';
        newState.exponentialFactorR102.value = 100;

        newState.activationEnergyR102.variableString = 'Ea R101';
        newState.activationEnergyR102.unit = '[J / mol]';
        newState.activationEnergyR102.value = 1000000;
        newState.activationEnergyR102.disabled = newState.digitalTwinState
          ? true
          : false;

        newState.lambdaR102.disabled = true;
        break;
    }
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

  if (e.target.name === 'inputMixTK100') {
    newState.inputMixTK100 = !newState.inputMixTK100;
    newState.inputSpeedMixTK100.disabled = !newState.inputMixTK100;
    newState.inputStartsPerDayMixTK100.disabled = !newState.inputMixTK100;
    newState.inputStartTimeMixTK100.disabled = !newState.inputMixTK100;
  }

  if (e.target.name === 'inputMixR101') {
    newState.inputMixR101 = !newState.inputMixR101;
    newState.inputSpeedMixR101.disabled = !newState.inputMixR101;
    newState.inputStartsPerDayMixR101.disabled = !newState.inputMixR101;
    newState.inputStartTimeMixR101.disabled = !newState.inputMixR101;
  }

  if (e.target.name === 'inputMixR102') {
    newState.inputMixR102 = !newState.inputMixR102;
    newState.inputSpeedMixR102.disabled = !newState.inputMixR102;
    newState.inputStartsPerDayMixR102.disabled = !newState.inputMixR102;
    newState.inputStartTimeMixR102.disabled = !newState.inputMixR102;
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
