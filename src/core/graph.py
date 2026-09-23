"""
Core Graph Module for Smart Delivery Network Design (MST).
Provides data structures for representing logistics locations (Nodes),
connecting candidate routes (Edges), and the overall Network (Graph).
Supports both Edge List (for Kruskal) and Adjacency List (for Prim).
"""

from __future__ import annotations
import csv
import json
import math
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Generator, List, Optional, Set, Tuple


class NodeType(str, Enum):
    HUB = "hub"  # Central Distribution Hub
    WAREHOUSE = "warehouse"  # Regional Warehouse
    DELIVERY_POINT = "delivery_point"  # Local delivery station / drop-off point
    UNKNOWN = "unknown"

    @classmethod
    def from_str(cls, val: Optional[str]) -> NodeType:
        if not val:
            return cls.UNKNOWN
        clean = val.strip().lower()
        for member in cls:
            if member.value == clean:
                return member
        return cls.UNKNOWN


@dataclass
class Node:
    """Represents a physical logistics facility or delivery location."""
    id: str
    name: str = ""
    node_type: NodeType = NodeType.DELIVERY_POINT
    x: float = 0.0
    y: float = 0.0
    lat: Optional[float] = None
    lon: Optional[float] = None

    def __post_init__(self):
        if not self.name:
            self.name = f"Location {self.id}"
        if isinstance(self.node_type, str):
            self.node_type = NodeType.from_str(self.node_type)

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            "id": self.id,
            "name": self.name,
            "type": self.node_type.value,
            "x": self.x,
            "y": self.y,
        }
        if self.lat is not None:
            data["lat"] = self.lat
        if self.lon is not None:
            data["lon"] = self.lon
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Node:
        return cls(
            id=str(data["id"]),
            name=str(data.get("name", "")),
            node_type=NodeType.from_str(data.get("type")),
            x=float(data.get("x", 0.0)),
            y=float(data.get("y", 0.0)),
            lat=float(data["lat"]) if "lat" in data and data["lat"] is not None else None,
            lon=float(data["lon"]) if "lon" in data and data["lon"] is not None else None,
        )


@dataclass(order=True)
class Edge:
    """Represents a potential or selected transportation link between two nodes."""
    # sort_index allows natural sorting by weight, then u, then v for deterministic ordering
    sort_index: Tuple[float, str, str] = field(init=False, repr=False)
    u: str
    v: str
    weight: float
    road_type: str = "urban"

    def __post_init__(self):
        # Normalize undirected edge (u <= v lexicographically) for consistent hashing/equality
        u_norm, v_norm = (self.u, self.v) if str(self.u) <= str(self.v) else (self.v, self.u)
        object.__setattr__(self, 'u', str(u_norm))
        object.__setattr__(self, 'v', str(v_norm))
        object.__setattr__(self, 'weight', float(self.weight))
        object.__setattr__(self, 'sort_index', (self.weight, self.u, self.v))

    def other(self, node_id: str) -> str:
        """Given one endpoint of this edge, returns the other endpoint."""
        if node_id == self.u:
            return self.v
        if node_id == self.v:
            return self.u
        raise ValueError(f"Node {node_id} is not an endpoint of edge ({self.u}, {self.v})")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "u": self.u,
            "v": self.v,
            "weight": round(self.weight, 4),
            "road_type": self.road_type,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Edge:
        return cls(
            u=str(data["u"]),
            v=str(data["v"]),
            weight=float(data["weight"]),
            road_type=str(data.get("road_type", "urban")),
        )


class Graph:
    """
    Undirected, weighted graph representing the shipping and delivery network.
    Maintains:
    - Node dictionary: id -> Node
    - Edge List: List of Edge objects (ideal for Kruskal's algorithm)
    - Adjacency List: node_id -> list of (neighbor_id, weight, edge) (ideal for Prim's algorithm)
    """

    def __init__(self, name: str = "DeliveryNetwork", description: str = ""):
        self.name = name
        self.description = description
        self.nodes: Dict[str, Node] = {}
        self.edges: List[Edge] = []
        self._edge_set: Set[Tuple[str, str]] = set()
        self.adj: Dict[str, List[Tuple[str, float, Edge]]] = {}

    def add_node(
        self,
        node_id: str,
        name: str = "",
        node_type: NodeType | str = NodeType.DELIVERY_POINT,
        x: float = 0.0,
        y: float = 0.0,
        lat: Optional[float] = None,
        lon: Optional[float] = None,
    ) -> Node:
        """Adds a node to the network."""
        node_id = str(node_id)
        node = Node(
            id=node_id,
            name=name,
            node_type=NodeType.from_str(node_type) if isinstance(node_type, str) else node_type,
            x=x,
            y=y,
            lat=lat,
            lon=lon,
        )
        self.nodes[node_id] = node
        if node_id not in self.adj:
            self.adj[node_id] = []
        return node

    def add_node_object(self, node: Node) -> None:
        self.nodes[node.id] = node
        if node.id not in self.adj:
            self.adj[node.id] = []

    def add_edge(
        self,
        u: str,
        v: str,
        weight: float,
        road_type: str = "urban",
    ) -> Optional[Edge]:
        """
        Adds an undirected edge between u and v with given weight.
        Both u and v must be present in the graph.
        Self-loops are ignored.
        Duplicate edges keep the minimum weight.
        """
        u_str = str(u)
        v_str = str(v)
        if u_str == v_str:
            return None  # Self-loop ignored in MST

        if u_str not in self.nodes or v_str not in self.nodes:
            raise KeyError(f"Both nodes {u_str} and {v_str} must be added before adding edge")

        edge = Edge(u=u_str, v=v_str, weight=weight, road_type=road_type)
        key = (edge.u, edge.v)

        if key in self._edge_set:
            # Check if this edge has smaller weight than previous
            for i, e in enumerate(self.edges):
                if (e.u, e.v) == key:
                    if weight < e.weight:
                        self.edges[i] = edge
                        # Rebuild adjacency for this pair
                        self._update_adj_pair(edge)
                    return edge
            return None

        self._edge_set.add(key)
        self.edges.append(edge)
        self.adj[edge.u].append((edge.v, edge.weight, edge))
        self.adj[edge.v].append((edge.u, edge.weight, edge))
        return edge

    def _update_adj_pair(self, edge: Edge):
        """Helper to update adjacency list when edge weight is replaced."""
        for endpoint, other in [(edge.u, edge.v), (edge.v, edge.u)]:
            self.adj[endpoint] = [
                (nbr, wt, e) if nbr != other else (nbr, edge.weight, edge)
                for nbr, wt, e in self.adj[endpoint]
            ]

    @property
    def num_nodes(self) -> int:
        return len(self.nodes)

    @property
    def num_edges(self) -> int:
        return len(self.edges)

    def get_neighbors(self, u: str) -> List[Tuple[str, float, Edge]]:
        """Returns adjacency list entries: (neighbor_id, weight, edge) for node u."""
        return self.adj.get(str(u), [])

    # -------------------------------------------------------------------------
    # Distance Calculations
    # -------------------------------------------------------------------------
    @staticmethod
    def euclidean_distance(n1: Node, n2: Node) -> float:
        """Calculates 2D Euclidean distance between two nodes."""
        return math.hypot(n1.x - n2.x, n1.y - n2.y)

    @staticmethod
    def haversine_distance(n1: Node, n2: Node) -> float:
        """
        Calculates Great-Circle distance in kilometers between two GPS coordinates
        using Haversine formula.
        """
        if n1.lat is None or n1.lon is None or n2.lat is None or n2.lon is None:
            raise ValueError("Both nodes must have valid latitude and longitude")

        # Earth radius in kilometers
        r = 6371.0
        phi1 = math.radians(n1.lat)
        phi2 = math.radians(n2.lat)
        delta_phi = math.radians(n2.lat - n1.lat)
        delta_lambda = math.radians(n2.lon - n1.lon)

        a = (
            math.sin(delta_phi / 2.0) ** 2
            + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
        )
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
        return r * c

    def connect_all_pairs(self, metric: str = "euclidean", cost_multiplier: float = 1.0) -> None:
        """
        Creates a complete graph (all pairs connected) using either Euclidean
        or Haversine distance as edge weights.
        """
        node_ids = list(self.nodes.keys())
        n = len(node_ids)
        for i in range(n):
            u_id = node_ids[i]
            u_node = self.nodes[u_id]
            for j in range(i + 1, n):
                v_id = node_ids[j]
                v_node = self.nodes[v_id]
                if metric == "haversine":
                    dist = self.haversine_distance(u_node, v_node)
                else:
                    dist = self.euclidean_distance(u_node, v_node)
                self.add_edge(u_id, v_id, round(dist * cost_multiplier, 4))

    # -------------------------------------------------------------------------
    # Connectivity & Component Analysis
    # -------------------------------------------------------------------------
    def get_connected_components(self) -> List[Set[str]]:
        """Finds all connected components in the graph using BFS/DFS."""
        visited: Set[str] = set()
        components: List[Set[str]] = []

        for node_id in self.nodes:
            if node_id not in visited:
                comp: Set[str] = set()
                queue = [node_id]
                visited.add(node_id)
                while queue:
                    curr = queue.pop(0)
                    comp.add(curr)
                    for nbr, _, _ in self.adj.get(curr, []):
                        if nbr not in visited:
                            visited.add(nbr)
                            queue.append(nbr)
                components.append(comp)

        return components

    def is_connected(self) -> bool:
        """Returns True if the entire graph is connected, False otherwise."""
        if not self.nodes:
            return True
        return len(self.get_connected_components()) == 1

    # -------------------------------------------------------------------------
    # Serialization / Deserialization (JSON & CSV)
    # -------------------------------------------------------------------------
    def to_dict(self) -> Dict[str, Any]:
        return {
            "network_name": self.name,
            "description": self.description,
            "num_nodes": self.num_nodes,
            "num_edges": self.num_edges,
            "nodes": [node.to_dict() for node in self.nodes.values()],
            "edges": [edge.to_dict() for edge in self.edges],
        }

    def save_json(self, filepath: str | Path) -> None:
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)

    @classmethod
    def load_json(cls, filepath: str | Path) -> Graph:
        path = Path(filepath)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        g = cls(
            name=data.get("network_name", "DeliveryNetwork"),
            description=data.get("description", ""),
        )
        for n_dict in data.get("nodes", []):
            g.add_node_object(Node.from_dict(n_dict))
        for e_dict in data.get("edges", []):
            g.add_edge(
                u=e_dict["u"],
                v=e_dict["v"],
                weight=float(e_dict["weight"]),
                road_type=e_dict.get("road_type", "urban"),
            )
        return g

    def save_csv(self, nodes_path: str | Path, edges_path: str | Path) -> None:
        n_p = Path(nodes_path)
        e_p = Path(edges_path)
        n_p.parent.mkdir(parents=True, exist_ok=True)
        e_p.parent.mkdir(parents=True, exist_ok=True)

        with open(n_p, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "name", "type", "x", "y", "lat", "lon"])
            for n in self.nodes.values():
                writer.writerow([n.id, n.name, n.node_type.value, n.x, n.y, n.lat or "", n.lon or ""])

        with open(e_p, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["u", "v", "weight", "road_type"])
            for e in self.edges:
                writer.writerow([e.u, e.v, e.weight, e.road_type])

    @classmethod
    def load_csv(cls, nodes_path: str | Path, edges_path: str | Path, name: str = "CSVNetwork") -> Graph:
        g = cls(name=name)
        with open(nodes_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                g.add_node_object(Node.from_dict(row))

        with open(edges_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                g.add_edge(
                    u=row["u"],
                    v=row["v"],
                    weight=float(row["weight"]),
                    road_type=row.get("road_type", "urban"),
                )
        return g

    def summary(self) -> str:
        comps = self.get_connected_components()
        lines = [
            f"=== Network Summary: {self.name} ===",
            f"Description: {self.description or 'N/A'}",
            f"Total Nodes: {self.num_nodes}",
            f"Total Edges: {self.num_edges}",
            f"Connected Components: {len(comps)}",
            f"Is Fully Connected: {len(comps) == 1}",
        ]
        type_counts: Dict[str, int] = {}
        for n in self.nodes.values():
            t = n.node_type.value
            type_counts[t] = type_counts.get(t, 0) + 1
        lines.append(f"Node Types Breakdown: {type_counts}")
        return "\n".join(lines)
