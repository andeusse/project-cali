import React, { useEffect, useState } from 'react';
import {
  OperationModeType,
  MODE_1_CADMIO_MODE_2,
  MODE_1_MODE_3,
  MODE_2_HYBRID_DIAGRAM_VARIABLES,
  MODE_4,
  MODE_5,
  SolarWindOutput,
  SolarWindParameters,
} from '../../../types/models/solar';
import DiagramVariables from '../common/DiagramVariables';

import mode1CadmioMode2Diagram from '../../../assets/solar/solarWindMode1CadmioMode2.png';
import mode1Mode3Diagram from '../../../assets/solar/solarWindMode1Mode3.png';
import mode2HybridDiagram from '../../../assets/solar/solarWindMode2Hybrid.png';
import mode4Diagram from '../../../assets/solar/solarWindMode4.png';
import mode5Diagram from '../../../assets/solar/solarWindMode5.png';

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

  const [diagramVariables, setDiagramVariables] = useState(MODE_1_MODE_3);

  useEffect(() => {
    if (
      (solarWind.inputOperationMode === OperationModeType.Mode1 &&
        solarWind.cadmiumTelluridePanel.isConnected) ||
      (solarWind.inputOperationMode === OperationModeType.Mode2 &&
        !solarWind.hybridInverter.isConnected)
    ) {
      setDiagramVariables(MODE_1_CADMIO_MODE_2);
    } else if (
      (solarWind.inputOperationMode === OperationModeType.Mode1 &&
        !solarWind.cadmiumTelluridePanel.isConnected) ||
      solarWind.inputOperationMode === OperationModeType.Mode3
    ) {
      setDiagramVariables(MODE_1_MODE_3);
    } else if (
      solarWind.inputOperationMode === OperationModeType.Mode2 &&
      solarWind.hybridInverter.isConnected
    ) {
      setDiagramVariables(MODE_2_HYBRID_DIAGRAM_VARIABLES);
    } else if (solarWind.inputOperationMode === OperationModeType.Mode4) {
      setDiagramVariables(MODE_4);
    } else if (solarWind.inputOperationMode === OperationModeType.Mode5) {
      setDiagramVariables(MODE_5);
    }
  }, [
    solarWind.cadmiumTelluridePanel.isConnected,
    solarWind.hybridInverter.isConnected,
    solarWind.inputOperationMode,
  ]);

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
        {((solarWind.inputOperationMode === OperationModeType.Mode1 &&
          solarWind.cadmiumTelluridePanel.isConnected) ||
          (solarWind.inputOperationMode === OperationModeType.Mode2 &&
            !solarWind.hybridInverter.isConnected)) && (
          <g>
            <image href={mode1CadmioMode2Diagram}></image>
            <image
              href={
                solarWind.directCurrentLoadPower.value !== 0
                  ? cargaDCOn
                  : cargaDCOff
              }
              transform="translate(1430 1700) scale(0.8 0.8)"
            ></image>
            <image
              href={
                solarWind.alternCurrentLoadPower.value !== 0
                  ? cargaACOn
                  : cargaACOff
              }
              transform="translate(2550 1500) scale(1 1)"
            ></image>
            <image
              href={
                solarWind.solarRadiation1.value !== 0 ||
                solarWind.solarRadiation2.value !== 0
                  ? lightOn
                  : lightOff
              }
              transform="translate(50 1400) scale(0.5 0.5)"
            ></image>
          </g>
        )}

        {((solarWind.inputOperationMode === OperationModeType.Mode1 &&
          !solarWind.cadmiumTelluridePanel.isConnected) ||
          solarWind.inputOperationMode === OperationModeType.Mode3) && (
          <g>
            <image href={mode1Mode3Diagram}></image>
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
                solarWind.solarRadiation1.value !== 0 ||
                solarWind.solarRadiation2.value !== 0
                  ? lightOn
                  : lightOff
              }
              transform="translate(350 1400) scale(0.5 0.5)"
            ></image>
          </g>
        )}

        {solarWind.inputOperationMode === OperationModeType.Mode2 &&
          solarWind.hybridInverter.isConnected && (
            <g>
              <image href={mode2HybridDiagram}></image>
              <image
                href={
                  solarWind.alternCurrentLoadPower.value !== 0
                    ? cargaACOn
                    : cargaACOff
                }
                transform="translate(2450 1100) scale(1 1)"
              ></image>
              <image
                href={
                  solarWind.solarRadiation1.value !== 0 ||
                  solarWind.solarRadiation2.value !== 0
                    ? lightOn
                    : lightOff
                }
                transform="translate(150 350) scale(0.5 0.5)"
              ></image>
            </g>
          )}

        {solarWind.inputOperationMode === OperationModeType.Mode4 && (
          <g>
            <image href={mode4Diagram}></image>
            <image
              href={
                solarWind.directCurrentLoadPower.value !== 0
                  ? cargaDCOn
                  : cargaDCOff
              }
              transform="translate(1730 1700) scale(0.8 0.8)"
            ></image>
          </g>
        )}

        {solarWind.inputOperationMode === OperationModeType.Mode5 && (
          <g>
            <image href={mode5Diagram}></image>
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
                solarWind.solarRadiation1.value !== 0 ||
                solarWind.solarRadiation2.value !== 0
                  ? lightOn
                  : lightOff
              }
              transform="translate(350 1400) scale(0.5 0.5)"
            ></image>
          </g>
        )}

        <DiagramVariables
          data={data}
          variables={diagramVariables}
          additionalCondition={solarWind.inputOfflineOperation}
        ></DiagramVariables>

        {!(
          solarWind.inputOperationMode === OperationModeType.Mode2 &&
          solarWind.hybridInverter.isConnected
        ) && (
          <g transform="translate(2150,700) scale(0.5,0.5)">
            <BatteryStateOfCharge
              batteryStateOfCharge={batteryStateOfCharge}
            ></BatteryStateOfCharge>
          </g>
        )}

        {solarWind.inputOperationMode === OperationModeType.Mode2 &&
          solarWind.hybridInverter.isConnected && (
            <g transform="translate(3325,1500) scale(0.5,0.5)">
              <BatteryStateOfCharge
                batteryStateOfCharge={batteryStateOfCharge}
              ></BatteryStateOfCharge>
            </g>
          )}

        {(solarWind.inputOperationMode === OperationModeType.Mode4 ||
          solarWind.inputOperationMode === OperationModeType.Mode5) && (
          <g>
            <image
              href={
                solarWind.windSpeed.value !== 0 && isPlaying ? fanOn : fanOff
              }
              transform="translate(580 380) scale(0.25 0.25)"
            ></image>
            <image
              href={
                solarWind.windSpeed.value !== 0 && isPlaying
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
