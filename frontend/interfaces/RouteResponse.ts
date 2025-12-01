import { LatLngExpression } from "leaflet";
export default interface RouteResponse {
  routePath: LatLngExpression[];
  totalDistance: number;
  totalTime: number;
  chargingStops: {
    id: string;
    name: string;
    coords: LatLngExpression;
    arrivalBattery: number;
    chargeTime: number;
  }[];
}
