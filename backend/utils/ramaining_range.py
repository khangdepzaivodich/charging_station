from model.VehicleOptions import VehicleOptions

def remaining_range(vehicle: VehicleOptions, current_battery_pct: float) -> float:
    energy_remain = current_battery_pct / 100 * vehicle.batteryCapacity  
    range_km = energy_remain / vehicle.consumptionRate * 100  
    return range_km