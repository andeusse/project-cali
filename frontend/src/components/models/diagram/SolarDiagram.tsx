import React, { useEffect, useState } from 'react';
import {
  OperationModeType,
  SOLAR_DIAGRAM_VARIABLES,
  SOLAR_WIND_DIAGRAM_VARIABLES,
  SolarWindOutput,
  SolarWindParameters,
} from '../../../types/models/solar';
import DiagramVariables from '../common/DiagramVariables';

import solarWindDiagram from '../../../assets/solar/solarWindDiagram.png';
import solarDiagram from '../../../assets/solar/solarDiagram.png';

import fanOff from '../../../assets/solar/fanOff.png';
import fanOn from '../../../assets/solar/fan.gif';
import turbineOff from '../../../assets/solar/turbineOff.png';
import turbineOn from '../../../assets/solar/turbine.gif';

import cargaACOff from '../../../assets/common/cargaACOff.png';
import cargaACOn from '../../../assets/common/cargaACOn.png';
import cargaDCOff from '../../../assets/common/cargaDCOff.png';
import cargaDCOn from '../../../assets/common/cargaDCOn.png';
import lightOff from '../../../assets/common/lightsOff.png';
import lightOn from '../../../assets/common/lightsOn.png';
import BatteryStateOfCharge from '../common/BatteryStateOfCharge';

type Props = {
  solarWind: SolarWindParameters;
  data: SolarWindOutput | undefined;
  isPlaying: boolean;
};

const SolarDiagram = (props: Props) => {
  const { solarWind, data, isPlaying } = props;

  const [batteryStateOfCharge, setBatteryStateOfCharge] = useState(
    data
      ? data.batteryStateOfCharge
      : (solarWind.battery1.stateOfCharge.value +
          (solarWind.isBattery2 ? solarWind.battery2.stateOfCharge.value : 0)) /
          2
  );

  useEffect(() => {
    let newValue = data
      ? data.batteryStateOfCharge
      : (solarWind.battery1.stateOfCharge.value +
          (solarWind.isBattery2 ? solarWind.battery2.stateOfCharge.value : 0)) /
        2;
    if (newValue > 100) {
      newValue = 100;
    } else if (newValue < 0) {
      newValue = 0;
    }
    setBatteryStateOfCharge(newValue);
  }, [
    data,
    solarWind.battery1.stateOfCharge.value,
    solarWind.battery2.stateOfCharge.value,
    solarWind.isBattery2,
  ]);

  return (
    <div
      style={{
        textAlign: 'center',
      }}
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        xmlnsXlink="http://www.w3.org/1999/xlink"
        viewBox={`0 0 4180 2450`}
      >
        {solarWind.inputOperationMode === OperationModeType.Mode2 &&
          solarWind.hybridInverter.isConnected && (
            <g>
              <image href={solarDiagram}></image>
              <DiagramVariables
                data={data}
                variables={SOLAR_DIAGRAM_VARIABLES}
              ></DiagramVariables>
              <image
                href={
                  solarWind.alternCurrentLoadPower.value !== 0
                    ? cargaACOn
                    : cargaACOff
                }
                transform="translate(2950 1100) scale(1 1)"
              ></image>
              <image
                href={
                  solarWind.solarRadiation1.value !== 0 ||
                  solarWind.solarRadiation2.value !== 0
                    ? lightOn
                    : lightOff
                }
                transform="translate(650 350) scale(0.5 0.5)"
              ></image>
              <g transform="translate(3820,1500) scale(0.5,0.5)">
                <BatteryStateOfCharge
                  batteryStateOfCharge={batteryStateOfCharge}
                ></BatteryStateOfCharge>
              </g>
            </g>
          )}
        {!(
          solarWind.inputOperationMode === OperationModeType.Mode2 &&
          solarWind.hybridInverter.isConnected
        ) && (
          <g>
            <image href={solarWindDiagram}></image>
            <DiagramVariables
              data={data}
              variables={SOLAR_WIND_DIAGRAM_VARIABLES}
            ></DiagramVariables>
            <image
              href={
                solarWind.alternCurrentLoadPower.value !== 0
                  ? cargaACOn
                  : cargaACOff
              }
              transform="translate(2850 1500) scale(1 1)"
            ></image>
            <image
              href={
                solarWind.directCurrentLoadPower.value !== 0
                  ? cargaDCOn
                  : cargaDCOff
              }
              transform="translate(1730 1700) scale(0.8 0.8)"
            ></image>
            <image
              href={
                (solarWind.solarRadiation1.value !== 0 ||
                  solarWind.solarRadiation2.value !== 0) &&
                solarWind.inputOperationMode !== OperationModeType.Mode4
                  ? lightOn
                  : lightOff
              }
              transform="translate(350 1400) scale(0.5 0.5)"
            ></image>
            <image
              href={
                solarWind.windSpeed.value !== 0 &&
                (solarWind.inputOperationMode === OperationModeType.Mode4 ||
                  solarWind.inputOperationMode === OperationModeType.Mode5) &&
                isPlaying
                  ? fanOn
                  : fanOff
              }
              transform="translate(580 380) scale(0.25 0.25)"
            ></image>
            <image
              href={
                solarWind.windSpeed.value !== 0 &&
                (solarWind.inputOperationMode === OperationModeType.Mode4 ||
                  solarWind.inputOperationMode === OperationModeType.Mode5) &&
                isPlaying
                  ? turbineOn
                  : turbineOff
              }
              transform="translate(1100 300) scale(0.4 0.4)"
            ></image>
          </g>
        )}
      </svg>
    </div>
  );
};

export default SolarDiagram;
