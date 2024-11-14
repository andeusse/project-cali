import React from 'react';
import {
  BiochemicalMethanePotentialOutput,
  BiochemicalMethanePotentialParameters,
  DiagramBiogasMeasurementMethodType,
  PlantOperationType,
} from '../../../types/models/biochemicalMethanePotential';
import { DiagramVariableType } from '../../../types/models/common';

import pbmAOff from '../../../assets/PBM/Lado A/PBM_A.png';
import pbmAPoolOff from '../../../assets/PBM/Lado A/PBM_A_Piscina.png';
import pbmAMixerOn from '../../../assets/PBM/Lado A/PBM_A_Agitador.gif';
import pbmAMixerInjectorOn from '../../../assets/PBM/Lado A/PBM_A_Agitador+Inyector.gif';
import pbmAMixerInjectorPoolOn from '../../../assets/PBM/Lado A/PBM_A_Agitador+Inyector+Piscina.gif';
import pbmAMixerPoolOn from '../../../assets/PBM/Lado A/PBM_A_Inyector.gif';
import pbmAInjectorOn from '../../../assets/PBM/Lado A/PBM_A_Inyector.gif';
import pbmAInjectorPoolOn from '../../../assets/PBM/Lado A/PBM_A_Inyector+Piscina.gif';

import pbmBOff from '../../../assets/PBM/Lado B/PBM_B.png';
import pbmBPoolOff from '../../../assets/PBM/Lado B/PBM_B_Piscina.png';
import pbmBMixerOn from '../../../assets/PBM/Lado B/PBM_B_Agitador.gif';
import pbmBMixerInjectorOn from '../../../assets/PBM/Lado B/PBM_B_Agitador+Inyector.gif';
import pbmBMixerInjectorPoolOn from '../../../assets/PBM/Lado B/PBM_B_Agitador+Inyector+Piscina.gif';
import pbmBMixerPoolOn from '../../../assets/PBM/Lado B/PBM_B_Inyector.gif';
import pbmBInjectorOn from '../../../assets/PBM/Lado B/PBM_B_Inyector.gif';
import pbmBInjectorPoolOn from '../../../assets/PBM/Lado B/PBM_B_Inyector+Piscina.gif';

import DiagramGrid from './DiagramGrid';

type Props = {
  bmp: BiochemicalMethanePotentialParameters;
  data: BiochemicalMethanePotentialOutput | undefined;
  isPlaying: boolean;
  diagramVariables: DiagramVariableType[];
};

const BiochemicalMethanePotentialDiagram = (props: Props) => {
  const { bmp, data, isPlaying, diagramVariables } = props;
  return (
    <div
      style={{
        textAlign: 'center',
      }}
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        xmlnsXlink="http://www.w3.org/1999/xlink"
        viewBox={`0 0 4000 5500`}
      >
        {bmp.plantOperation === PlantOperationType.SideA && (
          <g>
            {bmp.measurementMethodSideA ===
              DiagramBiogasMeasurementMethodType.Pressure && (
              <g>
                {(!isPlaying ||
                  (isPlaying &&
                    data !== null &&
                    data?.mixVelocityR101 === 0 &&
                    data?.caudalSideA === 0)) && (
                  <image
                    transform="translate(0 1500)"
                    href={pbmAOff}
                    width={'100%'}
                  ></image>
                )}

                {isPlaying &&
                  data !== null &&
                  data?.mixVelocityR101 !== 0 &&
                  data?.caudalSideA === 0 && (
                    <image
                      transform="translate(0 1500)"
                      href={pbmAMixerOn}
                      width={'100%'}
                    ></image>
                  )}

                {isPlaying &&
                  data !== null &&
                  data?.mixVelocityR101 === 0 &&
                  data?.caudalSideA !== 0 && (
                    <image
                      transform="translate(0 1500)"
                      href={pbmAInjectorOn}
                      width={'100%'}
                    ></image>
                  )}

                {isPlaying &&
                  data !== null &&
                  data?.mixVelocityR101 !== 0 &&
                  data?.caudalSideA !== 0 && (
                    <image
                      transform="translate(0 1500)"
                      href={pbmAMixerInjectorOn}
                      width={'100%'}
                    ></image>
                  )}
              </g>
            )}

            {bmp.measurementMethodSideA ===
              DiagramBiogasMeasurementMethodType.VolumeDisplaced && (
              <g>
                {(!isPlaying ||
                  (isPlaying &&
                    data !== null &&
                    data?.mixVelocityR101 === 0 &&
                    data?.caudalSideA === 0)) && (
                  <image
                    transform="translate(0 1500)"
                    href={pbmAPoolOff}
                    width={'100%'}
                  ></image>
                )}

                {isPlaying &&
                  data !== null &&
                  data?.mixVelocityR101 !== 0 &&
                  data?.caudalSideA === 0 && (
                    <image
                      transform="translate(0 1500)"
                      href={pbmAMixerPoolOn}
                      width={'100%'}
                    ></image>
                  )}

                {isPlaying &&
                  data !== null &&
                  data?.mixVelocityR101 === 0 &&
                  data?.caudalSideA !== 0 && (
                    <image
                      transform="translate(0 1500)"
                      href={pbmAInjectorPoolOn}
                      width={'100%'}
                    ></image>
                  )}

                {isPlaying &&
                  data !== null &&
                  data?.mixVelocityR101 !== 0 &&
                  data?.caudalSideA !== 0 && (
                    <image
                      transform="translate(0 1500)"
                      href={pbmAMixerInjectorPoolOn}
                      width={'100%'}
                    ></image>
                  )}
              </g>
            )}
          </g>
        )}
        {bmp.plantOperation === PlantOperationType.SideB && (
          <g>
            {bmp.measurementMethodSideB ===
              DiagramBiogasMeasurementMethodType.Pressure && (
              <g>
                {(!isPlaying ||
                  (isPlaying &&
                    data !== null &&
                    data?.mixVelocityR106 === 0 &&
                    data?.caudalsideB === 0)) && (
                  <image
                    transform="translate(0 1500)"
                    href={pbmBOff}
                    width={'100%'}
                  ></image>
                )}

                {isPlaying &&
                  data !== null &&
                  data?.mixVelocityR106 !== 0 &&
                  data?.caudalsideB === 0 && (
                    <image
                      transform="translate(0 1500)"
                      href={pbmBMixerOn}
                      width={'100%'}
                    ></image>
                  )}

                {isPlaying &&
                  data !== null &&
                  data?.mixVelocityR106 === 0 &&
                  data?.caudalsideB !== 0 && (
                    <image
                      transform="translate(0 1500)"
                      href={pbmBInjectorOn}
                      width={'100%'}
                    ></image>
                  )}

                {isPlaying &&
                  data !== null &&
                  data?.mixVelocityR106 !== 0 &&
                  data?.caudalsideB !== 0 && (
                    <image
                      transform="translate(0 1500)"
                      href={pbmBMixerInjectorOn}
                      width={'100%'}
                    ></image>
                  )}
              </g>
            )}

            {bmp.measurementMethodSideB ===
              DiagramBiogasMeasurementMethodType.VolumeDisplaced && (
              <g>
                {(!isPlaying ||
                  (isPlaying &&
                    data !== null &&
                    data?.mixVelocityR106 === 0 &&
                    data?.caudalsideB === 0)) && (
                  <image
                    transform="translate(0 1500)"
                    href={pbmBPoolOff}
                    width={'100%'}
                  ></image>
                )}

                {isPlaying &&
                  data !== null &&
                  data?.mixVelocityR106 !== 0 &&
                  data?.caudalsideB === 0 && (
                    <image
                      transform="translate(0 1500)"
                      href={pbmBMixerPoolOn}
                      width={'100%'}
                    ></image>
                  )}

                {isPlaying &&
                  data !== null &&
                  data?.mixVelocityR106 === 0 &&
                  data?.caudalsideB !== 0 && (
                    <image
                      transform="translate(0 1500)"
                      href={pbmBInjectorPoolOn}
                      width={'100%'}
                    ></image>
                  )}

                {isPlaying &&
                  data !== null &&
                  data?.mixVelocityR106 !== 0 &&
                  data?.caudalsideB !== 0 && (
                    <image
                      transform="translate(0 1500)"
                      href={pbmBMixerInjectorPoolOn}
                      width={'100%'}
                    ></image>
                  )}
              </g>
            )}
          </g>
        )}
        <DiagramGrid height={5500} width={4000}></DiagramGrid>
      </svg>
    </div>
  );
};

export default BiochemicalMethanePotentialDiagram;
