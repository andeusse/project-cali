import {
  CoolingTowerOutput,
  CoolingTowerParameters,
  COOLING_TOWER_DIAGRAM_VARIABLES,
} from '../../../types/models/coolingTower';
import DiagramVariables from '../common/DiagramVariables';
import coolingTowerOff from '../../../assets/tower/tower.png';
import coolingTowerOn from '../../../assets/tower/towerOn.gif';

type Props = {
  coolingTower: CoolingTowerParameters;
  data: CoolingTowerOutput | undefined;
  isPlaying: boolean;
};

const CoolingTowerDiagram = (props: Props) => {
  const { data, isPlaying } = props;

  return (
    <div
      style={{
        textAlign: 'center',
      }}
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        xmlnsXlink="http://www.w3.org/1999/xlink"
        viewBox={`0 0 6000 4300`}
        transform={`scale(0.8 0.8)`}
      >
        <image href={!isPlaying ? coolingTowerOff : coolingTowerOn}></image>
        <DiagramVariables
          data={data}
          variables={COOLING_TOWER_DIAGRAM_VARIABLES}
          additionalCondition={[]}
          fontSize={80}
        ></DiagramVariables>
      </svg>
    </div>
  );
};

export default CoolingTowerDiagram;
