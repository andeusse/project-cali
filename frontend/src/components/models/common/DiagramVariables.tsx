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
        if (data && typeof data[v.variable as keyof T] === 'number') {
          printValue = (data[v.variable as keyof T] as number).toFixed(v.fixed);
        } else if (data && typeof data[v.variable as keyof T] === 'boolean') {
          printValue = (data[v.variable as keyof T] as boolean) ? 'On' : 'Off';
        }
        return (
          <g key={v.variable}>
            {printValue && v.diagramName !== '' && (
              <g transform={`translate(${v.x},${v.y})`}>
                <text
                  style={{
                    alignmentBaseline: 'central',
                    fontSize: `${fontSize}px`,
                    fontWeight: 'bold',
                    fill: theme.palette.text.primary,
                  }}
                >{`${v.diagramName}`}</text>
                <g transform={`translate(${fontSize * 10},0)`}>
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
                    fontSize: `${fontSize}px`,
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