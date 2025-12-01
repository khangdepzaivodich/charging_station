from fastapi import FastAPI
from pydantic import BaseModel
from typing import Tuple, Dict
import osmnx as ox
from fastapi.middleware.cors import CORSMiddleware
from typing import List
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Vehicle(BaseModel):
    batteryLevel: float
    maxRange: float
    safetyThreshold: float


class Options(BaseModel):
    preference: str | None = None
    filters: Dict | None = None


class RouteRequest(BaseModel):
    start: List[float] 
    end: List[float]
    vehicle: Vehicle
    options: Options


@app.post("/route")
async def compute_route(req: RouteRequest):

    G = ox.graph_from_point(req.start, dist=5000, network_type="drive")
    orig = ox.nearest_nodes(G, req.start[1], req.start[0])
    dest = ox.nearest_nodes(G, req.end[1], req.end[0])
    route = ox.shortest_path(G, orig, dest)

    if route is None:
        return {"error": "No route found"}

    path_coords = [(G.nodes[n]["y"], G.nodes[n]["x"]) for n in route]

    
    total_length = 0
    for u, v in zip(route[:-1], route[1:]):
        edge_data = list(G.get_edge_data(u, v).values())[0]
        total_length += edge_data.get("length", 0)

    return {"path": path_coords, "length_meters": total_length}



@app.get("/")
def home():
    return {"message": "FastAPI Routing Server Ready"}

