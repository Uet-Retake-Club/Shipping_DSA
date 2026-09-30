"""
Dataset Generator & Geo-distance Utilities for Smart Delivery Network.
Hỗ trợ tính toán khoảng cách thực tế (Haversine Formula) giữa các tọa độ GPS,
đọc/ghi dữ liệu CSV & JSON cho mô hình mạng lưới logistics.
"""

import csv
import json
import math
from typing import Dict, List, Optional, Tuple


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Tính khoảng cách mặt cầu (Haversine formula) giữa 2 tọa độ GPS (km).

    Args:
        lat1, lon1: Vĩ độ và kinh độ điểm 1 (degrees)
        lat2, lon2: Vĩ độ và kinh độ điểm 2 (degrees)

    Returns:
        Khoảng cách tính theo kilometer (km), làm tròn 2 chữ số thập phân.
    """
    R = 6371.0  # Bán kính Trái Đất (km)

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_phi / 2.0) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    )
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return round(R * c, 2)


def euclidean_distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """Tính khoảng cách Euclid 2D trên hệ tọa độ trực giao."""
    return round(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2), 2)


def load_nodes_csv(filepath: str) -> List[Dict]:
    """Đọc danh sách các nút từ file CSV."""
    nodes = []
    with open(filepath, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            node = {
                "id": row["id"],
                "name": row["name"],
                "type": row["type"],
                "x": float(row["x"]) if row.get("x") else 0.0,
                "y": float(row["y"]) if row.get("y") else 0.0,
                "lat": float(row["lat"]) if row.get("lat") else None,
                "lon": float(row["lon"]) if row.get("lon") else None,
            }
            nodes.append(node)
    return nodes


def load_edges_csv(filepath: str) -> List[Dict]:
    """Đọc danh sách các cạnh từ file CSV."""
    edges = []
    with open(filepath, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            edges.append({
                "u": row["u"],
                "v": row["v"],
                "weight": float(row["weight"]),
                "road_type": row.get("road_type", "urban"),
            })
    return edges


def save_network_json(
    nodes: List[Dict],
    edges: List[Dict],
    filepath: str,
    network_name: str = "Logistics_Network",
    description: str = "",
) -> None:
    """Xuất mạng lưới gồm nodes và edges ra định dạng JSON chuẩn."""
    data = {
        "network_name": network_name,
        "description": description,
        "num_nodes": len(nodes),
        "num_edges": len(edges),
        "nodes": nodes,
        "edges": edges,
    }
    with open(filepath, mode="w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def generate_knn_edges(
    nodes: List[Dict],
    k: int = 3,
    road_factor: float = 1.25,
) -> List[Dict]:
    """
    Tự động sinh các cạnh kết nối dựa trên k láng giềng gần nhất (k-Nearest Neighbors).

    Args:
        nodes: Danh sách các nodes có lat/lon hoặc x/y.
        k: Số lượng láng giềng kết nối tối thiểu cho mỗi nút.
        road_factor: Hệ số uốn lượn đường bộ so với đường chim bay (mặc định 1.25x).

    Returns:
        Danh sách cạnh vô hướng (u, v, weight, road_type).
    """
    edges_set = set()
    edges = []

    for i, u in enumerate(nodes):
        distances = []
        for j, v in enumerate(nodes):
            if i == j:
                continue

            # Ưu tiên tính theo GPS Haversine nếu có, ngược lại tính Euclid
            if u.get("lat") is not None and v.get("lat") is not None:
                dist = haversine_distance(u["lat"], u["lon"], v["lat"], v["lon"])
            else:
                dist = euclidean_distance(u["x"], u["y"], v["x"], v["y"])

            # Nhân hệ số uốn lượn đường thực tế
            actual_dist = round(dist * road_factor, 2)
            distances.append((actual_dist, v["id"]))

        # Sắp xếp lấy k láng giềng gần nhất
        distances.sort(key=lambda item: item[0])
        for dist, neighbor_id in distances[:k]:
            edge_key = tuple(sorted([u["id"], neighbor_id]))
            if edge_key not in edges_set:
                edges_set.add(edge_key)

                # Phân loại loại đường theo khoảng cách
                if dist > 15.0:
                    road_type = "highway"
                elif dist > 7.0:
                    road_type = "arterial"
                else:
                    road_type = "urban"

                edges.append({
                    "u": edge_key[0],
                    "v": edge_key[1],
                    "weight": dist,
                    "road_type": road_type,
                })

    return edges


if __name__ == "__main__":
    import os

    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    nodes_csv = os.path.join(base_dir, "data", "reallife_data", "hanoi_nodes.csv")

    if os.path.exists(nodes_csv):
        hanoi_nodes = load_nodes_csv(nodes_csv)
        print(f"Loaded {len(hanoi_nodes)} Hanoi nodes successfully.")

        # Test Haversine distance between Long Bien Mega SOC (H01) and Hoan Kiem Post Office (D01)
        h01 = next(n for n in hanoi_nodes if n["id"] == "H01")
        d01 = next(n for n in hanoi_nodes if n["id"] == "D01")
        dist = haversine_distance(h01["lat"], h01["lon"], d01["lat"], d01["lon"])
        print(f"Distance (Haversine) H01 <-> D01: {dist} km")
