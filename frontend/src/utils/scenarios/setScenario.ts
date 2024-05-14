import { InputType } from '../../types/inputType';
import { COMMON_SOLAR_PANEL } from '../../types/scenarios/common';
import { SmartCityParameters } from '../../types/scenarios/smartCity';
import { SmartFactoryParameters } from '../../types/scenarios/smartFactory';
import { SmartHomeParameters } from '../../types/scenarios/smartHome';
import { v4 as uuidv4 } from 'uuid';

export const setScenario = (
  e: any,
  oldState: SmartCityParameters | SmartFactoryParameters | SmartHomeParameters
): SmartCityParameters | SmartFactoryParameters | SmartHomeParameters => {
  let newState = { ...oldState };
  const name: string = e.target.name;
  const value: number = parseFloat(e.target.value);

  if (name === 'steps') {
    console.log('in');
    if (value > newState.steps.value) {
      newState.solarPanels.forEach((sP) => {
        sP.radiationArray.push(0);
        sP.temperatureArray.push(0);
      });
    } else if (value < newState.steps.value) {
      newState.solarPanels.forEach((sP) => {
        sP.radiationArray.splice(-1);
        sP.temperatureArray.splice(-1);
      });
    }
  }
  if (name.includes('SystemNumber')) {
    if ('solarPanels' in newState && name.includes('solar')) {
      if (value > newState.solarSystemNumber.value) {
        newState.solarPanels = [
          ...newState.solarPanels,
          { ...COMMON_SOLAR_PANEL, id: uuidv4() },
        ];
      } else if (value < newState.solarSystemNumber.value) {
        newState.solarPanels.splice(-1);
      }
    }
    if ('' in newState && name.includes('biogas')) {
    }
    if ('' in newState && name.includes('load')) {
    }
    if ('' in newState && name.includes('battery')) {
    }
    if ('' in newState && name.includes('hydraulic')) {
    }
    if ('' in newState && name.includes('wind')) {
    }
  }
  newState = {
    ...newState,
    [name]: {
      ...(newState[
        name as keyof (
          | SmartCityParameters
          | SmartFactoryParameters
          | SmartHomeParameters
        )
      ] as InputType),
      value: value,
    },
  };
  return newState;
};
