from pydantic import BaseModel

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
