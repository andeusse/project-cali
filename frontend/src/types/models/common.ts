export default interface commonParameters {
  scenarioName: string;
  simulationSteps: number;
  stepTime: number;
  stepUnit: 'hour' | 'minute' | 'second';
}
