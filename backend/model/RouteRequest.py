from typing import List, Tuple, Dict, Optional
from pydantic import BaseModel
from .VehicleOptions import VehicleOptions
from .RouteOptions import RouteOptions
from .ChargingStation import ChargingStation

class RouteRequest(BaseModel):
    start: List[float]
    end: List[float]
    vehicle: VehicleOptions
    options: Optional[RouteOptions] = None
    chargingStations: List[ChargingStation] = []