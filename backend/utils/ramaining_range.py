from model.VehicleOptions import VehicleOptions

def remaining_range(vehicle: VehicleOptions) -> float:
    energy_remain = vehicle.batteryLevel / 100 * vehicle.batteryCapacity  
    range_km = energy_remain / vehicle.consumptionRate * 100  
    return range_km