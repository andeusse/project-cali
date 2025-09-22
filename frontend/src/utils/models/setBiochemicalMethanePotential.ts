import Constants from '../../config/constants';
import { OperationModelType, StepUnitType } from '../../types/common';
import {
  BiochemicalMethanePotentialParameters,
  MixRuleType,
  PlantOperationType,
} from '../../types/models/biochemicalMethanePotential';
import { getKeyByValue } from '../getKeyByValue';

export const setBiochemicalMethanePotential = (
  e: any,
  oldState: BiochemicalMethanePotentialParameters
): BiochemicalMethanePotentialParameters => {
  let newState = { ...oldState };
  if (e.target.name === 'stateSelection') {
    newState.stateSelection = !newState.stateSelection;

    newState.queryTime = newState.stateSelection
      ? Constants.QUERY_TIME_OFFLINE_BMP
      : Constants.QUERY_TIME_ONLINE_BMP;

    newState.testDurationSideA.disabled = !newState.stateSelection;
    newState.TemperatureSideA.disabled = !newState.stateSelection;
    newState.pHSideA.disabled = !newState.stateSelection;
    newState.mixManualSideA = newState.stateSelection;
    newState.feefManualSideA = newState.stateSelection;
    newState.manualBiogasCompositionSideA = newState.stateSelection;

    newState.testDurationSideB.disabled = !newState.stateSelection;
    newState.TemperatureSideB.disabled = !newState.stateSelection;
    newState.pHSideB.disabled = !newState.stateSelection;
    newState.mixManualSideB = newState.stateSelection;
    newState.feefManualSideB = newState.stateSelection;
    newState.manualBiogasCompositionSideB = newState.stateSelection;
  }
  if (e.target.name === 'modelSelectionSideA') {
    newState.modelSelectionSideA = getKeyByValue(
      OperationModelType,
      e.target.value
    );
    switch (newState.modelSelectionSideA) {
      case OperationModelType.Arrhenius:
        newState.kineticKSideA.disabled = false;
        newState.kineticKSideA.value = 100;
        newState.kineticKSideA.unit = '[L/s]';
        newState.kineticKSideA.variableString = 'K';
        newState.kineticKSideA.tooltip = 'Factor preexponencial para lado A';

        newState.kineticEaSideA.disabled = false;
        newState.kineticEaSideA.value = 1000000;
        newState.kineticEaSideA.unit = '[J/mol]';
        newState.kineticEaSideA.variableString = 'Ea';
        newState.kineticEaSideA.tooltip = 'Energía de activación para lado A';

        newState.kineticLambdaSideA.disabled = true;
        newState.kineticLambdaSideA.tooltip = '';
        break;
      case OperationModelType.ADM1:
        newState.kineticKSideA.disabled = false;
        newState.kineticKSideA.value = 1e-10;
        newState.kineticKSideA.unit = '[L/s]';
        newState.kineticKSideA.variableString = 'K';
        newState.kineticKSideA.tooltip = 'Parámetro cinético para lado A';

        newState.kineticEaSideA.disabled = true;
        newState.kineticEaSideA.tooltip = '';

        newState.kineticLambdaSideA.disabled = true;
        newState.kineticLambdaSideA.tooltip = '';
        break;
      case OperationModelType.Gompertz:
        newState.kineticKSideA.disabled = false;
        newState.kineticKSideA.value = 0.00329;
        newState.kineticKSideA.unit = '[mL/gSV]';
        newState.kineticKSideA.variableString = 'ym';
        newState.kineticKSideA.tooltip =
          'Potencial de producción de biogás para lado A';

        newState.kineticEaSideA.disabled = false;
        newState.kineticEaSideA.value = 2.59e-9;
        newState.kineticEaSideA.unit = '[mL/gSV dia]';
        newState.kineticEaSideA.variableString = 'U';
        newState.kineticEaSideA.tooltip =
          'Tasa máxima de producción de biogás para lado A';

        newState.kineticLambdaSideA.disabled = false;
        newState.kineticLambdaSideA.unit = 'dia';
        newState.kineticLambdaSideA.tooltip =
          'Tiempo mínimo de producción de biogás para lado A';
        break;
    }
  }
  if (e.target.name === 'mixRuleSideA') {
    newState.mixRuleSideA = getKeyByValue(MixRuleType, e.target.value);
    switch (newState.mixRuleSideA) {
      case MixRuleType.Fraction:
        newState.substrate1CompositionSideA.variableString = 'Fracción';
        newState.substrate1CompositionSideA.unit = '%';

        newState.substrate2CompositionSideA.variableString = 'Fracción';
        newState.substrate2CompositionSideA.unit = '%';

        newState.substrate3CompositionSideA.variableString = 'Fracción';
        newState.substrate3CompositionSideA.unit = '%';

        newState.substrate4CompositionSideA.variableString = 'Fracción';
        newState.substrate4CompositionSideA.unit = '%';

        newState.waterCompositionSideA.variableString = 'Fracción de agua';
        newState.waterCompositionSideA.unit = '%';
        break;
      case MixRuleType.Volume:
        newState.substrate1CompositionSideA.variableString = 'Volumen';
        newState.substrate1CompositionSideA.unit = 'mL';

        newState.substrate2CompositionSideA.variableString = 'Volumen';
        newState.substrate2CompositionSideA.unit = 'mL';

        newState.substrate3CompositionSideA.variableString = 'Volumen';
        newState.substrate3CompositionSideA.unit = 'mL';

        newState.substrate4CompositionSideA.variableString = 'Volumen';
        newState.substrate4CompositionSideA.unit = 'mL';

        newState.waterCompositionSideA.variableString = 'Volumen de agua';
        newState.waterCompositionSideA.unit = 'mL';
        break;
      case MixRuleType.Weight:
        newState.substrate1CompositionSideA.variableString = 'Peso';
        newState.substrate1CompositionSideA.unit = 'g';

        newState.substrate2CompositionSideA.variableString = 'Peso';
        newState.substrate2CompositionSideA.unit = 'g';

        newState.substrate3CompositionSideA.variableString = 'Peso';
        newState.substrate3CompositionSideA.unit = 'g';

        newState.substrate4CompositionSideA.variableString = 'Peso';
        newState.substrate4CompositionSideA.unit = 'g';

        newState.waterCompositionSideA.variableString = 'Peso de agua';
        newState.waterCompositionSideA.unit = 'g';
        break;
    }
  }
  if (e.target.name === 'modelSelectionSideB') {
    newState.modelSelectionSideB = getKeyByValue(
      OperationModelType,
      e.target.value
    );
    switch (newState.modelSelectionSideB) {
      case OperationModelType.Arrhenius:
        newState.kineticKSideB.disabled = false;
        newState.kineticKSideB.value = 100;
        newState.kineticKSideB.unit = '[L/s]';
        newState.kineticKSideB.variableString = 'K';
        newState.kineticKSideB.tooltip = 'Factor preexponencial para lado B';

        newState.kineticEaSideB.disabled = false;
        newState.kineticEaSideB.value = 1000000;
        newState.kineticEaSideB.unit = '[J/mol]';
        newState.kineticEaSideB.variableString = 'Ea';
        newState.kineticEaSideB.tooltip = 'Energía de activación para lado B';

        newState.kineticLambdaSideB.disabled = true;
        newState.kineticLambdaSideB.tooltip = '';
        break;
      case OperationModelType.ADM1:
        newState.kineticKSideB.disabled = false;
        newState.kineticKSideB.value = 1e-10;
        newState.kineticKSideB.unit = '[L/s]';
        newState.kineticKSideB.variableString = 'K';
        newState.kineticKSideB.tooltip = 'Parámetro cinético para lado B';

        newState.kineticEaSideB.disabled = true;
        newState.kineticEaSideB.tooltip = '';

        newState.kineticLambdaSideB.disabled = true;
        newState.kineticLambdaSideB.tooltip = '';
        break;
      case OperationModelType.Gompertz:
        newState.kineticKSideB.disabled = false;
        newState.kineticKSideB.value = 0.00329;
        newState.kineticKSideB.unit = '[L/gSV]';
        newState.kineticKSideB.variableString = 'ym';
        newState.kineticKSideB.tooltip =
          'Potencial de producción de biogás para lado B';

        newState.kineticEaSideB.disabled = false;
        newState.kineticEaSideB.value = 2.59e-9;
        newState.kineticEaSideB.unit = '[L/gSV.s]';
        newState.kineticEaSideB.variableString = 'U';
        newState.kineticEaSideB.tooltip =
          'Tasa máxima de producción de biogás para lado B';

        newState.kineticLambdaSideB.disabled = false;
        newState.kineticLambdaSideB.unit = 's';
        newState.kineticLambdaSideB.tooltip =
          'Tiempo mínimo de producción de biogás para lado B';
        break;
    }
  }
  if (e.target.name === 'mixRuleSideB') {
    newState.mixRuleSideB = getKeyByValue(MixRuleType, e.target.value);
    switch (newState.mixRuleSideB) {
      case MixRuleType.Fraction:
        newState.substrate1CompositionSideB.variableString = 'Fracción';
        newState.substrate1CompositionSideB.unit = '%';

        newState.substrate2CompositionSideB.variableString = 'Fracción';
        newState.substrate2CompositionSideB.unit = '%';

        newState.substrate3CompositionSideB.variableString = 'Fracción';
        newState.substrate3CompositionSideB.unit = '%';

        newState.substrate4CompositionSideB.variableString = 'Fracción';
        newState.substrate4CompositionSideB.unit = '%';

        newState.waterCompositionSideB.variableString = 'Fracción de agua';
        newState.waterCompositionSideB.unit = '%';
        break;
      case MixRuleType.Volume:
        newState.substrate1CompositionSideB.variableString = 'Volumen';
        newState.substrate1CompositionSideB.unit = 'mL';

        newState.substrate2CompositionSideB.variableString = 'Volumen';
        newState.substrate2CompositionSideB.unit = 'mL';

        newState.substrate3CompositionSideB.variableString = 'Volumen';
        newState.substrate3CompositionSideB.unit = 'mL';

        newState.substrate4CompositionSideB.variableString = 'Volumen';
        newState.substrate4CompositionSideB.unit = 'mL';

        newState.waterCompositionSideB.variableString = 'Volumen de agua';
        newState.waterCompositionSideB.unit = 'mL';
        break;
      case MixRuleType.Weight:
        newState.substrate1CompositionSideB.variableString = 'Peso';
        newState.substrate1CompositionSideB.unit = 'g';

        newState.substrate2CompositionSideB.variableString = 'Peso';
        newState.substrate2CompositionSideB.unit = 'g';

        newState.substrate3CompositionSideB.variableString = 'Peso';
        newState.substrate3CompositionSideB.unit = 'g';

        newState.substrate4CompositionSideB.variableString = 'Peso';
        newState.substrate4CompositionSideB.unit = 'g';

        newState.waterCompositionSideB.variableString = 'Peso de agua';
        newState.waterCompositionSideB.unit = 'g';
        break;
    }
  }
  if (e.target.name === 'trainingMode') {
    newState.trainingMode = e.target.checked;
    newState.stateSelection = !newState.trainingMode;

    newState.testDurationSideA.disabled = !newState.stateSelection;
    newState.TemperatureSideA.disabled = !newState.stateSelection;
    newState.pHSideA.disabled = !newState.stateSelection;
    newState.mixManualSideA = newState.stateSelection;
    newState.feefManualSideA = newState.stateSelection;
    newState.manualBiogasCompositionSideA = newState.stateSelection;

    newState.testDurationSideB.disabled = !newState.stateSelection;
    newState.TemperatureSideB.disabled = !newState.stateSelection;
    newState.pHSideB.disabled = !newState.stateSelection;
    newState.mixManualSideB = newState.stateSelection;
    newState.feefManualSideB = newState.stateSelection;
    newState.manualBiogasCompositionSideB = newState.stateSelection;
  }
  if (e.target.name === 'inputProfileEnable') {
    newState.inputProfileEnable = e.target.checked;
    if (!newState.inputProfileEnable) {
      newState.steps.value = 1;
      newState.stepTime.value = 1;
      newState.stepUnit = StepUnitType.Second;
    }
  }
  if (e.target.name === 'isSideAOn') {
    newState.isSideAOn = e.target.checked;
    if (!newState.isSideAOn && !newState.isSideBOn) {
      newState.isSideBOn = true;
      newState.plantOperation = PlantOperationType.SideB;
    }
    if (!newState.isSideAOn) {
      newState.plantOperation = PlantOperationType.SideB;
    }
  }
  if (e.target.name === 'isSideBOn') {
    newState.isSideBOn = e.target.checked;
    if (!newState.isSideAOn && !newState.isSideBOn) {
      newState.isSideAOn = true;
      newState.plantOperation = PlantOperationType.SideA;
    }
    if (!newState.isSideBOn) {
      newState.plantOperation = PlantOperationType.SideA;
    }
  }

  return newState;
};
