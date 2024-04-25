import { useTheme } from '@mui/material';
import {
  TurbineOutput,
  TurbineParameters,
  TurbineType,
} from '../../../types/models/turbine';
import { DiagramVariableType } from '../../../types/models/common';

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

type Props = {
  turbine: TurbineParameters;
  data: TurbineOutput | undefined;
  variables: DiagramVariableType[];
  isPlaying: boolean;
};

const TurbineDiagram = (props: Props) => {
  const { turbine, data, variables, isPlaying } = props;
  const theme = useTheme();

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
        <g>
          {variables.map((v) => {
            if (!v.isShown) return null;
            let printValue: string = '';
            if (
              data &&
              typeof data[v.variable as keyof TurbineOutput] === 'number'
            ) {
              printValue = (
                data[v.variable as keyof TurbineOutput] as number
              ).toFixed(v.fixed);
            } else if (
              data &&
              typeof data[v.variable as keyof TurbineOutput] === 'boolean'
            ) {
              printValue = (data[v.variable as keyof TurbineOutput] as boolean)
                ? 'On'
                : 'Off';
            }
            return (
              <g key={v.variable}>
                {data && printValue && (
                  <g transform={`translate(${v.x},${v.y})`}>
                    <text
                      style={{
                        alignmentBaseline: 'central',
                        textAnchor: 'middle',
                        fontSize: '13px',
                        fontWeight: 'bold',
                      }}
                    >{`${v.diagramName}`}</text>
                    <g transform={`translate(75,0)`}>
                      <rect
                        width="80"
                        height="20"
                        x="-40"
                        y="-10"
                        rx="5"
                        ry="5"
                        fill="blue"
                      ></rect>
                      <text
                        style={{
                          alignmentBaseline: 'central',
                          textAnchor: 'middle',
                          fontSize: '13px',
                          fill: 'white',
                        }}
                      >{`${printValue} ${v.unit}`}</text>
                    </g>
                  </g>
                )}
              </g>
            );
          })}
        </g>
      </svg>
    </div>
  );
};

export default TurbineDiagram;
