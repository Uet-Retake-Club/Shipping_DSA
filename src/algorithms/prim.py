"""
Prim's Algorithm for Minimum Spanning Tree (MST).
Time Complexity: O(E log V) using custom MinHeap and Adjacency List
Space Complexity: O(V + E)
Handles disconnected graphs by growing trees in each connected component (MST Forest).
"""

from __future__ import annotations
import time
from dataclasses import dataclass
from typing import List, Optional, Set, Tuple
from src.core.graph import Edge, Graph
from src.algorithms.min_heap import MinHeap


@dataclass
class PrimResult:
    """Encapsulates the output of Prim's algorithm."""
    mst_edges: List[Edge]
    total_cost: float
    num_nodes: int
    num_edges_in_mst: int
    is_connected: bool
    num_components: int
    execution_time_ms: float
    edges_considered: int


def prim_mst(graph: Graph, start_node: Optional[str] = None) -> PrimResult:
    """
    Computes the Minimum Spanning Tree (or Forest) using Prim's algorithm.

    Steps:
    1. Maintain a set `visited` of nodes already included in the MST.
    2. Maintain custom `MinHeap` storing tuples: (weight, u, v, edge)
       where u in visited, v not in visited.
    3. Iterate across all nodes so that if graph is disconnected,
       Prim continues on each unvisited component (building an MST Forest).
    4. In each step, extract min edge from MinHeap. If target node already visited, discard.
       Otherwise, include edge in MST, mark target visited, and push all its outgoing
       edges to unvisited neighbors into MinHeap.

    Returns PrimResult.
    """
    start_time = time.perf_counter()

    if graph.num_nodes == 0:
        return PrimResult(
            mst_edges=[],
            total_cost=0.0,
            num_nodes=0,
            num_edges_in_mst=0,
            is_connected=True,
            num_components=0,
            execution_time_ms=0.0,
            edges_considered=0,
        )

    visited: Set[str] = set()
    mst_edges: List[Edge] = []
    total_cost: float = 0.0
    edges_considered: int = 0
    num_components: int = 0

    heap: MinHeap[Tuple[float, str, str, Edge]] = MinHeap()

    # Determine node iteration order: start with start_node if given
    all_node_keys = list(graph.nodes.keys())
    if start_node is not None and str(start_node) in graph.nodes:
        all_node_keys.remove(str(start_node))
        all_node_keys.insert(0, str(start_node))

    # Process all components
    for initial_node in all_node_keys:
        if initial_node in visited:
            continue

        num_components += 1
        visited.add(initial_node)

        # Push all edges incident to initial_node into heap
        for nbr, wt, edge in graph.get_neighbors(initial_node):
            if nbr not in visited:
                # Store (weight, u, v, edge)
                heap.push((wt, initial_node, nbr, edge))

        while not heap.is_empty():
            wt, u, v, edge = heap.pop()
            edges_considered += 1

            if v in visited:
                continue

            # Add to MST
            visited.add(v)
            mst_edges.append(edge)
            total_cost += wt

            # Push incident edges of the newly added node v
            for nbr, next_wt, next_edge in graph.get_neighbors(v):
                if nbr not in visited:
                    heap.push((next_wt, v, nbr, next_edge))

    end_time = time.perf_counter()
    execution_time_ms = (end_time - start_time) * 1000.0

    is_connected = (num_components <= 1)

    return PrimResult(
        mst_edges=mst_edges,
        total_cost=round(total_cost, 4),
        num_nodes=graph.num_nodes,
        num_edges_in_mst=len(mst_edges),
        is_connected=is_connected,
        num_components=num_components,
        execution_time_ms=round(execution_time_ms, 4),
        edges_considered=edges_considered,
    )
