from typing import Dict, List, Tuple, Optional, Any
import heapq
import itertools
import networkx as nx
import osmnx as ox
import math
from model.VehicleOptions import VehicleOptions
from model.ChargingStation import ChargingStation
from utils.spatial_index import StationIndex 
from utils.heuristic_function import calculate_heuristic

def _segment_a_star(
    adj: Dict[int, List[Tuple[int, float]]],
    G: Any,
    start: int,
    goal: int,
    vehicle: VehicleOptions,
    current_battery_pct: float,
    preference: str = "time"
) -> Optional[Dict]:
    """
    Tìm đường A->B. 
    - Sử dụng edge_length từ adjList.
    - Không tính cost di chuyển (tiền) vào g_score.
    """
    open_set = []
    counter = itertools.count() 
    
    # Heuristic
    h_start = calculate_heuristic(G, start, goal, vehicle, preference, current_battery_pct)
    
    # Heap: (f, tie_breaker, node, g, battery_pct)
    heapq.heappush(open_set, (h_start, next(counter), start, 0.0, current_battery_pct))

    g_score = {start: 0.0}
    parent = {start: None}
    
    safety_threshold_pct = vehicle.safetyThreshold

    while open_set:
        f_curr, _, current, g_curr, batt_curr_pct = heapq.heappop(open_set)

        if current == goal:
            path = []
            cur = goal
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            path.reverse()
            return {
                "path": path,
                "g_score": g_curr,
                "final_battery_pct": batt_curr_pct
            }

        if g_curr > g_score.get(current, float('inf')):
            continue

        for neighbor, edge_length_m in adj.get(current, []):
            
            dist_km = edge_length_m / 1000.0
            
            kwh_consumed = dist_km * (vehicle.consumptionRate / 100.0)
            pct_loss = (kwh_consumed / vehicle.batteryCapacity) * 100.0
            new_batt_pct = batt_curr_pct - pct_loss

            # Check an toàn
            if new_batt_pct < safety_threshold_pct:
                continue

            # 2. Tính Step Cost (g)
            step_cost = 0.0
            
            if preference == "distance":
                step_cost = dist_km
            elif preference == "time":
                step_cost = dist_km / vehicle.speed 
            elif preference == "cost":
                step_cost = 0.0 

            tentative_g = g_curr + step_cost
            
            if tentative_g < g_score.get(neighbor, float('inf')):
                g_score[neighbor] = tentative_g
                parent[neighbor] = current
                
                h_val = calculate_heuristic(G, neighbor, goal, vehicle, preference, new_batt_pct)
                
                f_val = tentative_g + h_val
                heapq.heappush(open_set, (f_val, next(counter), neighbor, tentative_g, new_batt_pct))

    return None


def _get_station_access_node(G: Any, station_obj: ChargingStation) -> int:
    """
    Tìm Node ID gần nhất trên đồ thị giao thông cho trạm sạc (Snapping).
    Sử dụng 'access_node_id' để cache kết quả.
    """
    # 1. Kiểm tra cache
    if hasattr(station_obj, 'access_node_id') and station_obj.access_node_id is not None:
        return station_obj.access_node_id
        
    try:
        lng = station_obj.coords.lng
        lat = station_obj.coords.lat
        
        node_id = ox.nearest_nodes(G, lng, lat)
        
        station_obj.access_node_id = node_id 
        return node_id
        
    except AttributeError:
        print(f"[ERROR] Station object {station_obj.id if hasattr(station_obj, 'id') else 'unknown'} missing coordinates.")
        return None
    except Exception as e:
        print(f"[WARN] Failed to snap station to graph. Error: {e}")
        return None

def _filter_candidates_with_index(G, current_node, goal_node, vehicle, station_index, current_battery_pct):
    current_kwh = (current_battery_pct / 100.0) * vehicle.batteryCapacity
    range_km = (current_kwh / vehicle.consumptionRate) * 100 * 0.95
    range_deg = range_km / 111.0 
    
    curr_y, curr_x = G.nodes[current_node]['y'], G.nodes[current_node]['x']
    goal_y, goal_x = G.nodes[goal_node]['y'], G.nodes[goal_node]['x']
    
    if not station_index.tree: return []
    indices = station_index.tree.query_ball_point([curr_y, curr_x], r=range_deg)
    
    candidates = []
    dist_to_goal_km = ox.distance.great_circle(curr_y, curr_x, goal_y, goal_x) / 1000.0
    
    for idx in indices:
        station = station_index.stations[idx]
        st_lat, st_lng = station.coords.lat, station.coords.lng
        d_curr_st = ox.distance.great_circle(curr_y, curr_x, st_lat, st_lng) / 1000.0
        d_st_goal = ox.distance.great_circle(st_lat, st_lng, goal_y, goal_x) / 1000.0
        
        # Ellipse Filter
        detour = d_curr_st + d_st_goal
        if (detour > dist_to_goal_km * 1.5) and (detour > dist_to_goal_km + 30):
            continue
        candidates.append((detour, station))
        
    candidates.sort(key=lambda x: x[0])
    return [c[1] for c in candidates[:15]]


def _plan_rescue_route(
    adj, G, current_node, vehicle, station_index, full_path_ids, total_stats, preference
):

    curr_y, curr_x = G.nodes[current_node]['y'], G.nodes[current_node]['x']
    
    _, nearest_st = station_index.find_nearest(curr_y, curr_x)
    
    if not nearest_st:
        return {
            "type": "FATAL", "feasible": False, 
            "message": "Không tìm thấy bất kỳ trạm sạc nào trên bản đồ."
        }
    
    rescue_st_node = _get_station_access_node(G, nearest_st)
    if not rescue_st_node:
         return {"type": "FATAL", "feasible": False, "message": "Trạm gần nhất bị lỗi tọa độ."}

    fake_batt_pct = 100.0
    rescue_leg = _segment_a_star(adj, G, current_node, rescue_st_node, vehicle, fake_batt_pct, preference)
    
    if rescue_leg:
        # Merge Path
        path_segment = rescue_leg["path"][1:] if full_path_ids else rescue_leg["path"]
        full_path_ids.extend(path_segment)
        
        # Merge Stats 
        val = rescue_leg["g_score"]
        if preference == "time": total_stats["travel_time"] += val
        elif preference == "distance": total_stats["distance"] += val
        
        return {
            "type": "RESCUE", 
            "feasible": False,
            "path": full_path_ids, 
            "stats": total_stats,
            "final_battery_pct": 0.0, # Về 0
            "message": f"Hết pin! Đây là đường cứu hộ tới trạm gần nhất: {nearest_st.name}"
        }
    else:
        return {
            "type": "NO_PATH", "feasible": False, 
            "message": "Xe kẹt ở vị trí cô lập, không thể kéo tới trạm gần nhất."
        }


def find_ev_route_multistop(
    adj: Dict[int, List[Tuple[int, float]]],
    G: Any,
    start: int,
    goal: int,
    vehicle: VehicleOptions,
    station_index: StationIndex, 
    preference: str = "time"
):
    full_path_ids = []
    total_stats = {
        "travel_time": 0.0, "distance": 0.0, "cost": 0.0,
        "charge_count": 0, "charging_time": 0.0, "charging_logs": []
    }
    
    current_node = start
    # Input %
    current_battery_pct = vehicle.batteryLevel
    if current_battery_pct > 100: current_battery_pct = 100.0
    
    stop_counter = 0
    safety_threshold_pct = vehicle.safetyThreshold

    while True:
        print(f"\n[Hop {stop_counter}] Node {current_node} | Batt: {current_battery_pct:.1f}%")
        
        # 1. Thử đi thẳng
        direct_try = _segment_a_star(adj, G, current_node, goal, vehicle, current_battery_pct, preference)
        
        if direct_try and direct_try["final_battery_pct"] >= safety_threshold_pct:
            print("=> SUCCESS: Reached Goal!")
            path = direct_try["path"] if stop_counter == 0 else direct_try["path"][1:]
            full_path_ids.extend(path)
            
            val = direct_try["g_score"]
            if preference == "time": total_stats["travel_time"] += val
            elif preference == "distance": total_stats["distance"] += val
            elif preference == "cost": total_stats["cost"] += 0 
            
            return {
                "type": "SUCCESS", "feasible": True, 
                "path": full_path_ids, "stats": total_stats,
                "final_battery_pct": round(direct_try["final_battery_pct"], 1)
            }

        candidates = _filter_candidates_with_index(G, current_node, goal, vehicle, station_index, current_battery_pct)
        
        if not candidates:
            print("=> STRANDED (No candidates). Initiating Rescue Plan...")
            return _plan_rescue_route(
                adj, G, current_node, vehicle, station_index, full_path_ids, total_stats, preference
            )
            
        best_hop = None
        best_total_score = float('inf')
        
        for station in candidates:
            st_node = _get_station_access_node(G, station)
            if st_node is None or st_node == current_node: continue
            
            leg = _segment_a_star(adj, G, current_node, st_node, vehicle, current_battery_pct, preference)
            if not leg: continue
            
            target_pct = 80.0
            h_future = calculate_heuristic(G, st_node, goal, vehicle, preference, target_pct)
            
            score = leg["g_score"] + h_future
            
            if score < best_total_score:
                best_total_score = score
                best_hop = {"station": station, "node": st_node, "leg": leg}
        
        if not best_hop:
             print("=> STRANDED (Candidates unreachable). Initiating Rescue Plan...")
             return _plan_rescue_route(
                adj, G, current_node, vehicle, station_index, full_path_ids, total_stats, preference
            )
            
        chosen_st = best_hop["station"]
        leg_res = best_hop["leg"]
        path = leg_res["path"] if stop_counter == 0 else leg_res["path"][1:]
        full_path_ids.extend(path)
        
        val = leg_res["g_score"]
        if preference == "time": total_stats["travel_time"] += val
        elif preference == "distance": total_stats["distance"] += val
        
        # Sạc
        arrival_pct = leg_res["final_battery_pct"]
        target_pct = 80.0 
        pct_needed = max(0.0, target_pct - arrival_pct)
        kwh_needed = (pct_needed / 100.0) * vehicle.batteryCapacity
        
        t_chg = kwh_needed / getattr(chosen_st, 'power_kw', 60.0)
        c_chg = kwh_needed * getattr(chosen_st, 'price_per_kwh', 3000)
        
        total_stats["charge_count"] += 1
        total_stats["charging_time"] += t_chg
        total_stats["cost"] += c_chg 
        
        total_stats["charging_logs"].append({
            "stop": stop_counter+1, "station": chosen_st.name, 
            "kwh": round(kwh_needed, 2), "time": round(t_chg, 2), "cost": round(c_chg, 0)
        })
        
        current_node = best_hop["node"]
        current_battery_pct = target_pct 
        stop_counter += 1
        
    return {"type": "FAIL", "feasible": False, "message": "Loop limit reached."}