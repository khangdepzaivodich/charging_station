from fastapi import FastAPI, HTTPException
import osmnx as ox
from fastapi.middleware.cors import CORSMiddleware
from model.RouteRequest import RouteRequest
from utils.build_adj_list import build_adj_list
from utils.ramaining_range import remaining_range
from algorithms.a_star import a_star


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/route")
async def compute_route(req: RouteRequest):
    try:
        direct_dist = ox.distance.great_circle(req.start[0], req.start[1], req.end[0], req.end[1])
        radius = max(500, direct_dist * 1.5)
        G = ox.graph_from_point(req.start, dist=radius, network_type="drive")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error building graph: {e}")

    try:
        orig = ox.nearest_nodes(G, req.start[1], req.start[0])
        dest = ox.nearest_nodes(G, req.end[1], req.end[0])
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error finding nearest nodes: {e}")

    filters = req.options.filters if req.options else None
    adj = build_adj_list(G, filters)

    preference = req.options.preference if req.options and req.options.preference else "time"
    node_path, total_time = a_star(adj, G, orig, dest, req.vehicle, req.chargingStations, preference)

    if node_path is None:
        raise HTTPException(status_code=404, detail="No path found")

    path_coords = [(G.nodes[n]["y"], G.nodes[n]["x"]) for n in node_path]
    total_length = 0.0
    for u, v in zip(node_path[:-1], node_path[1:]):
        edges = G.get_edge_data(u, v)
        edge_list = list(edges.values())
        chosen = min(edge_list, key=lambda d: d.get("length", float("inf")))
        total_length += chosen.get("length", 0.0)

    return {
        "orig_node": int(orig),
        "dest_node": int(dest),
        "node_path": node_path,
        "path": path_coords,
        "length_meters": total_length,
        "estimated_time_hours": total_time,
        "vehicle_range_km": remaining_range(req.vehicle)
    }

@app.get("/nodes_in_radius")
async def get_nodes_in_radius(lat: float, lon: float, radius: float):
    try:
        G = ox.graph_from_point((lat, lon), dist=radius, network_type="drive")
        nodes = list(G.nodes)
        return {"nodes": nodes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving nodes: {e}")

@app.get("/")
def home():
    return {"message": "FastAPI Routing Server Ready"}
