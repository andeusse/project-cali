import {
  TURBINE_DIAGRAM_VARIABLES,
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

type Props = {
  turbine: TurbineParameters;
  data: TurbineOutput | undefined;
  isPlaying: boolean;
};

const TurbineDiagram = (props: Props) => {
  const { turbine, data, isPlaying } = props;

  return (
    <div
      style={{
        textAlign: 'center',
      }}
    >
      <svg
        height={'100%'}
        width={'100%'}
        xmlns="http://www.w3.org/2000/svg"
        xmlnsXlink="http://www.w3.org/1999/xlink"
        viewBox={`0 0 800 800`}
      >
        <image
          href={
            turbine.turbineType === TurbineType.Pelton
              ? peltonDiagram
              : turgoDiagram
          }
        ></image>
        {turbine.turbineType === TurbineType.Pelton && isPlaying && (
          <image
            href={peltonTurbine}
            transform="translate(0 0) scale(0.1 0.1)"
          ></image>
        )}
        {turbine.turbineType === TurbineType.Pelton && !isPlaying && (
          <image
            href={peltonTurbineOff}
            transform="translate(0 0) scale(0.42 0.42)"
          ></image>
        )}
        {turbine.turbineType === TurbineType.Turgo && isPlaying && (
          <image
            href={isPlaying ? turgoTurbine : turgoTurbineOff}
            transform="translate(0 0) scale(0.1 0.1)"
          ></image>
        )}
        {turbine.turbineType === TurbineType.Turgo && !isPlaying && (
          <image
            href={turgoTurbineOff}
            transform="translate(0 0) scale(0.42 0.42)"
          ></image>
        )}
        <image
          href={turbine.inputActivePower.value !== 0 ? cargaACOn : cargaACOff}
          transform="translate(550 600) scale(0.5 0.5)"
        ></image>
        {turbine.turbineType === TurbineType.Turgo && (
          <image
            href={turbine.inputDirectCurrentPower ? cargaDCOn : cargaDCOff}
            transform="translate(-50 600) scale(0.5 0.5)"
          ></image>
        )}
        <DiagramVariables
          data={data}
          variables={TURBINE_DIAGRAM_VARIABLES}
          additionalCondition={turbine.turbineType === TurbineType.Turgo}
        ></DiagramVariables>
      </svg>
    </div>
  );
};

export default TurbineDiagram;
