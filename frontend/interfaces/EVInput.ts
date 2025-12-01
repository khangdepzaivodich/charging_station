export default interface EVInputParams {
  maxBattery: number;
  currentBattery: number;
  consumption: number;
  minSafeBattery: number;
  filters: {
    avoidHighways: boolean;
    avoidTolls: boolean;
  };
}
