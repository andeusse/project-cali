import { useTheme } from '@mui/material';
import { DiagramVariableType } from '../../types/models/common';

type Props = {
  diagram: string;
  variables: DiagramVariableType[];
  width: number;
  height: number;
};

const Diagram = (props: Props) => {
  const { diagram, variables, width, height } = props;
  const array: number[] = new Array(variables.length);

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
        viewBox={`0 0 ${width} ${height}`}
      >
        <image href={diagram}></image>
        <g>
          {variables.map((v, index) => {
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
