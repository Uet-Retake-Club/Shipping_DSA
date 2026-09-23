"""
Unit tests for Prim's algorithm and equivalence check with Kruskal's algorithm.
Compatible with standard library unittest and pytest.
"""

import unittest
from src.core.graph import Graph
from src.algorithms.kruskal import kruskal_mst
from src.algorithms.prim import prim_mst
from src.generators.dataset_generator import create_small_network


class TestPrim(unittest.TestCase):
    def test_prim_triangle(self):
        g = Graph("Triangle")
        g.add_node("A")
        g.add_node("B")
        g.add_node("C")
        g.add_edge("A", "B", 1.0)
        g.add_edge("B", "C", 2.0)
        g.add_edge("A", "C", 3.0)

        res_a = prim_mst(g, start_node="A")
        res_b = prim_mst(g, start_node="B")
        res_c = prim_mst(g, start_node="C")

        self.assertAlmostEqual(res_a.total_cost, 3.0)
        self.assertAlmostEqual(res_b.total_cost, 3.0)
        self.assertAlmostEqual(res_c.total_cost, 3.0)
        self.assertEqual(res_a.num_edges_in_mst, 2)

    def test_prim_disconnected_forest(self):
        g = Graph("Disconnected")
        g.add_node("A")
        g.add_node("B")
        g.add_node("C")
        g.add_node("D")
        g.add_edge("A", "B", 4.0)
        g.add_edge("C", "D", 5.0)

        res = prim_mst(g)
        self.assertFalse(res.is_connected)
        self.assertEqual(res.num_components, 2)
        self.assertEqual(res.num_edges_in_mst, 2)
        self.assertAlmostEqual(res.total_cost, 9.0)

    def test_kruskal_prim_agreement_small_network(self):
        g = create_small_network()
        k_res = kruskal_mst(g)
        p_res = prim_mst(g)

        self.assertAlmostEqual(k_res.total_cost, p_res.total_cost, places=4)
        self.assertEqual(k_res.num_edges_in_mst, p_res.num_edges_in_mst)
        self.assertEqual(k_res.is_connected, p_res.is_connected)


if __name__ == "__main__":
    unittest.main()
