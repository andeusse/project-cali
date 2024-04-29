import {
  PELTON_TURBINE_DIAGRAM_VARIABLES,
  TURGO_TURBINE_DIAGRAM_VARIABLES,
  TurbineOutput,
  TurbineParameters,
  TurbineType,
} from '../../../types/models/turbine';

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
import DiagramVariables from '../common/DiagramVariables';

import battery from '../../../assets/common/battery-empty.svg';
import { useEffect, useState } from 'react';

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
        viewBox={`0 0 2100 1260`}
      >
        <rect
          width="2100"
          height="1260"
          x="0"
          y="0"
          rx="20"
          ry="20"
          fill="white"
        />
        <image
          href={
            turbine.turbineType === TurbineType.Pelton
              ? peltonDiagram
              : turgoDiagram
          }
        ></image>
        {turbine.turbineType === TurbineType.Pelton && (
          <g>
            <rect
              width="110"
              height={2 * batteryStateOfCharge}
              x="873"
              y={-2 * batteryStateOfCharge + 888}
              rx="20"
              ry="20"
              fill="green"
            />
            <image
              href={battery}
              transform="translate(800 650) scale(0.5 0.5)"
            ></image>
          </g>
        )}
        {turbine.turbineType === TurbineType.Turgo && (
          <g>
            <rect
              width="110"
              height={2 * batteryStateOfCharge}
              x="873"
              y={-2 * batteryStateOfCharge + 388}
              rx="20"
              ry="20"
              fill="green"
            />
            <image
              href={battery}
              transform="translate(800 150) scale(0.5 0.5)"
            ></image>
          </g>
        )}
        {turbine.turbineType === TurbineType.Pelton && !isPlaying && (
          <image
            href={peltonTurbineOff}
            transform="translate(310 220) scale(0.1 0.1)"
          ></image>
        )}
        {turbine.turbineType === TurbineType.Turgo && !isPlaying && (
          <image
            href={turgoTurbineOff}
            transform="translate(325 800) scale(0.1 0.1)"
          ></image>
        )}
        {turbine.turbineType === TurbineType.Pelton && isPlaying && (
          <image
            href={peltonTurbine}
            transform="translate(310 220) scale(0.1 0.1)"
          ></image>
        )}
        {turbine.turbineType === TurbineType.Turgo && isPlaying && (
          <image
            href={isPlaying ? turgoTurbine : turgoTurbineOff}
            transform="translate(325 800) scale(0.1 0.1)"
          ></image>
        )}
        <image
          href={turbine.inputActivePower.value !== 0 ? cargaACOn : cargaACOff}
          transform="translate(1500 770) scale(0.5 0.5)"
        ></image>
        {turbine.turbineType === TurbineType.Turgo && (
          <image
            href={turbine.inputDirectCurrentPower ? cargaDCOn : cargaDCOff}
            transform="translate(940 975) scale(0.4 0.4)"
          ></image>
        )}
        <DiagramVariables
          data={data}
          variables={
            turbine.turbineType === TurbineType.Pelton
              ? PELTON_TURBINE_DIAGRAM_VARIABLES
              : TURGO_TURBINE_DIAGRAM_VARIABLES
          }
          additionalCondition={turbine.turbineType === TurbineType.Turgo}
        ></DiagramVariables>
      </svg>
    </div>
  );
};

export default TurbineDiagram;
