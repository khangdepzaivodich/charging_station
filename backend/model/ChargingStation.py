from pydantic import BaseModel
from typing import Optional
class Coordinates(BaseModel):
    lat: float
    lng: float

class ChargingStation(BaseModel):
    coords: Coordinates
    name: str
    address: str
    id: str
    chargingPorts: int
    maximumPower: float  
    type: str            
    pricePerKWh: float   
    access_node_id: Optional[int] = None
