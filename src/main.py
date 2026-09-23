"""
Main CLI Application for Smart Delivery Network Design (MST).
Allows running and comparing Kruskal and Prim algorithms on logistics datasets.
"""

from __future__ import annotations
import argparse
import sys
from pathlib import Path

# Ensure project root is in sys.path for direct script execution
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Ensure UTF-8 console output
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from src.core.graph import Graph
from src.algorithms.kruskal import kruskal_mst
from src.algorithms.prim import prim_mst
from src.generators.dataset_generator import create_small_network


def format_currency_cost(cost: float) -> str:
    """Formats cost in a standard logistics financial representation."""
    return f"${cost:,.2f}"


def run_pipeline(graph: Graph, verbose: bool = False) -> None:
    print("\n" + "=" * 70)
    print(f" LOGISTICS NETWORK MST OPTIMIZATION: {graph.name}")
    print("=" * 70)
    print(graph.summary())
    print("-" * 70)

    # 1. Run Kruskal
    kruskal_res = kruskal_mst(graph)

    # 2. Run Prim
    prim_res = prim_mst(graph)

    # Output Comparison
    print("\n ALGORITHM PERFORMANCE & COST COMPARISON:")
    print("-" * 70)
    print(f"{'Metric':<30} | {'Kruskal (DSU)':<18} | {'Prim (Min-Heap)':<18}")
    print("-" * 70)
    print(f"{'Total MST Cost':<30} | {format_currency_cost(kruskal_res.total_cost):<18} | {format_currency_cost(prim_res.total_cost):<18}")
    print(f"{'Edges Selected':<30} | {kruskal_res.num_edges_in_mst:<18} | {prim_res.num_edges_in_mst:<18}")
    print(f"{'Target Edges (V - 1)':<30} | {graph.num_nodes - 1:<18} | {graph.num_nodes - 1:<18}")
    print(f"{'Connected Components':<30} | {kruskal_res.num_components:<18} | {prim_res.num_components:<18}")
    print(f"{'Is Network Fully Connected':<30} | {str(kruskal_res.is_connected):<18} | {str(prim_res.is_connected):<18}")
    print(f"{'Edges Inspected/Pushed':<30} | {kruskal_res.edges_considered:<18} | {prim_res.edges_considered:<18}")
    print(f"{'Execution Time (ms)':<30} | {kruskal_res.execution_time_ms:<18.4f} | {prim_res.execution_time_ms:<18.4f}")
    print("-" * 70)

    # Verification
    cost_diff = abs(kruskal_res.total_cost - prim_res.total_cost)
    if cost_diff < 1e-4:
        print("[PASS] VERIFICATION SUCCESS: Both algorithms produced identical minimum cost!")
    else:
        print(f"[FAIL] VERIFICATION WARNING: Cost mismatch! Difference = {cost_diff}")

    if not kruskal_res.is_connected:
        print("[WARNING] The input graph is disconnected! An MST Forest was computed.")

    if verbose:
        print("\n SELECTED BACKBONE INFRASTRUCTURE ROUTES (Kruskal):")
        print("-" * 70)
        for i, edge in enumerate(kruskal_res.mst_edges, 1):
            u_node = graph.nodes[edge.u]
            v_node = graph.nodes[edge.v]
            print(f"  {i:>2}. [{edge.u}] ({u_node.name}) <---> [{edge.v}] ({v_node.name}) | Cost: {edge.weight:8.2f} | Type: {edge.road_type}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Smart Delivery Network Design using Minimum Spanning Tree (MST)"
    )
    parser.add_argument(
        "--data",
        "-d",
        type=str,
        default=None,
        help="Path to graph dataset JSON file (e.g., data/sample_small_10_nodes.json)",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Display detailed list of chosen edges in the MST",
    )

    args = parser.parse_args()

    if args.data:
        data_path = Path(args.data)
        if not data_path.exists():
            print(f"Error: File {data_path} not found.")
            sys.exit(1)
        graph = Graph.load_json(data_path)
    else:
        print("No dataset specified. Loading default small 10-node network...")
        default_json = Path("data/sample_small_10_nodes.json")
        if default_json.exists():
            graph = Graph.load_json(default_json)
        else:
            graph = create_small_network()

    run_pipeline(graph, verbose=args.verbose)


if __name__ == "__main__":
    main()
