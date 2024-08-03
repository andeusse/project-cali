import React from 'react';
import { DiagramVariableType } from '../../../types/models/common';
import { useTheme } from '@mui/material';

type Props<T> = {
  data: T;
  variables: DiagramVariableType[];
  additionalCondition: boolean[];
  fontSize: number;
};

const DiagramVariables = <T,>(props: Props<T>) => {
  const { data, variables, additionalCondition, fontSize } = props;
  const theme = useTheme();

  return (
    <g>
      {variables.map((v) => {
        if (!v.isShown) return null;
        if (
          additionalCondition.length !== 0 &&
          v.hasAdditionalCondition !== undefined &&
          additionalCondition[v.hasAdditionalCondition]
        )
          return null;

        let printValue: string = '-';
        const value = data ? data[v.variable as keyof T] : null;
        if (data && typeof value === 'number' && !v.scientificNotation) {
          printValue = (value as number).toFixed(v.fixed);
        } else if (data && typeof value === 'number' && v.scientificNotation) {
          printValue = (value as number).toExponential(v.fixed);
        } else if (data && typeof value === 'boolean') {
          printValue = (value as boolean) ? 'On' : 'Off';
        }
        return (
          <g key={v.variable}>
            {printValue && v.diagramName !== '' && (
              <g
                transform={`translate(${v.x ? v.x + fontSize * 5 : 0},${v.y})`}
              >
                <text
                  style={{
                    alignmentBaseline: 'central',
                    textAnchor: 'end',
                    fontSize: `${fontSize}px`,
                    fontWeight: 'bold',
                    fill: theme.palette.text.primary,
                  }}
                >{`${v.diagramName}`}</text>
                <g transform={`translate(${fontSize * 5},0)`}>
                  <rect
                    width={`${fontSize * 6}`}
                    height={`${fontSize * 1.5}`}
                    x={`${fontSize * -3}`}
                    y={`${(fontSize * -3) / 4}`}
                    rx="20"
                    ry="20"
                    fill="blue"
                  ></rect>
                  <text
                    style={{
                      alignmentBaseline: 'central',
                      textAnchor: 'middle',
                      fontSize: `${fontSize}px`,
                      fill: 'white',
                    }}
                  >
                    {`${printValue} ${printValue !== '-' ? v.unit : ''}`}
                  </text>
                </g>
              </g>
            )}
            {printValue && v.diagramName === '' && (
              <g transform={`translate(${v.x},${v.y})`}>
                <text
                  style={{
                    alignmentBaseline: 'central',
                    textAnchor: 'middle',
                    fontSize: `${fontSize * 0.9}px`,
                    fill: theme.palette.text.primary,
                  }}
                >
                  {`${printValue} ${printValue !== '-' ? v.unit : ''}`}
                </text>
              </g>
            )}
          </g>
        );
      })}
    </g>
  );
};

export default DiagramVariables;
