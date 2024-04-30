import React from 'react';
import { DiagramVariableType } from '../../../types/models/common';
import { useTheme } from '@mui/material';

type Props<T> = {
  data: T;
  variables: DiagramVariableType[];
  additionalCondition?: boolean;
};

const DiagramVariables = <T,>(props: Props<T>) => {
  const { data, variables, additionalCondition } = props;
  const theme = useTheme();

  return (
    <g>
      {variables.map((v) => {
        if (!v.isShown) return null;
        if (v.hasAdditionalCondition && additionalCondition) return null;
        let printValue: string = '-';
        if (data && typeof data[v.variable as keyof T] === 'number') {
          printValue = (data[v.variable as keyof T] as number).toFixed(v.fixed);
        } else if (data && typeof data[v.variable as keyof T] === 'boolean') {
          printValue = (data[v.variable as keyof T] as boolean) ? 'On' : 'Off';
        }
        return (
          <g key={v.variable}>
            {printValue && (
              <g transform={`translate(${v.x},${v.y})`}>
                <text
                  style={{
                    alignmentBaseline: 'central',
                    fontSize: '40px',
                    fontWeight: 'bold',
                    fill: theme.palette.text.primary,
                  }}
                >{`${v.diagramName}`}</text>
                <g transform={`translate(400,0)`}>
                  <rect
                    width="240"
                    height="60"
                    x="-120"
                    y="-30"
                    rx="5"
                    ry="5"
                    fill="blue"
                  ></rect>
                  <text
                    style={{
                      alignmentBaseline: 'central',
                      textAnchor: 'middle',
                      fontSize: '40px',
                      fill: 'white',
                    }}
                  >{`${printValue} ${printValue !== '-' ? v.unit : ''}`}</text>
                </g>
              </g>
            )}
          </g>
        );
      })}
    </g>
  );
};

export default DiagramVariables;
