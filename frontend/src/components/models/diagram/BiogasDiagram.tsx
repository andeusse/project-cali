import {
  BiogasOutput,
  BiogasParameters,
  DiagramBiogasType,
  DiagramBiogasUnitType,
  DiagramCompoundType,
  DiagramHumidityType,
  OperationModelType,
  OperationModeType,
} from '../../../types/models/biogas';
import { DiagramVariableType } from '../../../types/models/common';
import { useTheme } from '@mui/material';

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
import DiagramVariables from '../common/DiagramVariables';

type Props = {
  biogas: BiogasParameters;
  data: BiogasOutput | undefined;
  isPlaying: boolean;
  diagramVariables: DiagramVariableType[];
};

const VIEWBOX_WIDTH = 9600;
const VIEWBOX_HEIGHT = 7200;

const BiogasDiagram = (props: Props) => {
  const { biogas, data, isPlaying, diagramVariables } = props;
  const theme = useTheme();

  return (
    <div
      style={{
        textAlign: 'center',
      }}
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        xmlnsXlink="http://www.w3.org/1999/xlink"
        viewBox={`0 0 ${VIEWBOX_WIDTH} ${VIEWBOX_HEIGHT}`}
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
        <g transform={`translate(1000,125)`}>
          <text
            style={{
              alignmentBaseline: 'central',
              textAnchor: 'middle',
              fontSize: `250px`,
              fill: theme.palette.text.primary,
            }}
          >
            C
          </text>
        </g>
        <g transform={`translate(1400,125)`}>
          <text
            style={{
              alignmentBaseline: 'central',
              textAnchor: 'middle',
              fontSize: `250px`,
              fill: theme.palette.text.primary,
            }}
          >
            H
          </text>
        </g>
        <g transform={`translate(1800,125)`}>
          <text
            style={{
              alignmentBaseline: 'central',
              textAnchor: 'middle',
              fontSize: `250px`,
              fill: theme.palette.text.primary,
            }}
          >
            O
          </text>
        </g>
        <g transform={`translate(2200,125)`}>
          <text
            style={{
              alignmentBaseline: 'central',
              textAnchor: 'middle',
              fontSize: `250px`,
              fill: theme.palette.text.primary,
            }}
          >
            N
          </text>
        </g>
        <g transform={`translate(2600,125)`}>
          <text
            style={{
              alignmentBaseline: 'central',
              textAnchor: 'middle',
              fontSize: `250px`,
              fill: theme.palette.text.primary,
            }}
          >
            S
          </text>
        </g>
        <DiagramVariables
          data={data}
          variables={diagramVariables}
          additionalCondition={[
            !(
              biogas.operationModelType === OperationModelType.Arrhenius ||
              biogas.operationModelType === OperationModelType.ADM1
            ),
            !(biogas.operationModelType === OperationModelType.Gompertz),
            !(biogas.operationModelType === OperationModelType.Arrhenius),
            !(biogas.operationModelType === OperationModelType.Gompertz),
            !(biogas.operationModelType === OperationModelType.ADM1),
            !(
              biogas.diagramBiogas === DiagramBiogasType.Accumulated &&
              biogas.diagramBiogasUnit === DiagramBiogasUnitType.NormalVolume
            ),
            !(
              biogas.diagramBiogas === DiagramBiogasType.Stored &&
              biogas.diagramBiogasUnit === DiagramBiogasUnitType.NormalVolume
            ),
            !(
              biogas.diagramBiogas === DiagramBiogasType.Accumulated &&
              biogas.diagramBiogasUnit === DiagramBiogasUnitType.Pressure
            ),
            !(
              biogas.diagramBiogas === DiagramBiogasType.Stored &&
              biogas.diagramBiogasUnit === DiagramBiogasUnitType.Pressure
            ),
            !(biogas.diagramCompound === DiagramCompoundType.PartialVolume),
            !(biogas.diagramCompound === DiagramCompoundType.Concentration),
            !(biogas.diagramCompound === DiagramCompoundType.Moles),
            !(biogas.diagramHumidity === DiagramHumidityType.Moles),
            !(biogas.diagramHumidity === DiagramHumidityType.Relative),
          ]}
          fontSize={80}
        ></DiagramVariables>
      </svg>
    </div>
  );
};

export default BiogasDiagram;
