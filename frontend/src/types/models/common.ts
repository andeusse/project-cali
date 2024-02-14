export default interface commonParameters {
  scenarioName: string;
  simulationSteps: number;
  stepTime: number;
  stepUnit: 'hour' | 'minute' | 'second';
}

export interface bodyTest {
  data: string;
}

export interface respTest {
  data: string;
}
