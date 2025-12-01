export default interface ChargingStation {
  coords: {
    lat: number;
    lng: number;
  };
  name: string;
  address: string;
  id: string;
  chargingPorts: number;
  maximumPower: number;
  type: string; // AC or DC
  pricePerKWh: number;
}
