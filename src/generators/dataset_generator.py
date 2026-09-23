"""
Dataset Generator for Logistics Delivery Networks.
Provides:
1. create_small_network(): Manual 10-node network (1 Hub, 3 Warehouses, 6 Delivery Points).
2. generate_clustered_network(): Clustered spatial network mimicking urban/suburban logistics.
3. generate_benchmark_datasets(): Generates small, medium, and large datasets (10, 50, 500 nodes).
"""

from __future__ import annotations
import math
import random
import sys
from pathlib import Path
from typing import List, Tuple

# Ensure project root is in sys.path for direct script execution
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.core.graph import Graph, Node, NodeType

# Ensure safe console output on Windows platforms
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def create_small_network() -> Graph:
    """
    Creates a curated 10-node logistics network representing a metropolitan delivery system:
    - 1 Central Distribution Hub (H0)
    - 3 Regional Warehouses (W1, W2, W3)
    - 6 Local Delivery Stations (D1 to D6)
    """
    g = Graph(
        name="Metro_Logistics_Small_10",
        description="Sample metropolitan logistics network with 1 Central Hub, 3 Warehouses, and 6 Delivery Stations",
    )


    # 1 Hub (Central)
    g.add_node("H0", "Central Hub (Long Bien)", NodeType.HUB, x=50.0, y=50.0, lat=21.037, lon=105.890)

    # 3 Warehouses (North, West, South)
    g.add_node("W1", "North Warehouse (Dong Anh)", NodeType.WAREHOUSE, x=50.0, y=85.0, lat=21.137, lon=105.850)
    g.add_node("W2", "West Warehouse (Cau Giay)", NodeType.WAREHOUSE, x=15.0, y=50.0, lat=21.033, lon=105.795)
    g.add_node("W3", "South Warehouse (Hoang Mai)", NodeType.WAREHOUSE, x=60.0, y=15.0, lat=20.970, lon=105.860)

    # 6 Delivery Points
    g.add_node("D1", "Station Soc Son", NodeType.DELIVERY_POINT, x=45.0, y=105.0, lat=21.260, lon=105.830)
    g.add_node("D2", "Station Me Linh", NodeType.DELIVERY_POINT, x=75.0, y=90.0, lat=21.170, lon=105.720)
    g.add_node("D3", "Station Nam Tu Liem", NodeType.DELIVERY_POINT, x=5.0, y=60.0, lat=21.010, lon=105.760)
    g.add_node("D4", "Station Ha Dong", NodeType.DELIVERY_POINT, x=10.0, y=30.0, lat=20.970, lon=105.770)
    g.add_node("D5", "Station Thanh Tri", NodeType.DELIVERY_POINT, x=55.0, y=0.0, lat=20.930, lon=105.840)
    g.add_node("D6", "Station Gia Lam", NodeType.DELIVERY_POINT, x=85.0, y=45.0, lat=21.020, lon=105.930)

    # Predefined candidate roads with Euclidean-based costs rounded
    roads: List[Tuple[str, str, str]] = [
        # Hub connections to Warehouses
        ("H0", "W1", "highway"),
        ("H0", "W2", "highway"),
        ("H0", "W3", "highway"),
        ("W1", "W2", "arterial"),
        ("W2", "W3", "arterial"),
        # Warehouse 1 to Northern delivery stations
        ("W1", "D1", "arterial"),
        ("W1", "D2", "urban"),
        ("D1", "D2", "urban"),
        # Warehouse 2 to Western delivery stations
        ("W2", "D3", "urban"),
        ("W2", "D4", "arterial"),
        ("D3", "D4", "urban"),
        # Warehouse 3 to Southern delivery stations
        ("W3", "D5", "arterial"),
        ("W3", "D6", "urban"),
        ("H0", "D6", "arterial"),
        # Cross-connections (alternate candidate routes)
        ("D4", "W3", "urban"),
        ("W1", "D6", "urban"),
    ]

    for u, v, rtype in roads:
        n1 = g.nodes[u]
        n2 = g.nodes[v]
        dist = round(g.euclidean_distance(n1, n2), 2)
        # Factor cost by road type
        cost_multiplier = 1.0 if rtype == "highway" else (1.2 if rtype == "arterial" else 1.5)
        weight = round(dist * cost_multiplier, 2)
        g.add_edge(u, v, weight, road_type=rtype)

    return g


def generate_clustered_network(
    num_nodes: int,
    num_clusters: int = 3,
    area_size: float = 1000.0,
    k_neighbors: int = 4,
    random_seed: int = 42,
    name: str = "Clustered_Logistics_Network",
    disconnected: bool = False,
) -> Graph:
    """
    Generates a realistic spatial logistics network:
    - Nodes are grouped into geographic clusters (representing urban zones).
    - Edges are created between each node and its k-nearest neighbors to ensure
      realistic road topology (sparse graph).
    - Clusters are bridged together through their regional hubs (unless disconnected=True).
    """
    rng = random.Random(random_seed)
    g = Graph(name=name, description=f"Synthetic clustered delivery network with {num_nodes} nodes")

    # Generate Cluster Centers (Hub locations)
    cluster_centers: List[Tuple[float, float]] = []
    margin = area_size * 0.15
    for _ in range(num_clusters):
        cx = rng.uniform(margin, area_size - margin)
        cy = rng.uniform(margin, area_size - margin)
        cluster_centers.append((cx, cy))

    # Assign nodes to clusters
    nodes_per_cluster = num_nodes // num_clusters
    remainder = num_nodes % num_clusters

    created_nodes: List[Node] = []
    current_idx = 0

    for c_id, (cx, cy) in enumerate(cluster_centers):
        count = nodes_per_cluster + (1 if c_id < remainder else 0)
        cluster_std = area_size / (num_clusters * 3.5)

        for i in range(count):
            node_id = f"N{current_idx}"
            current_idx += 1

            # First node in cluster is Hub, second is Warehouse, rest are Delivery Points
            if i == 0:
                ntype = NodeType.HUB
                name_str = f"Hub_C{c_id}"
                x, y = cx, cy
            elif i == 1 and count > 3:
                ntype = NodeType.WAREHOUSE
                name_str = f"Warehouse_C{c_id}"
                x = cx + rng.gauss(0, cluster_std * 0.5)
                y = cy + rng.gauss(0, cluster_std * 0.5)
            else:
                ntype = NodeType.DELIVERY_POINT
                name_str = f"DeliveryPoint_{node_id}"
                x = cx + rng.gauss(0, cluster_std)
                y = cy + rng.gauss(0, cluster_std)

            # Clamp coordinates inside boundary
            x = max(0.0, min(area_size, x))
            y = max(0.0, min(area_size, y))

            node = g.add_node(node_id, name=name_str, node_type=ntype, x=round(x, 2), y=round(y, 2))
            created_nodes.append(node)

    # Connect k-nearest neighbors within the network to form realistic roads
    for i, u_node in enumerate(created_nodes):
        # Find distances to all other nodes
        dists = []
        for j, v_node in enumerate(created_nodes):
            if i != j:
                d = g.euclidean_distance(u_node, v_node)
                dists.append((d, v_node.id))
        dists.sort(key=lambda item: item[0])

        # Pick k nearest
        for d, v_id in dists[:k_neighbors]:
            g.add_edge(u_node.id, v_id, round(d, 2), road_type="arterial")

    # If connected is required and graph isn't fully connected, bridge the components
    if not disconnected:
        components = g.get_connected_components()
        while len(components) > 1:
            # Find closest pair of nodes between component 0 and any other component
            comp_a = components[0]
            best_dist = float("inf")
            best_pair: Tuple[str, str] = ("", "")

            for comp_b in components[1:]:
                for u_id in comp_a:
                    u_node = g.nodes[u_id]
                    for v_id in comp_b:
                        v_node = g.nodes[v_id]
                        d = g.euclidean_distance(u_node, v_node)
                        if d < best_dist:
                            best_dist = d
                            best_pair = (u_id, v_id)

            if best_pair[0] and best_pair[1]:
                g.add_edge(best_pair[0], best_pair[1], round(best_dist, 2), road_type="highway")
            components = g.get_connected_components()

    return g


def generate_benchmark_datasets(output_dir: str | Path = "data") -> Tuple[Graph, Graph, Graph]:
    """
    Generates and saves the 3 official benchmark datasets to the given directory:
    - small_10_nodes (JSON & CSV)
    - medium_50_nodes (JSON & CSV)
    - large_500_nodes (JSON & CSV)
    """
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    # 1. Small Dataset (10 nodes)
    small_g = create_small_network()
    small_g.save_json(out_path / "sample_small_10_nodes.json")
    small_g.save_csv(out_path / "small_nodes.csv", out_path / "small_edges.csv")

    # 2. Medium Dataset (50 nodes)
    medium_g = generate_clustered_network(
        num_nodes=50,
        num_clusters=4,
        area_size=500.0,
        k_neighbors=4,
        random_seed=123,
        name="Regional_Logistics_Medium_50",
    )
    medium_g.save_json(out_path / "sample_medium_50_nodes.json")
    medium_g.save_csv(out_path / "medium_nodes.csv", out_path / "medium_edges.csv")

    # 3. Large Dataset (500 nodes)
    large_g = generate_clustered_network(
        num_nodes=500,
        num_clusters=10,
        area_size=2000.0,
        k_neighbors=5,
        random_seed=456,
        name="Nationwide_Logistics_Large_500",
    )
    large_g.save_json(out_path / "sample_large_500_nodes.json")
    large_g.save_csv(out_path / "large_nodes.csv", out_path / "large_edges.csv")

    return small_g, medium_g, large_g


if __name__ == "__main__":
    print("Generating datasets in data/ ...")
    s, m, l = generate_benchmark_datasets()
    print(s.summary())
    print("\n" + m.summary())
    print("\n" + l.summary())
