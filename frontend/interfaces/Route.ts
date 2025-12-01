export default interface Route {
  orig_node: number;
  dest_node: number;
  node_path: number[];
  path: [number, number][];
  length_meters: number;
  estimated_time_hours: number;
  vehicle_range_km: number;
}
