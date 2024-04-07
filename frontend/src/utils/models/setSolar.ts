import { SolarWindParameters } from '../../types/models/solar';

export const setSolar = (
  e: any,
  oldState: SolarWindParameters
): SolarWindParameters => {
  let newState = { ...oldState };
  if (e.target.name === 'controller.customize') {
    newState.controller.customize = e.target.checked;
    newState.controller.chargeVoltageBulk.disabled = !e.target.checked;
    newState.controller.chargeVoltageFloat.disabled = !e.target.checked;
    newState.controller.chargingMinimunVoltage.disabled = !e.target.checked;
  }
  return newState;
};
