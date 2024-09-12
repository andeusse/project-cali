import React from 'react';
import {
  BiochemicalMethanePotentialOutput,
  BiochemicalMethanePotentialParameters,
} from '../../../types/models/biochemicalMethanePotential';

type Props = {
  bmp: BiochemicalMethanePotentialParameters;
  data: BiochemicalMethanePotentialOutput | undefined;
  isPlaying: boolean;
};

const BiochemicalMethanePotentialDiagram = (props: Props) => {
  const { bmp, data, isPlaying } = props;
  return <div>BiochemicalMethanePotentialDiagram</div>;
};

export default BiochemicalMethanePotentialDiagram;
