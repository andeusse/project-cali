import React from 'react';
import pelton from '../../assets/peltonTurbine.svg';
import turgo from '../../assets/turgoTurbine.svg';
import { TurbineType, TURBINE_DIAGRAM } from '../../types/models/turbine';
import { useTheme } from '@mui/material';

type Props = { turbineType: TurbineType };

const Diagram = (props: Props) => {
  const { turbineType } = props;
  const array: number[] = new Array(TURBINE_DIAGRAM.variables.length);

  const theme = useTheme();

  array.fill(Math.random() * 100);

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
          href={turbineType === TurbineType.Pelton ? pelton : turgo}
        ></image>
        <g>
          {TURBINE_DIAGRAM.variables.map((v, index) => {
            return (
              <g key={v.name} transform={`translate(${v.x},${v.y})`}>
                <text
                  style={{
                    alignmentBaseline: 'central',
                    textAnchor: 'middle',
                    fill: theme.palette.text.primary,
                    fontSize: '13px',
                  }}
                >{`${v.printedName}: ${array[index].toFixed(v.fixed)} ${
                  v.unit
                }`}</text>
              </g>
            );
          })}
        </g>
      </svg>
    </div>
  );
};

export default Diagram;
