"""
Unit tests for Kruskal's algorithm.
Compatible with standard library unittest and pytest.
"""

import unittest
from src.core.graph import Graph
from src.algorithms.kruskal import kruskal_mst


class TestKruskal(unittest.TestCase):
    def test_kruskal_triangle(self):
        g = Graph("Triangle")
        g.add_node("A")
        g.add_node("B")
        g.add_node("C")
        g.add_edge("A", "B", 1.0)
        g.add_edge("B", "C", 2.0)
        g.add_edge("A", "C", 3.0)

        res = kruskal_mst(g)
        self.assertTrue(res.is_connected)
        self.assertEqual(res.num_edges_in_mst, 2)
        self.assertAlmostEqual(res.total_cost, 3.0)

    def test_kruskal_disconnected_forest(self):
        g = Graph("Disconnected")
        g.add_node("A")
        g.add_node("B")
        g.add_node("C")
        g.add_node("D")
        g.add_edge("A", "B", 4.0)
        g.add_edge("C", "D", 5.0)

        res = kruskal_mst(g)
        self.assertFalse(res.is_connected)
        self.assertEqual(res.num_components, 2)
        self.assertEqual(res.num_edges_in_mst, 2)
        self.assertAlmostEqual(res.total_cost, 9.0)

    def test_kruskal_empty_and_single(self):
        empty_g = Graph("Empty")
        res_empty = kruskal_mst(empty_g)
        self.assertEqual(res_empty.num_edges_in_mst, 0)
        self.assertEqual(res_empty.total_cost, 0.0)

        single_g = Graph("Single")
        single_g.add_node("A")
        res_single = kruskal_mst(single_g)
        self.assertEqual(res_single.num_edges_in_mst, 0)
        self.assertEqual(res_single.total_cost, 0.0)
        self.assertTrue(res_single.is_connected)


if __name__ == "__main__":
    unittest.main()
