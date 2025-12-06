from model.VehicleOptions import VehicleOptions
from model.ChargingStation import ChargingStation

def optimal_charging_time(
    vehicle: VehicleOptions, 
    station: ChargingStation, 
    distance_to_goal: float, 
    current_battery_pct: float
) -> tuple[float, float, float]:
    
    battery_capacity_kwh = vehicle.batteryCapacity          
    energy_current = (current_battery_pct / 100.0) * battery_capacity_kwh
    energy_min = (vehicle.safetyThreshold / 100.0) * battery_capacity_kwh
    
    TARGET_PCT = 85.0
    energy_target_std = (TARGET_PCT / 100.0) * battery_capacity_kwh
    
    energy_needed_dist = ((distance_to_goal * vehicle.consumptionRate) / 100.0) * 1.5
    energy_target_req = energy_needed_dist + energy_min

    energy_target = max(energy_target_std, energy_target_req)

    min_added = 0.10 * battery_capacity_kwh
    if (energy_target - energy_current) < min_added:
         energy_target = min(energy_current + min_added, battery_capacity_kwh)

    energy_target = min(energy_target, battery_capacity_kwh)

    energy_to_charge = max(0.0, energy_target - energy_current)

    if energy_to_charge <= 0:   
        return 0.0, 0.0, current_battery_pct

    real_power = station.maximumPower

    charging_time_hours = energy_to_charge / real_power
    cost_added = energy_to_charge * station.pricePerKWh

    new_energy = energy_current + energy_to_charge
    new_battery_percent = (new_energy / battery_capacity_kwh) * 100.0
    new_battery_percent = min(new_battery_percent, 100.0)

    return charging_time_hours, cost_added, new_battery_percent