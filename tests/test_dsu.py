"""
Unit tests for DisjointSetUnion (DSU) data structure.
Compatible with standard library unittest and pytest.
"""

import unittest
from src.algorithms.dsu import DisjointSetUnion


class TestDisjointSetUnion(unittest.TestCase):
    def test_dsu_initialization(self):
        nodes = ["A", "B", "C", "D"]
        dsu = DisjointSetUnion(nodes)
        self.assertEqual(dsu.num_sets, 4)
        for node in nodes:
            self.assertEqual(dsu.find(node), node)

    def test_dsu_union_and_cycle_detection(self):
        dsu = DisjointSetUnion(["A", "B", "C", "D"])

        # Merge A and B
        self.assertTrue(dsu.union("A", "B"))
        self.assertEqual(dsu.num_sets, 3)
        self.assertTrue(dsu.connected("A", "B"))

        # Merge B and C
        self.assertTrue(dsu.union("B", "C"))
        self.assertEqual(dsu.num_sets, 2)
        self.assertTrue(dsu.connected("A", "C"))

        # Attempt to union A and C (cycle detected)
        self.assertFalse(dsu.union("A", "C"))
        self.assertEqual(dsu.num_sets, 2)

    def test_dsu_path_compression(self):
        dsu = DisjointSetUnion(range(10))
        for i in range(4):
            dsu.union(i, i + 1)

        root = dsu.find(0)
        for i in range(5):
            self.assertEqual(dsu.find(i), root)

        # Verify path compression flattened parent pointer directly
        dsu.find(4)
        self.assertEqual(dsu.parent[4], root)

    def test_dsu_components(self):
        dsu = DisjointSetUnion(["A", "B", "C", "D", "E"])
        dsu.union("A", "B")
        dsu.union("C", "D")

        self.assertEqual(dsu.num_sets, 3)
        comps = dsu.get_components()
        self.assertEqual(len(comps), 3)


if __name__ == "__main__":
    unittest.main()
