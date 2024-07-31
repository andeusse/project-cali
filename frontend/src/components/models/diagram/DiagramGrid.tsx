import React from 'react';

type Props = {
  width: number;
  height: number;
};

const DiagramGrid = (props: Props) => {
  const { width, height } = props;
  return (
    <>
      <g>
        {Array(Math.floor(width / 100))
          .fill(0)
          .map((_, index) => {
            return (
              <line
                x1={(index + 1) * 100}
                y1={0}
                x2={(index + 1) * 100}
                y2={height}
                style={{
                  stroke: 'white',
                  strokeWidth: (index + 1) % 10 === 0 ? 20 : 1,
                }}
              ></line>
            );
          })}
      </g>
      <g>
        {Array(Math.floor(height / 100))
          .fill(0)
          .map((_, index) => {
            return (
              <line
                x1={0}
                y1={(index + 1) * 100}
                x2={width}
                y2={(index + 1) * 100}
                style={{
                  stroke: 'white',
                  strokeWidth: (index + 1) % 10 === 0 ? 20 : 1,
                }}
              ></line>
            );
          })}
      </g>
    </>
  );
};

export default DiagramGrid;
