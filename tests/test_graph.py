"""
Unit tests for Graph, Node, and Edge models.
Compatible with standard library unittest and pytest.
"""

import tempfile
import unittest
from pathlib import Path
from src.core.graph import Graph, Node, Edge, NodeType


class TestGraphModel(unittest.TestCase):
    def test_node_creation(self):
        n = Node("H1", "Central Hub", NodeType.HUB, x=10.0, y=20.0)
        self.assertEqual(n.id, "H1")
        self.assertEqual(n.node_type, NodeType.HUB)
        self.assertEqual(n.x, 10.0)

    def test_edge_normalization(self):
        e1 = Edge("B", "A", 15.0)
        e2 = Edge("A", "B", 15.0)
        self.assertEqual(e1.u, "A")
        self.assertEqual(e1.v, "B")
        self.assertEqual(e2.u, "A")
        self.assertEqual(e2.v, "B")
        self.assertEqual(e1, e2)

    def test_graph_add_nodes_and_edges(self):
        g = Graph("TestNet")
        g.add_node("N1", "Node 1")
        g.add_node("N2", "Node 2")
        g.add_node("N3", "Node 3")

        g.add_edge("N1", "N2", 10.0)
        g.add_edge("N2", "N3", 20.0)

        self.assertEqual(g.num_nodes, 3)
        self.assertEqual(g.num_edges, 2)
        self.assertEqual(len(g.get_neighbors("N2")), 2)
        self.assertTrue(g.is_connected())

    def test_distance_calculations(self):
        g = Graph()
        n1 = g.add_node("A", x=0.0, y=0.0, lat=21.0, lon=105.0)
        n2 = g.add_node("B", x=3.0, y=4.0, lat=21.0, lon=106.0)

        euclid = g.euclidean_distance(n1, n2)
        self.assertAlmostEqual(euclid, 5.0, places=5)

        haversine = g.haversine_distance(n1, n2)
        self.assertGreater(haversine, 0.0)

    def test_disconnected_components(self):
        g = Graph()
        for i in range(1, 5):
            g.add_node(f"N{i}")

        g.add_edge("N1", "N2", 5.0)
        g.add_edge("N3", "N4", 7.0)

        comps = g.get_connected_components()
        self.assertEqual(len(comps), 2)
        self.assertFalse(g.is_connected())

    def test_json_and_csv_roundtrip(self):
        g = Graph("SerializationTest")
        g.add_node("H1", "Hub 1", NodeType.HUB, x=1.0, y=2.0, lat=21.0, lon=105.0)
        g.add_node("W1", "Warehouse 1", NodeType.WAREHOUSE, x=4.0, y=6.0, lat=21.1, lon=105.2)
        g.add_edge("H1", "W1", 12.5, road_type="highway")

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)

            # Test JSON
            json_file = tmp_path / "test.json"
            g.save_json(json_file)
            loaded_g = Graph.load_json(json_file)
            self.assertEqual(loaded_g.num_nodes, 2)
            self.assertEqual(loaded_g.num_edges, 1)
            self.assertEqual(loaded_g.edges[0].weight, 12.5)

            # Test CSV
            nodes_csv = tmp_path / "nodes.csv"
            edges_csv = tmp_path / "edges.csv"
            g.save_csv(nodes_csv, edges_csv)
            loaded_csv_g = Graph.load_csv(nodes_csv, edges_csv)
            self.assertEqual(loaded_csv_g.num_nodes, 2)
            self.assertEqual(loaded_csv_g.num_edges, 1)


if __name__ == "__main__":
    unittest.main()
