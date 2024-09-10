import {
  ElectronicLoadModeText,
  HYDROGEN_CELL_DIAGRAM_VARIABLES,
  HydrogenCellOutput,
  HydrogencellParameters,
  LightsModeType,
} from '../../../types/models/hydrogenCell';
import hydrogenCellOff from '../../../assets/hydrogen/hydrogen.png';
import hydrogenCellOn1 from '../../../assets/hydrogen/hydrogenOn1.gif';
import hydrogenCellOn2 from '../../../assets/hydrogen/hydrogenOn2.gif';
import hydrogenCellOn3 from '../../../assets/hydrogen/hydrogenOn3.gif';
import DiagramVariables from '../common/DiagramVariables';
import { useEffect, useState } from 'react';
import { getValueByKey } from '../../../utils/getValueByKey';
import { useTheme } from '@mui/material';

type Props = {
  hydrogenCell: HydrogencellParameters;
  data: HydrogenCellOutput | undefined;
  isPlaying: boolean;
};

const HydrogenCellDiagram = (props: Props) => {
  const theme = useTheme();

  const { hydrogenCell, data, isPlaying } = props;
  const [modeText, setModeText] = useState('');

  useEffect(() => {
    setModeText(
      getValueByKey(ElectronicLoadModeText, hydrogenCell.electronicLoadMode)
    );
  }, [hydrogenCell.electronicLoadMode]);

  return (
    <div
      style={{
        textAlign: 'center',
      }}
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        xmlnsXlink="http://www.w3.org/1999/xlink"
        viewBox={`0 0 5500 3500`}
        transform={`scale(0.9 0.9)`}
      >
        <image
          href={
            !isPlaying
              ? hydrogenCellOff
              : !hydrogenCell.lightsConnected
              ? hydrogenCellOn1
              : hydrogenCell.lightsMode === LightsModeType.Parallel
              ? hydrogenCellOn2
              : hydrogenCellOn3
          }
        ></image>
        <text
          transform={`translate(5400, 2450)`}
          style={{
            alignmentBaseline: 'central',
            textAnchor: 'end',
            fontSize: `80px`,
            fontWeight: 'bold',
            fill: theme.palette.text.primary,
          }}
        >
          {`Modo: ${modeText}`}
        </text>
        <DiagramVariables
          data={data}
          variables={HYDROGEN_CELL_DIAGRAM_VARIABLES}
          additionalCondition={[true]}
          fontSize={70}
        ></DiagramVariables>
      </svg>
    </div>
  );
};

export default HydrogenCellDiagram;
