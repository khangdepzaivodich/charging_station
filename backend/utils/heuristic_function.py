# utils/heuristic_function.py
from typing import List, Optional
from model.VehicleOptions import VehicleOptions
from model.ChargingStation import ChargingStation
import osmnx as ox
from utils.ramaining_range import remaining_range
from utils.charging_time import optimal_charging_time

def heuristic(
    G,
    a_node: int,
    b_node: int,
    vehicle: VehicleOptions,
    stations: List[ChargingStation] = [],
    preference: Optional[str] = "time"
):
    ay, ax = G.nodes[a_node]["y"], G.nodes[a_node]["x"]
    by, bx = G.nodes[b_node]["y"], G.nodes[b_node]["x"]
    distance_m = ox.distance.euclidean(ay, ax, by, bx)
    distance_km = distance_m / 1000
    rem_range_km = remaining_range(vehicle)

    if preference == "distance":
        return distance_km

    elif preference == "charging":
        if rem_range_km >= distance_km and vehicle.batteryLevel > vehicle.safetyThreshold:
            return 0
        elif stations:
            station_distances = [
                (ox.distance.euclidean((ay, ax), (s.coords.lat, s.coords.lng)), s) for s in stations
            ]
            nearest_station = min(station_distances, key=lambda x: x[0])[1]
            return 1
        else:
            return 1

    else: 
        travel_time = distance_km / vehicle.speed
        if rem_range_km < distance_km or vehicle.batteryLevel <= vehicle.safetyThreshold:
            if stations:
                station_distances = [
                    (ox.distance.euclidean((ay, ax), (s.coords.lat, s.coords.lng)), s) for s in stations
                ]
                nearest_station = min(station_distances, key=lambda x: x[0])[1]
                charging_time = optimal_charging_time(vehicle, nearest_station, distance_km)
            else:
                charging_time = 1.0
        else:
            charging_time = 0.0
        return travel_time + charging_time
