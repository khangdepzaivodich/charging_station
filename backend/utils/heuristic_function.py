import osmnx as ox
from model.VehicleOptions import VehicleOptions

# CẤU HÌNH ƯỚC LƯỢNG
# Dùng công suất sạc MAX để thời gian sạc ước lượng luôn <= thực tế (Admissible)
MAX_CHARGING_POWER_KW = 60.0 
# Dùng giá điện MIN để chi phí ước lượng luôn <= thực tế (Admissible)
MIN_PRICE_PER_KWH = 3000.0 

def calculate_heuristic(
    G,
    current_node: int,
    goal_node: int,
    vehicle: VehicleOptions,        
    preference: str,
    current_battery_pct: float 
) -> float:
    curr_y = G.nodes[current_node]["y"]
    curr_x = G.nodes[current_node]["x"]
    goal_y = G.nodes[goal_node]["y"]
    goal_x = G.nodes[goal_node]["x"]
    
    dist_m = ox.distance.great_circle(curr_y, curr_x, goal_y, goal_x)
    dist_km = dist_m / 1000.0

    h_val = 0.0

    if preference == "distance":
        h_val = dist_km

    elif preference == "time":
        drive_time = dist_km / vehicle.speed
        
        energy_needed_kwh = dist_km * (vehicle.consumptionRate / 100.0)
        current_energy_kwh = (current_battery_pct / 100.0) * vehicle.batteryCapacity
        energy_deficit_kwh = max(0.0, energy_needed_kwh - current_energy_kwh)
        
        charge_time = 0.0
        if energy_deficit_kwh > 0:
            charge_time = energy_deficit_kwh / MAX_CHARGING_POWER_KW
            
        h_val = drive_time + charge_time

    elif preference == "cost":
        energy_needed_kwh = dist_km * (vehicle.consumptionRate / 100.0)
        current_energy_kwh = (current_battery_pct / 100.0) * vehicle.batteryCapacity
        energy_deficit_kwh = max(0.0, energy_needed_kwh - current_energy_kwh)
        
        estimated_charging_cost = energy_deficit_kwh * MIN_PRICE_PER_KWH
        
        h_val = estimated_charging_cost

    return h_val