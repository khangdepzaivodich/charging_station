import os
import uvicorn
import osmnx as ox
import networkx as nx
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from model.RouteRequest import RouteRequest
from utils.build_adj_list import build_adj_list
from utils.ramaining_range import remaining_range
from utils.spatial_index import StationIndex
from algorithms.ev_router import find_ev_route_multistop


global_G = None
MAP_FILENAME = "hcmc_map.graphml"
PLACE_NAME = "Ho Chi Minh City, Vietnam"

@asynccontextmanager
async def lifespan(app: FastAPI):
    global global_G
    print(f"\n[STARTUP] Đang khởi động Server cho khu vực: {PLACE_NAME}")
    
    if os.path.exists(MAP_FILENAME):
        print(f"Tìm thấy file cache '{MAP_FILENAME}'. Đang load vào RAM...")
        global_G = ox.load_graphml(MAP_FILENAME)
        print("Load xong bản đồ từ file!")
    else:
        print(f"Chưa có file cache. Đang tải bản đồ từ OpenStreetMap...")
        try:
            global_G = ox.graph_from_place(PLACE_NAME, network_type="drive")
            
            print("Đang tối ưu hóa đồ thị...")
            largest_cc = max(nx.strongly_connected_components(global_G), key=len)
            global_G = global_G.subgraph(largest_cc).copy()
            
            print("Đang lưu file cache...")
            ox.save_graphml(global_G, MAP_FILENAME)
            print("Đã tải và lưu xong!")
            
        except Exception as e:
            print(f"LỖI TẢI MAP: {e}")
            global_G = None

    yield
    global_G = None
    print("Server stopped.")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/route")
async def compute_route(req: RouteRequest):
    if global_G is None:
        raise HTTPException(status_code=503, detail="Bản đồ chưa sẵn sàng hoặc lỗi tải.")

    try:
        orig_node = ox.nearest_nodes(global_G, req.start[1], req.start[0])
        dest_node = ox.nearest_nodes(global_G, req.end[1], req.end[0])
    except Exception as e:
        raise HTTPException(status_code=400, detail="Vị trí nằm ngoài phạm vi bản đồ.")

    station_index = StationIndex(req.chargingStations)
    filters = req.options.filters if req.options else None
    adj = build_adj_list(global_G, filters)
    preference = req.options.preference if req.options and req.options.preference else "time"
    
    try:
        result = find_ev_route_multistop(
            adj=adj,
            G=global_G,
            start=orig_node,
            goal=dest_node,
            vehicle=req.vehicle,
            station_index=station_index,
            preference=preference
        )
    except Exception as e:
        print(f"Algorithm Error: {e}")
        raise HTTPException(status_code=500, detail=f"Lỗi thuật toán: {str(e)}")

    if result is None:
         raise HTTPException(status_code=500, detail="Thuật toán không trả về kết quả.")

    path_nodes = result.get("path", [])
    stats = result.get("stats", {})
    
    if not path_nodes:
        raise HTTPException(status_code=404, detail=result.get("message", "Không tìm thấy đường đi."))

    path_geometry = [(global_G.nodes[n]["y"], global_G.nodes[n]["x"]) for n in path_nodes]
    
    real_dist_m = 0.0
    for u, v in zip(path_nodes[:-1], path_nodes[1:]):
        edge_data = global_G.get_edge_data(u, v)
        if edge_data:
            shortest = min(edge_data.values(), key=lambda x: x.get("length", float("inf")))
            real_dist_m += shortest.get("length", 0.0)

    final_battery = result.get("final_battery_pct", stats.get("battery", 0))
    
    return {
        "status": "success" if result.get("feasible") else "warning", 
        "feasible": result.get("feasible", False),                  
        "type": result.get("type", "UNKNOWN"),                     
        "message": result.get("message", ""),
        "summary": {
            "total_distance_km": round(real_dist_m / 1000, 2),
            "estimated_time_hours": round(stats.get("travel_time", 0), 2),
            "total_cost": round(stats.get("cost", 0), 0),
            "charge_count": stats.get("charge_count", 0),
            "total_charging_time_hours": round(stats.get("charging_time", 0), 2),
            "final_battery_pct": round(final_battery, 1),
            "remaining_range_km": remaining_range(req.vehicle, final_battery)
        },
        "path_geometry": path_geometry, 
        "charging_stations": stats.get("charging_logs", [])
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)