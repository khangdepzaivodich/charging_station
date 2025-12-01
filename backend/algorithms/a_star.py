from typing import Dict, List, Tuple, Optional
import heapq
from utils.heuristic_function import heuristic
from model.VehicleOptions import VehicleOptions
from model.ChargingStation import ChargingStation

def a_star(
    adj: Dict[int, List[Tuple[int, float]]],
    G,
    start: int,
    goal: int,
    vehicle: VehicleOptions,
    stations: List[ChargingStation] = [],
    preference: Optional[str] = "time"
):
    open_set = []
    heapq.heappush(open_set, (0.0, start))
    g_score = {node: float("inf") for node in adj}
    f_score = {node: float("inf") for node in adj}
    parent = {node: None for node in adj}

    g_score[start] = 0.0
    f_score[start] = heuristic(G, start, goal, vehicle, stations, preference)

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            path = []
            cur = goal
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            path.reverse()
            return path, g_score[goal]

        for neighbor, w in adj.get(current, []):
            tentative_g = g_score[current] + w / vehicle.speed
            if tentative_g < g_score.get(neighbor, float("inf")):
                parent[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(G, neighbor, goal, vehicle, stations, preference)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
    return None, float("inf")
