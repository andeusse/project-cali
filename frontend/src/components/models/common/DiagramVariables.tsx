import React from 'react';
import { DiagramVariableType } from '../../../types/models/common';

type Props<T> = {
  data: T;
  variables: DiagramVariableType[];
  additionalCondition?: boolean;
};

const DiagramVariables = <T,>(props: Props<T>) => {
  const { data, variables, additionalCondition } = props;
  return (
    <g>
      {variables.map((v) => {
        if (!v.isShown) return null;
        if (v.hasAdditionalCondition && !additionalCondition) return null;
        let printValue: string = '';
        if (data && typeof data[v.variable as keyof T] === 'number') {
          printValue = (data[v.variable as keyof T] as number).toFixed(v.fixed);
        } else if (data && typeof data[v.variable as keyof T] === 'boolean') {
          printValue = (data[v.variable as keyof T] as boolean) ? 'On' : 'Off';
        }
        return (
          <g key={v.variable}>
            {data && printValue && (
              <g transform={`translate(${v.x},${v.y})`}>
                <text
                  style={{
                    alignmentBaseline: 'central',
                    fontSize: '20px',
                    fontWeight: 'bold',
                  }}
                >{`${v.diagramName}`}</text>
                <g transform={`translate(180,0)`}>
                  <rect
                    width="120"
                    height="30"
                    x="-60"
                    y="-15"
                    rx="5"
                    ry="5"
                    fill="blue"
                  ></rect>
                  <text
                    style={{
                      alignmentBaseline: 'central',
                      textAnchor: 'middle',
                      fontSize: '20px',
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
  );
};

export default DiagramVariables;
