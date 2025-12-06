from scipy.spatial import KDTree
from typing import List, Tuple
from model.ChargingStation import ChargingStation

class StationIndex:
    def __init__(self, stations: List[ChargingStation]):
        self.stations = stations
        self.coords = [(s.coords.lat, s.coords.lng) for s in stations]
        
        if self.coords:
            self.tree = KDTree(self.coords)
        else:
            self.tree = None

    def find_nearest(self, lat: float, lon: float) -> Tuple[float, ChargingStation]:
        if not self.tree:
            return float('inf'), None
        
        dist, idx = self.tree.query([lat, lon], k=1)
        
        return dist, self.stations[idx]