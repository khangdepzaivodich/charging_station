from pydantic import BaseModel

class VehicleOptions(BaseModel):
    batteryLevel: float
    maxRange: float
    safetyThreshold: float
    consumptionRate: float
    speed: float
    batteryCapacity: float