import {
  CoolingTowerOutput,
  CoolingTowerParameters,
  CoolingTowerVariables,
} from '../../../types/models/coolingTower';
import DiagramVariables from '../common/DiagramVariables';

type Props = {
  coolingTower: CoolingTowerParameters;
  data: CoolingTowerOutput | undefined;
  isPlaying: boolean;
};

const CoolingTowerDiagram = (props: Props) => {
  const { coolingTower, data, isPlaying } = props;

  return (
    <div
      style={{
        textAlign: 'center',
      }}
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        xmlnsXlink="http://www.w3.org/1999/xlink"
        viewBox={`0 0 4200 2520`}
      >
        <image href={''}></image>
        <DiagramVariables
          data={data}
          variables={CoolingTowerVariables}
          additionalCondition={[]}
          fontSize={40}
        ></DiagramVariables>
      </svg>
    </div>
  );
};

export default CoolingTowerDiagram;
