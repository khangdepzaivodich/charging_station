export default interface UserInput {
  start: [number, number];
  end: [number, number];
  vehicle: {
    batteryLevel: number;
    maxRange: number;
    safetyThreshold: number;
  };
  options: {
    preference: string;
    filters?: {
      avoidHighways: boolean;
      avoidTolls: boolean;
    };
  };
}
