import {
  PELTON_TURBINE_DIAGRAM_VARIABLES,
  TURGO_TURBINE_DIAGRAM_VARIABLES,
  TurbineOutput,
  TurbineParameters,
  TurbineType,
} from '../../../types/models/turbine';
import DiagramVariables from '../common/DiagramVariables';

import peltonDiagram from '../../../assets/turbine/peltonDiagram.png';
import turgoDiagram from '../../../assets/turbine/turgoDiagram.png';

import peltonTurbineOff from '../../../assets/turbine/peltonTurbineOff.png';
import turgoTurbineOff from '../../../assets/turbine/turgoTurbineOff.png';
import peltonTurbine from '../../../assets/turbine/peltonTurbine.gif';
import turgoTurbine from '../../../assets/turbine/turgoTurbine.gif';

import cargaACOff from '../../../assets/common/cargaACOff.png';
import cargaACOn from '../../../assets/common/cargaACOn.png';
import cargaDCOff from '../../../assets/common/cargaDCOff.png';
import cargaDCOn from '../../../assets/common/cargaDCOn.png';

import { useEffect, useState } from 'react';
import BatteryStateOfCharge from '../common/BatteryStateOfCharge';

type Props = {
  turbine: TurbineParameters;
  data: TurbineOutput | undefined;
  isPlaying: boolean;
};

const TurbineDiagram = (props: Props) => {
  const { turbine, data, isPlaying } = props;

  const [batteryStateOfCharge, setBatteryStateOfCharge] = useState(
    data ? data.batteryStateOfCharge : turbine.battery.stateOfCharge.value
  );

  useEffect(() => {
    let newValue = data
      ? data.batteryStateOfCharge
      : turbine.battery.stateOfCharge.value;
    if (newValue > 100) {
      newValue = 100;
    } else if (newValue < 0) {
      newValue = 0;
    }
    setBatteryStateOfCharge(newValue);
  }, [data, turbine.battery.stateOfCharge.value]);

  return (
    <div
      style={{
        textAlign: 'center',
      }}
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        xmlnsXlink="http://www.w3.org/1999/xlink"
        viewBox={`0 0 4200 2520`}
      >
        <image
          href={
            turbine.turbineType === TurbineType.Pelton
              ? peltonDiagram
              : turgoDiagram
          }
        ></image>
        <g transform="translate(2300,1500) scale(0.5,0.5)">
          <BatteryStateOfCharge
            batteryStateOfCharge={batteryStateOfCharge}
          ></BatteryStateOfCharge>
        </g>
        {turbine.turbineType === TurbineType.Pelton && !isPlaying && (
          <image
            href={peltonTurbineOff}
            transform="translate(620 440) scale(0.2 0.2)"
          ></image>
        )}
        {turbine.turbineType === TurbineType.Turgo && !isPlaying && (
          <image
            href={turgoTurbineOff}
            transform="translate(650 1600) scale(0.2 0.2)"
          ></image>
        )}
        {turbine.turbineType === TurbineType.Pelton && isPlaying && (
          <image
            href={peltonTurbine}
            transform="translate(620 440) scale(0.2 0.2)"
          ></image>
        )}
        {turbine.turbineType === TurbineType.Turgo && isPlaying && (
          <image
            href={isPlaying ? turgoTurbine : turgoTurbineOff}
            transform="translate(650 1600) scale(0.2 0.2)"
          ></image>
        )}
        <image
          href={data?.inverterActivePower !== 0 ? cargaACOn : cargaACOff}
          transform="translate(3000 1540) scale(1 1)"
        ></image>
        {turbine.turbineType === TurbineType.Turgo && (
          <image
            href={data?.directCurrentLoadPower ? cargaDCOn : cargaDCOff}
            transform="translate(1880 1950) scale(0.8 0.8)"
          ></image>
        )}
        <DiagramVariables
          data={data}
          variables={
            turbine.turbineType === TurbineType.Pelton
              ? PELTON_TURBINE_DIAGRAM_VARIABLES
              : TURGO_TURBINE_DIAGRAM_VARIABLES
          }
          additionalCondition={[
            turbine.inputOfflineOperation,
            turbine.turbineType !== TurbineType.Turgo,
          ]}
          fontSize={40}
        ></DiagramVariables>
      </svg>
    </div>
  );
};

export default TurbineDiagram;
