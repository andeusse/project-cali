import { OperationModelType } from '../../types/common';
import {
  BiochemicalMethanePotentialParameters,
  MixRuleType,
} from '../../types/models/biochemicalMethanePotential';
import { getKeyByValue } from '../getKeyByValue';

export const setBiochemicalMethanePotential = (
  e: any,
  oldState: BiochemicalMethanePotentialParameters
): BiochemicalMethanePotentialParameters => {
  let newState = { ...oldState };
  if (e.target.name === 'stateSelectionSideA') {
    newState.stateSelectionSideA = !newState.stateSelectionSideA;

    newState.testDurationSideA.disabled = !newState.stateSelectionSideA;
    newState.TemperatureSideA.disabled = !newState.stateSelectionSideA;
    newState.pHSideA.disabled = !newState.stateSelectionSideA;
    newState.mixManualSideA = newState.stateSelectionSideA;
    newState.feefManualSideA = newState.stateSelectionSideA;
    newState.manualBiogasCompositionSideA = newState.stateSelectionSideA;
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
        newState.kineticKSideA.unit = '[L / s]';
        newState.kineticKSideA.variableString = 'K';

        newState.kineticEaSideA.disabled = false;
        newState.kineticEaSideA.value = 1000000;
        newState.kineticEaSideA.unit = '[J / mol]';
        newState.kineticEaSideA.variableString = 'Ea';

        newState.kineticLambdaSideA.disabled = true;
        break;
      case OperationModelType.ADM1:
        newState.kineticKSideA.disabled = false;
        newState.kineticKSideA.value = 1e-10;
        newState.kineticKSideA.unit = '[L / s]';
        newState.kineticKSideA.variableString = 'K';

        newState.kineticEaSideA.disabled = true;
        newState.kineticLambdaSideA.disabled = true;
        break;
      case OperationModelType.Gompertz:
        newState.kineticKSideA.disabled = false;
        newState.kineticKSideA.value = 0.00329;
        newState.kineticKSideA.unit = '[L / gSV]';
        newState.kineticKSideA.variableString = 'ym';

        newState.kineticEaSideA.disabled = false;
        newState.kineticEaSideA.value = 2.59e-9;
        newState.kineticEaSideA.unit = '[L / gSV.s]';
        newState.kineticEaSideA.variableString = 'U';

        newState.kineticLambdaSideA.disabled = false;
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
  if (e.target.name === 'stateSelectionSideB') {
    newState.stateSelectionSideB = !newState.stateSelectionSideB;

    newState.testDurationSideB.disabled = !newState.stateSelectionSideB;
    newState.TemperatureSideB.disabled = !newState.stateSelectionSideB;
    newState.pHSideB.disabled = !newState.stateSelectionSideB;
    newState.mixManualSideB = newState.stateSelectionSideB;
    newState.feefManualSideB = newState.stateSelectionSideB;
    newState.manualBiogasCompositionSideB = newState.stateSelectionSideB;
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
        newState.kineticKSideB.unit = '[L / s]';
        newState.kineticKSideB.variableString = 'K';

        newState.kineticEaSideB.disabled = false;
        newState.kineticEaSideB.value = 1000000;
        newState.kineticEaSideB.unit = '[J / mol]';
        newState.kineticEaSideB.variableString = 'Ea';

        newState.kineticLambdaSideB.disabled = true;
        break;
      case OperationModelType.ADM1:
        newState.kineticKSideB.disabled = false;
        newState.kineticKSideB.value = 1e-10;
        newState.kineticKSideB.unit = '[L / s]';
        newState.kineticKSideB.variableString = 'K';

        newState.kineticEaSideB.disabled = true;
        newState.kineticLambdaSideB.disabled = true;
        break;
      case OperationModelType.Gompertz:
        newState.kineticKSideB.disabled = false;
        newState.kineticKSideB.value = 0.00329;
        newState.kineticKSideB.unit = '[L / gSV]';
        newState.kineticKSideB.variableString = 'ym';

        newState.kineticEaSideB.disabled = false;
        newState.kineticEaSideB.value = 2.59e-9;
        newState.kineticEaSideB.unit = '[L / gSV.s]';
        newState.kineticEaSideB.variableString = 'U';

        newState.kineticLambdaSideB.disabled = false;
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

  return newState;
};
