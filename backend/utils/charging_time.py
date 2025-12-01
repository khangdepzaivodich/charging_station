from model.VehicleOptions import VehicleOptions
from model.ChargingStation import ChargingStation

def optimal_charging_time(vehicle: VehicleOptions, station: ChargingStation, distance_to_goal: float) -> float:
    energy_needed = distance_to_goal * vehicle.consumptionRate / 100
    energy_min = vehicle.safetyThreshold / 100 * vehicle.batteryCapacity
    energy_current = vehicle.batteryLevel / 100 * vehicle.batteryCapacity

    energy_to_charge = max(0.0, energy_needed + energy_min - energy_current)
    charging_time = energy_to_charge / station.maximumPower  
    return charging_time
