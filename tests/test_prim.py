import unittest
from src.algorithms.prim import lazyPrims


class TestPrimAlgorithm(unittest.TestCase):
    def test_basic_mst_integer_nodes(self):
        """Kiểm thử đồ thị cơ bản với ID đỉnh là số nguyên."""
        n = 5
        edges = [
            (1, 2, 3),
            (1, 3, 4),
            (2, 3, 1),
            (2, 4, 7),
            (3, 5, 2),
            (4, 5, 5),
        ]
        total_weight, mst_edges, is_connected = lazyPrims(n, edges, start=1)

        self.assertTrue(is_connected)
        self.assertEqual(total_weight, 11)
        self.assertEqual(len(mst_edges), n - 1)

    def test_string_node_ids_logistics(self):
        """Kiểm thử với định dạng chuỗi ID nút mạng lưới Logistics (Hub, Warehouse, Delivery)."""
        nodes = ["Hub_A", "WH_B", "WH_C", "DP_D"]
        edges = [
            ("Hub_A", "WH_B", 10.0),
            ("Hub_A", "WH_C", 15.0),
            ("WH_B", "WH_C", 4.0),
            ("WH_B", "DP_D", 8.0),
            ("WH_C", "DP_D", 9.0),
        ]
        total_weight, mst_edges, is_connected = lazyPrims(edges=edges, nodes=nodes)

        self.assertTrue(is_connected)
        # MST tối ưu: (WH_B, WH_C, 4.0) + (WH_B, DP_D, 8.0) + (Hub_A, WH_B, 10.0) = 22.0
        self.assertEqual(total_weight, 22.0)
        self.assertEqual(len(mst_edges), len(nodes) - 1)

    def test_start_node_independence(self):
        """Kiểm thử: Dù bắt đầu ở bất kỳ đỉnh nào thì tổng trọng số MST vẫn phải bằng nhau."""
        n = 4
        edges = [
            (1, 2, 1),
            (2, 3, 2),
            (3, 4, 3),
            (4, 1, 4),
            (1, 3, 5)
        ]
        cost_start_1, _, _ = lazyPrims(n, edges, start=1)
        cost_start_2, _, _ = lazyPrims(n, edges, start=2)
        cost_start_4, _, _ = lazyPrims(n, edges, start=4)

        self.assertEqual(cost_start_1, cost_start_2)
        self.assertEqual(cost_start_2, cost_start_4)
        self.assertEqual(cost_start_1, 6)

    def test_disconnected_graph(self):
        """Kiểm thử đồ thị bị cô lập / không liên thông."""
        nodes = [1, 2, 3, 4, 5]
        # Thành phần 1: {1, 2, 3}, Thành phần 2: {4, 5} -> Không có cạnh nối giữa 2 nhóm
        edges = [
            (1, 2, 2),
            (2, 3, 3),
            (4, 5, 4)
        ]
        total_weight, mst_edges, is_connected = lazyPrims(nodes=nodes, edges=edges, start=1)

        self.assertFalse(is_connected)
        # Vì bắt đầu từ 1, chỉ kết nối được 1-2-3 (2 cạnh)
        self.assertEqual(len(mst_edges), 2)
        self.assertNotEqual(len(mst_edges), len(nodes) - 1)

    def test_single_node_and_empty(self):
        """Kiểm thử trường hợp biên: 1 đỉnh đơn lẻ hoặc đồ thị rỗng."""
        # 1 đỉnh đơn lẻ
        weight, edges, connected = lazyPrims(nodes=["H1"], edges=[])
        self.assertEqual(weight, 0)
        self.assertEqual(len(edges), 0)
        self.assertTrue(connected)

        # 0 đỉnh
        weight_0, edges_0, connected_0 = lazyPrims(nodes=[], edges=[])
        self.assertEqual(weight_0, 0)
        self.assertEqual(len(edges_0), 0)
        self.assertTrue(connected_0)

    def test_equal_weights(self):
        """Kiểm thử khi nhiều cạnh có cùng trọng số (Tie-breaking)."""
        nodes = [1, 2, 3]
        edges = [
            (1, 2, 5),
            (2, 3, 5),
            (1, 3, 5)
        ]
        weight, mst_edges, connected = lazyPrims(nodes=nodes, edges=edges)
        self.assertTrue(connected)
        self.assertEqual(weight, 10)
        self.assertEqual(len(mst_edges), 2)


if __name__ == '__main__':
    unittest.main()

