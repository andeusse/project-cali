import React from 'react';
import {
  HydrogenCellOutput,
  HydrogencellParameters,
} from '../../../types/models/hydrogenCell';

type Props = {
  hydrogenCell: HydrogencellParameters;
  data: HydrogenCellOutput | undefined;
  isPlaying: boolean;
};

const HydrogenCellDiagram = (props: Props) => {
  return <div>HydrogenCellDiagram</div>;
};

export default HydrogenCellDiagram;
