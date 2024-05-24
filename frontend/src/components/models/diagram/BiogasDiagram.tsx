import React, { useEffect, useState } from 'react';
import {
  BiogasOutput,
  BiogasParameters,
  OperationModeType,
} from '../../../types/models/biogas';
import { DiagramVariableType } from '../../../types/models/common';

import mode1 from '../../../assets/biogas/Mode1.png';
import mode1On from '../../../assets/biogas/Mode1On.gif';
import mode2 from '../../../assets/biogas/Mode2.png';
import mode2On from '../../../assets/biogas/Mode2On.gif';
import mode3 from '../../../assets/biogas/Mode3.png';
import mode3On from '../../../assets/biogas/Mode3On.gif';
import mode4 from '../../../assets/biogas/Mode4.png';
import mode4On from '../../../assets/biogas/Mode4On.gif';
import mode5 from '../../../assets/biogas/Mode5.png';
import mode5On from '../../../assets/biogas/Mode5On.gif';

type Props = {
  biogas: BiogasParameters;
  data: BiogasOutput | undefined;
  isPlaying: boolean;
  diagramVariables: DiagramVariableType[];
};

const BiogasDiagram = (props: Props) => {
  const { biogas, data, isPlaying, diagramVariables } = props;

  const [viewBoxWidth, setViewBoxWidth] = useState(8164);
  const [viewBoxHeight, setViewBoxHeight] = useState(6803);

  useEffect(() => {
    if (
      biogas.inputOperationMode === OperationModeType.Modo1 ||
      biogas.inputOperationMode === OperationModeType.Modo2
    ) {
      setViewBoxWidth(8164);
      setViewBoxHeight(6803);
    }
    if (biogas.inputOperationMode === OperationModeType.Modo3) {
      setViewBoxWidth(9638);
      setViewBoxHeight(6803);
    }
    if (
      biogas.inputOperationMode === OperationModeType.Modo4 ||
      biogas.inputOperationMode === OperationModeType.Modo5
    ) {
      setViewBoxWidth(10772);
      setViewBoxHeight(7370);
    }
  }, [biogas.inputOperationMode]);

  return (
    <div
      style={{
        textAlign: 'center',
      }}
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        xmlnsXlink="http://www.w3.org/1999/xlink"
        viewBox={`0 0 ${viewBoxWidth} ${viewBoxHeight}`}
      >
        {biogas.inputOperationMode === OperationModeType.Modo1 && (
          <image href={!isPlaying ? mode1 : mode1On}></image>
        )}
        {biogas.inputOperationMode === OperationModeType.Modo2 && (
          <image href={!isPlaying ? mode2 : mode2On}></image>
        )}
        {biogas.inputOperationMode === OperationModeType.Modo3 && (
          <image href={!isPlaying ? mode3 : mode3On}></image>
        )}
        {biogas.inputOperationMode === OperationModeType.Modo4 && (
          <image href={!isPlaying ? mode4 : mode4On}></image>
        )}
        {biogas.inputOperationMode === OperationModeType.Modo5 && (
          <image href={!isPlaying ? mode5 : mode5On}></image>
        )}
      </svg>
    </div>
  );
};

export default BiogasDiagram;
