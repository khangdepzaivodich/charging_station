import { LatLngExpression } from "leaflet";
export default interface MapInterface {
  startCoords: LatLngExpression | null;
  endCoords: LatLngExpression | null;
  startPointName?: string;
  endPointName?: string;
  path?: LatLngExpression[] | null;
}
