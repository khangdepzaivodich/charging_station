from typing import Tuple
from model.VehicleOptions import VehicleOptions

def calculate_step_cost(
    edge_length_m: float,
    vehicle: VehicleOptions,
    preference: str,
    current_battery_pct: float
) -> Tuple[float, float, float, float]:
    distance_km = edge_length_m / 1000.0
    travel_time_hours = distance_km / vehicle.speed
    
    # Tính tiêu hao năng lượng
    energy_consumed_kwh = vehicle.consumptionRate * (distance_km / 100.0)
    battery_drain_pct = (energy_consumed_kwh / vehicle.batteryCapacity) * 100.0
    final_battery_pct = current_battery_pct - battery_drain_pct

    # Nếu hết pin (âm) => Trả về vô cực để A* không chọn đường này (trừ khi rẽ vào trạm)
    if final_battery_pct < 0:
        return float('inf'), final_battery_pct, travel_time_hours, distance_km

    # Tính step_cost theo tiêu chí
    step_cost = 0.0
    if preference == "distance":
        step_cost = distance_km
    elif preference == "cost":
        # Giả sử chi phí vận hành ~ distance (chưa tính phí sạc)
        step_cost = distance_km 
    else:  # time (default)
        step_cost = travel_time_hours

    return step_cost, final_battery_pct, travel_time_hours, distance_km