import { useTheme } from '@mui/material';
import { DiagramVariableType } from '../../types/models/common';

type Props<T> = {
  diagram: string;
  variables: DiagramVariableType[];
  data: T | undefined;
  width: number;
  height: number;
};

const Diagram = <T,>(props: Props<T>) => {
  const { diagram, variables, data, width, height } = props;
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
        viewBox={`0 0 ${width} ${height}`}
      >
        <image href={diagram}></image>
        <g>
          {variables.map((v) => {
            if (!v.isShown) return null;
            let printValue: string = '';
            if (data && typeof data[v.variable as keyof T] === 'number') {
              printValue = (data[v.variable as keyof T] as number).toFixed(
                v.fixed
              );
            } else if (
              data &&
              typeof data[v.variable as keyof T] === 'boolean'
            ) {
              printValue = (data[v.variable as keyof T] as boolean)
                ? 'On'
                : 'Off';
            }
            return (
              <g key={v.variable} transform={`translate(${v.x},${v.y})`}>
                {data && printValue && (
                  <text
                    style={{
                      alignmentBaseline: 'central',
                      textAnchor: 'middle',
                      fill: theme.palette.text.primary,
                      fontSize: '13px',
                    }}
                  >{`${v.diagramName}: ${printValue} ${v.unit}`}</text>
                )}
              </g>
            );
          })}
        </g>
      </svg>
    </div>
  );
};

export default Diagram;
