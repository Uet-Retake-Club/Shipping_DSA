"""
Unit Tests for Borůvka's Algorithm.
Kiểm tra tính đúng đắn, xử lý edge cases và đối soát chéo với NetworkX.
"""

import os
import sys

# Thêm thư mục gốc vào sys.path để có thể import package 'src' khi chạy trực tiếp file test
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import networkx as nx
import pytest

from src.algorithms.boruvka import boruvka_mst, boruvka_from_json
from src.algorithms.dsu import DisjointSetUnion


class TestDisjointSetUnion:
    """Kiểm tra cấu trúc dữ liệu DSU."""

    def test_dsu_basic_operations(self):
        dsu = DisjointSetUnion(["A", "B", "C", "D"])
        assert dsu.count == 4
        assert not dsu.is_connected("A", "B")

        # Union A and B
        assert dsu.union("A", "B") is True
        assert dsu.count == 3
        assert dsu.is_connected("A", "B")

        # Duplicate union should return False
        assert dsu.union("A", "B") is False
        assert dsu.count == 3

        # Union B and C -> A, B, C are connected
        assert dsu.union("B", "C") is True
        assert dsu.count == 2
        assert dsu.is_connected("A", "C")

        # D remains separate
        assert not dsu.is_connected("A", "D")


class TestBoruvkaAlgorithm:
    """Kiểm tra thuật toán Boruvka."""

    def test_simple_triangle_graph(self):
        # Tam giác 3 đỉnh: (A, B, 1), (B, C, 2), (A, C, 3)
        edges = [
            ("A", "B", 1.0),
            ("B", "C", 2.0),
            ("A", "C", 3.0),
        ]
        result = boruvka_mst(edges)

        assert result.is_connected is True
        assert result.num_components == 1
        assert len(result.mst_edges) == 2
        assert result.total_weight == pytest.approx(3.0)

    def test_tie_breaking_equal_weights(self):
        # Hình vuông 4 đỉnh đều có trọng số 2:
        # A - B
        # |   |
        # D - C
        edges = [
            {"u": "A", "v": "B", "weight": 2.0},
            {"u": "B", "v": "C", "weight": 2.0},
            {"u": "C", "v": "D", "weight": 2.0},
            {"u": "D", "v": "A", "weight": 2.0},
        ]
        result = boruvka_mst(edges)

        assert result.is_connected is True
        assert len(result.mst_edges) == 3
        assert result.total_weight == pytest.approx(6.0)

    def test_disconnected_graph(self):
        # 2 thành phần liên thông riêng biệt: {A, B} và {C, D}
        edges = [
            ("A", "B", 5.0),
            ("C", "D", 7.0),
        ]
        nodes = ["A", "B", "C", "D", "E"]  # E là đỉnh cô lập
        result = boruvka_mst(edges, nodes=nodes)

        assert result.is_connected is False
        assert result.num_components == 3  # {A, B}, {C, D}, {E}
        assert len(result.mst_edges) == 2
        assert result.total_weight == pytest.approx(12.0)

    def test_self_loops_and_parallel_edges(self):
        # Đồ thị có khuyên (self-loop) và cạnh song song
        edges = [
            ("A", "A", 0.5),   # Khuyên - cần bỏ qua
            ("A", "B", 10.0),  # Cạnh song song 1
            ("A", "B", 3.0),   # Cạnh song song 2 (nhỏ hơn)
            ("B", "C", 4.0),
        ]
        result = boruvka_mst(edges)

        assert result.is_connected is True
        assert len(result.mst_edges) == 2
        assert result.total_weight == pytest.approx(7.0)

    def test_cross_validation_with_networkx_random_graph(self):
        # Tạo đồ thị ngẫu nhiên và đối soát kết quả tổng trọng số với NetworkX
        G = nx.gnp_random_graph(n=20, p=0.3, seed=42)
        # Gán trọng số ngẫu nhiên cho các cạnh
        import random
        rnd = random.Random(42)
        edge_list = []
        for u, v in G.edges():
            w = round(rnd.uniform(1.0, 50.0), 2)
            G[u][v]["weight"] = w
            edge_list.append((u, v, w))

        # Đảm bảo chỉ xét thành phần liên thông lớn nhất
        largest_cc = max(nx.connected_components(G), key=len)
        subgraph = G.subgraph(largest_cc).copy()
        sub_edges = [(u, v, subgraph[u][v]["weight"]) for u, v in subgraph.edges()]

        # Tính MST bằng NetworkX Kruskal
        nx_mst = nx.minimum_spanning_tree(subgraph, algorithm="kruskal")
        expected_weight = sum(d["weight"] for _, _, d in nx_mst.edges(data=True))

        # Tính MST bằng Boruvka của chúng ta
        result = boruvka_mst(sub_edges, nodes=list(largest_cc))

        assert result.is_connected is True
        assert result.total_weight == pytest.approx(expected_weight, rel=1e-3)
        assert len(result.mst_edges) == len(largest_cc) - 1

    def test_hanoi_network_real_data(self):
        # Kiểm tra chạy trên dataset thực tế Hà Nội
        json_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "data", "reallife_data", "hanoi_network.json")
        )
        if not os.path.exists(json_path):
            pytest.skip("Chưa tìm thấy dataset hanoi_network.json")

        result = boruvka_from_json(json_path)
        assert result.total_weight > 0
        assert len(result.mst_edges) > 0
        # Đồ thị Hà Nội có 22 đỉnh, nếu liên thông thì MST có 21 cạnh
        if result.is_connected:
            assert len(result.mst_edges) == 21


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
