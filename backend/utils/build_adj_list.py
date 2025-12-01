from typing import Dict, List, Tuple, Optional

def build_adj_list(G, filters: Optional[Dict[str, bool]] = None) -> Dict[int, List[Tuple[int, float]]]:
    adj = {u: [] for u in G.nodes}
    for u, v, key, data in G.edges(keys=True, data=True):
        length = data.get("length", 0.0)
        if filters:
            if filters.get("avoidHighway") and data.get("highway") in ["motorway", "trunk"]:
                length *= 10
            if filters.get("avoidToll") and data.get("toll"):
                length *= 10
        adj[u].append((v, length))
    return adj