"""
Kruskal's Algorithm for Minimum Spanning Tree (MST).
Time Complexity: O(E log E) = O(E log V)
Space Complexity: O(V + E)
Uses custom DisjointSetUnion (DSU) to avoid cycles.
Handles disconnected graphs gracefully by producing an MST Forest.
"""

from __future__ import annotations
import time
from dataclasses import dataclass, field
from typing import List, Tuple
from src.core.graph import Edge, Graph
from src.algorithms.dsu import DisjointSetUnion


@dataclass
class KruskalResult:
    """Encapsulates the output of Kruskal's algorithm."""
    mst_edges: List[Edge]
    total_cost: float
    num_nodes: int
    num_edges_in_mst: int
    is_connected: bool
    num_components: int
    execution_time_ms: float
    edges_considered: int


def kruskal_mst(graph: Graph) -> KruskalResult:
    """
    Computes the Minimum Spanning Tree (or Forest) using Kruskal's algorithm.

    Steps:
    1. Initialize DSU with all nodes in the graph.
    2. Sort all candidate edges in ascending order of weight (with deterministic tie-breaking).
    3. For each edge (u, v, w):
       - If u and v belong to different disjoint sets, merge them and add edge to MST.
       - If they are in the same set, discard edge (cycle detected).
    4. Stop early if we have selected (V - 1) edges in a connected graph.

    Returns KruskalResult.
    """
    start_time = time.perf_counter()

    if graph.num_nodes == 0:
        return KruskalResult(
            mst_edges=[],
            total_cost=0.0,
            num_nodes=0,
            num_edges_in_mst=0,
            is_connected=True,
            num_components=0,
            execution_time_ms=0.0,
            edges_considered=0,
        )

    # 1. Initialize DSU
    dsu = DisjointSetUnion(graph.nodes.keys())

    # 2. Sort edges by weight, then u, then v (Edge.__post_init__ ensures natural sorting)
    sorted_edges = sorted(graph.edges)

    mst_edges: List[Edge] = []
    total_cost: float = 0.0
    edges_considered: int = 0
    target_edges = graph.num_nodes - 1

    # 3. Greedy selection
    for edge in sorted_edges:
        edges_considered += 1
        if dsu.union(edge.u, edge.v):
            mst_edges.append(edge)
            total_cost += edge.weight
            if len(mst_edges) == target_edges:
                break

    end_time = time.perf_counter()
    execution_time_ms = (end_time - start_time) * 1000.0

    num_components = dsu.num_sets
    is_connected = (num_components <= 1)

    return KruskalResult(
        mst_edges=mst_edges,
        total_cost=round(total_cost, 4),
        num_nodes=graph.num_nodes,
        num_edges_in_mst=len(mst_edges),
        is_connected=is_connected,
        num_components=num_components,
        execution_time_ms=round(execution_time_ms, 4),
        edges_considered=edges_considered,
    )
