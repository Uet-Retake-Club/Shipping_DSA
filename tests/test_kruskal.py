"""
Unit tests cho src/algorithms/kruskal.py.

Nguyên tắc: khi có cạnh cùng trọng số, MST có thể KHÔNG duy nhất, nên các test
kiểm tra tổng trọng số, số cạnh, số thành phần liên thông và tính hợp lệ của cây
(không chu trình, bao trùm) thay vì so sánh danh sách cạnh cụ thể.
"""

import copy
import csv
import heapq
import json
import math
import random
import sys
import threading
import time
import tracemalloc
import warnings
from collections import Counter, defaultdict, deque
from decimal import Decimal
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path

import pytest

import src.algorithms.kruskal as kruskal_module
from src.algorithms.kruskal import MSTResult, kruskal

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# ``kruskal_mst`` là điểm vào gọn theo đặc tả (trả về (danh sách cạnh, tổng trọng số)).
# Nếu kruskal.py chưa có hàm này, các test RIÊNG của nó bị bỏ qua (skip, có ghi lý do)
# thay vì làm hỏng cả file test; mọi test của kruskal() vẫn chạy đầy đủ.
kruskal_mst = getattr(kruskal_module, "kruskal_mst", None)
requires_kruskal_mst = pytest.mark.skipif(
    kruskal_mst is None, reason="kruskal.py chưa có hàm kruskal_mst"
)


# ---------------------------------------------------------------------------
# Hàm phụ trợ độc lập với DSU (để kiểm chứng không "tự chấm bài mình")
# ---------------------------------------------------------------------------
def _labels_after_merging(node_ids, edges):
    """Gộp nhãn thành phần liên thông bằng cách ngây thơ. Trả (labels, is_forest)."""
    label = {n: n for n in node_ids}
    is_forest = True
    for u, v, *_ in edges:
        if label[u] == label[v]:
            is_forest = False
            continue
        old, new = label[v], label[u]
        for n in label:
            if label[n] == old:
                label[n] = new
    return label, is_forest


def _count_components(node_ids, edges):
    label, _ = _labels_after_merging(node_ids, edges)
    return len(set(label.values()))


def _assert_valid_spanning_forest(node_ids, edges, result):
    """Các cạnh chọn phải là rừng bao trùm: không chu trình, giữ nguyên liên thông."""
    chosen = [(e["u"], e["v"]) for e in result.edges]
    _, acyclic = _labels_after_merging(node_ids, chosen)
    assert acyclic, "MST không được chứa chu trình"

    expected_components = _count_components(node_ids, edges)
    assert result.num_components == expected_components
    # Rừng chọn ra phải có cùng số thành phần liên thông với đồ thị gốc.
    assert _count_components(node_ids, chosen) == expected_components
    assert result.num_edges == len(node_ids) - expected_components


def _brute_force_msf_weight(node_ids, edges):
    """Trọng số rừng bao trùm nhỏ nhất bằng cách thử mọi tập V-C cạnh."""
    k = len(node_ids) - _count_components(node_ids, edges)
    best = math.inf
    for combo in combinations(edges, k):
        _, acyclic = _labels_after_merging(node_ids, combo)
        if acyclic:
            best = min(best, sum(w for _, _, w in combo))
    return best


def _reference_msf_total(node_ids, raw_edges):
    """
    Prim dùng heapq chạy từ mỗi thành phần liên thông: trọng số rừng bao trùm nhỏ nhất.
    Cài đặt hoàn toàn độc lập với DSU/Kruskal, chỉ dùng làm đối chứng.
    """
    adjacency = defaultdict(list)
    for u, v, weight in raw_edges:
        if u != v:
            adjacency[u].append((weight, v))
            adjacency[v].append((weight, u))
    visited = set()
    weights = []
    for start in node_ids:
        if start in visited:
            continue
        visited.add(start)
        heap = list(adjacency[start])
        heapq.heapify(heap)
        while heap:
            weight, node = heapq.heappop(heap)
            if node in visited:
                continue
            visited.add(node)
            weights.append(weight)
            for item in adjacency[node]:
                if item[1] not in visited:
                    heapq.heappush(heap, item)
    return math.fsum(weights)


def _run_with_timeout(fn, seconds=20):
    """Chạy ``fn`` trong luồng phụ; quá hạn thì báo lỗi thay vì treo cả bộ test.
    (Dùng threading thay vì signal.alarm để chạy được cả trên Windows.)"""
    box = {}

    def target():
        try:
            box["result"] = fn()
        except BaseException as exc:  # noqa: BLE001 - chuyển tiếp mọi lỗi ra luồng chính
            box["error"] = exc

    thread = threading.Thread(target=target, daemon=True)
    thread.start()
    thread.join(seconds)
    if thread.is_alive():
        pytest.fail(f"chạy quá {seconds}s: nghi ngờ vòng lặp vô hạn")
    if "error" in box:
        raise box["error"]
    return box.get("result")


def _edge(u, v, weight, **extra):
    return {"u": u, "v": v, "weight": weight, **extra}


# ---------------------------------------------------------------------------
# Ví dụ nhỏ tính tay
# ---------------------------------------------------------------------------
class TestHandComputedExamples:
    def test_square_with_diagonal_cycle(self):
        # Ví dụ trong bài VNOI: chu trình 1-2-3-4, trọng số 1, 2, 3, 4.
        edges = [_edge(1, 2, 1), _edge(2, 3, 2), _edge(3, 4, 3), _edge(4, 1, 4)]
        result = kruskal([1, 2, 3, 4], edges)
        assert result.total_weight == 6
        assert result.num_edges == 3
        assert result.is_connected
        # Cạnh nặng nhất (4-1) đóng chu trình nên bị loại.
        assert _edge(4, 1, 4) not in result.edges

    def test_vnoi_qbmst_sample(self):
        # Đồ thị 6 đỉnh 9 cạnh (mẫu bài QBMST): 5 cạnh trọng số 1 tạo cây.
        raw = [
            (1, 2, 1), (1, 3, 1), (2, 4, 1), (2, 3, 2), (2, 5, 1),
            (3, 5, 1), (3, 6, 1), (4, 5, 2), (5, 6, 2),
        ]
        result = kruskal(range(1, 7), raw)
        assert result.total_weight == 5
        assert result.num_edges == 5

    def test_edges_are_selected_in_nondecreasing_weight_order(self):
        edges = [_edge("A", "B", 5), _edge("B", "C", 1), _edge("A", "C", 3), _edge("C", "D", 2)]
        result = kruskal("ABCD", edges)
        weights = [e["weight"] for e in result.edges]
        assert weights == sorted(weights)
        assert result.total_weight == 6  # 1 + 2 + 3

    def test_edge_order_in_input_does_not_matter_for_total(self):
        edges = [_edge("A", "B", 4), _edge("B", "C", 1), _edge("A", "C", 2), _edge("C", "D", 7),
                 _edge("B", "D", 3)]
        expected = kruskal("ABCD", edges).total_weight
        rng = random.Random(1)
        for _ in range(20):
            shuffled = edges[:]
            rng.shuffle(shuffled)
            assert kruskal("ABCD", shuffled).total_weight == expected == 6

    def test_tree_input_returns_all_edges(self):
        edges = [_edge("A", "B", 3), _edge("B", "C", 9), _edge("C", "D", 1)]
        result = kruskal("ABCD", edges)
        assert result.num_edges == 3
        assert result.total_weight == 13


# ---------------------------------------------------------------------------
# Trường hợp biên
# ---------------------------------------------------------------------------
class TestEdgeCases:
    def test_empty_graph(self):
        result = kruskal([], [])
        assert result.edges == []
        assert result.total_weight == 0
        assert result.num_nodes == 0
        assert result.num_components == 0
        assert result.is_connected

    def test_single_node(self):
        result = kruskal(["H0"], [])
        assert result.edges == []
        assert result.total_weight == 0
        assert result.num_components == 1
        assert result.is_connected

    def test_nodes_without_edges_are_isolated(self):
        with pytest.warns(UserWarning):
            result = kruskal(["A", "B", "C"], [])
        assert result.num_edges == 0
        assert result.num_components == 3
        assert not result.is_connected

    def test_self_loop_is_ignored(self):
        edges = [_edge("A", "A", 0.5), _edge("A", "B", 2)]
        result = kruskal("AB", edges)
        assert result.total_weight == 2
        assert result.num_edges == 1

    def test_parallel_edges_pick_the_cheapest(self):
        edges = [_edge("A", "B", 9), _edge("B", "A", 4), _edge("A", "B", 6)]
        result = kruskal("AB", edges)
        assert result.total_weight == 4
        assert result.num_edges == 1

    def test_all_equal_weights_triangle_has_multiple_valid_msts(self):
        edges = [_edge("A", "B", 1), _edge("B", "C", 1), _edge("A", "C", 1)]
        result = kruskal("ABC", edges)
        assert result.total_weight == 2
        assert result.num_edges == 2
        _assert_valid_spanning_forest("ABC", [(e["u"], e["v"], 1) for e in edges], result)

    def test_undirected_edge_direction_is_irrelevant(self):
        forward = kruskal("ABC", [_edge("A", "B", 1), _edge("B", "C", 2)])
        backward = kruskal("ABC", [_edge("B", "A", 1), _edge("C", "B", 2)])
        assert forward.total_weight == backward.total_weight == 3

    def test_zero_and_float_weights(self):
        edges = [_edge("A", "B", 0), _edge("B", "C", 0.1), _edge("A", "C", 0.2)]
        result = kruskal("ABC", edges)
        assert result.total_weight == pytest.approx(0.1)

    def test_float_total_uses_exact_summation(self):
        # Cộng dồn thủ công 10 lần 0.1 cho 0.9999999999999999 (sai số dấu phẩy động);
        # tổng chính xác (fsum) phải cho đúng 1.0. (Không dùng sum() để kiểm tra
        # điều kiện vì Python >= 3.12 đã tự bù sai số cho sum() trên float.)
        nodes = list(range(11))
        edges = [(i, i + 1, 0.1) for i in range(10)]
        naive_total = 0.0
        for _, _, w in edges:
            naive_total += w
        assert naive_total != 1.0
        assert kruskal(nodes, edges).total_weight == 1.0

    def test_integer_node_ids_and_string_ids_both_work(self):
        assert kruskal([0, 1, 2], [(0, 1, 1), (1, 2, 1)]).total_weight == 2
        assert kruskal(["0", "1", "2"], [("0", "1", 1), ("1", "2", 1)]).total_weight == 2


# ---------------------------------------------------------------------------
# Đồ thị không liên thông (MST Forest)
# ---------------------------------------------------------------------------
class TestDisconnectedGraph:
    NODES = ["A", "B", "C", "D", "E", "F"]  # F bị cô lập
    EDGES = [
        _edge("A", "B", 1), _edge("B", "C", 2), _edge("A", "C", 3),  # thành phần 1
        _edge("D", "E", 4),                                          # thành phần 2
    ]

    def test_returns_minimum_spanning_forest(self):
        with pytest.warns(UserWarning):
            result = kruskal(self.NODES, self.EDGES)
        assert result.total_weight == 1 + 2 + 4
        assert result.num_edges == 6 - 3  # V - C
        assert result.num_components == 3
        assert not result.is_connected
        _assert_valid_spanning_forest(
            self.NODES, [(e["u"], e["v"], e["weight"]) for e in self.EDGES], result
        )

    def test_components_are_reported(self):
        with pytest.warns(UserWarning):
            result = kruskal(self.NODES, self.EDGES)
        as_sets = {frozenset(c) for c in result.components}
        assert as_sets == {frozenset("ABC"), frozenset("DE"), frozenset("F")}

    def test_warning_message_mentions_component_count(self):
        with pytest.warns(UserWarning, match="3 thành phần"):
            kruskal(self.NODES, self.EDGES)

    def test_warning_can_be_disabled(self):
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            result = kruskal(self.NODES, self.EDGES, warn_if_disconnected=False)
        assert result.num_components == 3

    def test_no_warning_for_connected_graph(self):
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            kruskal("ABC", [_edge("A", "B", 1), _edge("B", "C", 1)])


# ---------------------------------------------------------------------------
# Định dạng đầu vào và đầu ra
# ---------------------------------------------------------------------------
class TestInputOutputFormats:
    def test_nodes_as_dict_records_and_edges_as_dicts(self):
        nodes = [{"id": "H0", "type": "hub"}, {"id": "W1", "type": "warehouse"}]
        edges = [_edge("H0", "W1", 35.0, road_type="highway")]
        result = kruskal(nodes, edges)
        assert result.total_weight == 35.0
        assert result.edges == [_edge("H0", "W1", 35.0, road_type="highway")]

    def test_edges_as_tuples_and_lists_are_normalized_to_dicts(self):
        result = kruskal("ABC", [("A", "B", 2), ["B", "C", 1, "extra"]])
        assert result.edges == [_edge("B", "C", 1), _edge("A", "B", 2)]

    def test_accepts_generators(self):
        nodes = (n for n in "ABC")
        edges = (e for e in [("A", "B", 1), ("B", "C", 2)])
        assert kruskal(nodes, edges).total_weight == 3

    def test_input_is_not_mutated(self):
        nodes = [{"id": "A"}, {"id": "B"}, {"id": "C"}]
        edges = [_edge("B", "C", 5), _edge("A", "B", 1), _edge("A", "C", 2)]
        nodes_before, edges_before = copy.deepcopy(nodes), copy.deepcopy(edges)
        kruskal(nodes, edges)
        assert nodes == nodes_before
        assert edges == edges_before  # kể cả thứ tự cạnh

    def test_result_edges_are_copies(self):
        edges = [_edge("A", "B", 1)]
        result = kruskal("AB", edges)
        result.edges[0]["weight"] = 999
        assert edges[0]["weight"] == 1

    def test_result_type_and_derived_properties(self):
        result = kruskal("ABC", [_edge("A", "B", 1), _edge("B", "C", 1)])
        assert isinstance(result, MSTResult)
        assert result.num_nodes == 3
        assert result.num_edges == 2
        assert result.num_components == 1
        assert result.is_connected
        assert isinstance(result.total_weight, float)


# ---------------------------------------------------------------------------
# Kiểm tra dữ liệu đầu vào
# ---------------------------------------------------------------------------
class TestValidation:
    def test_duplicate_node_ids_rejected(self):
        with pytest.raises(ValueError, match="Trùng id"):
            kruskal(["A", "B", "A"], [])

    def test_node_dict_without_id_rejected(self):
        with pytest.raises(ValueError, match="id"):
            kruskal([{"name": "no id"}], [])

    @pytest.mark.parametrize("missing", ["u", "v", "weight"])
    def test_edge_missing_field_rejected(self, missing):
        edge = _edge("A", "B", 1)
        del edge[missing]
        with pytest.raises(ValueError, match=f"'{missing}'"):
            kruskal("AB", [edge])

    @pytest.mark.parametrize("bad_edge", [("A", "B"), "AB1", 42, None, ["A"]])
    def test_malformed_edge_rejected(self, bad_edge):
        with pytest.raises(ValueError):
            kruskal("AB", [bad_edge])

    @pytest.mark.parametrize(
        "bad_weight", [math.nan, math.inf, -math.inf, "5", None, True, [1], 1 + 2j]
    )
    def test_invalid_weight_rejected(self, bad_weight):
        with pytest.raises(ValueError, match="trọng số"):
            kruskal("AB", [_edge("A", "B", bad_weight)])

    def test_unknown_endpoint_rejected(self):
        with pytest.raises(ValueError, match="không tồn tại"):
            kruskal("AB", [_edge("A", "Z", 1)])
        with pytest.raises(ValueError, match="không tồn tại"):
            kruskal("AB", [_edge("Z", "A", 1)])

    def test_bad_edge_after_early_stop_is_still_reported(self):
        # Đồ thị đã liên thông sau cạnh đầu, cạnh lỗi nằm cuối vẫn phải bị phát hiện
        # (không được bỏ sót vì thuật toán dừng sớm).
        edges = [_edge("A", "B", 1), _edge("A", "Z", 99)]
        with pytest.raises(ValueError, match="không tồn tại"):
            kruskal("AB", edges)

    def test_errors_carry_edge_index(self):
        edges = [_edge("A", "B", 1), _edge("B", "C", math.nan)]
        with pytest.raises(ValueError, match=r"edges\[1\]"):
            kruskal("ABC", edges)


# ---------------------------------------------------------------------------
# Đối chứng ngẫu nhiên với brute-force (gồm khuyên, cạnh song song, không liên thông)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("seed", range(60))
def test_matches_brute_force_on_random_small_graphs(seed):
    rng = random.Random(seed)
    node_ids = list(range(rng.randint(1, 7)))
    num_edges = rng.randint(0, 9)
    # Trọng số nhỏ để có nhiều cạnh trùng trọng số; cho phép khuyên và cạnh song song.
    raw = [
        (rng.choice(node_ids), rng.choice(node_ids), rng.randint(1, 5))
        for _ in range(num_edges)
    ]

    result = kruskal(node_ids, raw, warn_if_disconnected=False)

    assert result.total_weight == pytest.approx(_brute_force_msf_weight(node_ids, raw))
    _assert_valid_spanning_forest(node_ids, raw, result)


# ---------------------------------------------------------------------------
# Dữ liệu thật của nhóm (thư mục data/)
# ---------------------------------------------------------------------------
def _load_json(name):
    path = DATA_DIR / name
    if not path.exists():
        pytest.skip(f"thiếu file dữ liệu {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    return data["nodes"], data["edges"]


def _load_csv(prefix):
    nodes_path, edges_path = DATA_DIR / f"{prefix}_nodes.csv", DATA_DIR / f"{prefix}_edges.csv"
    if not (nodes_path.exists() and edges_path.exists()):
        pytest.skip(f"thiếu file dữ liệu {prefix}_*.csv")
    with nodes_path.open(encoding="utf-8", newline="") as f:
        nodes = list(csv.DictReader(f))
    with edges_path.open(encoding="utf-8", newline="") as f:
        edges = [{**row, "weight": float(row["weight"])} for row in csv.DictReader(f)]
    return nodes, edges


DATASETS = [
    pytest.param(lambda: _load_json("sample_small_10_nodes.json"), 10, id="small-json"),
    pytest.param(lambda: _load_csv("small"), 10, id="small-csv"),
    pytest.param(lambda: _load_json("sample_medium_50_nodes.json"), 50, id="medium-json"),
    pytest.param(lambda: _load_csv("medium"), 50, id="medium-csv"),
    pytest.param(lambda: _load_json("sample_large_500_nodes.json"), 500, id="large-json"),
    pytest.param(lambda: _load_csv("large"), 500, id="large-csv"),
]


@pytest.mark.parametrize("loader, expected_nodes", DATASETS)
def test_real_datasets_produce_valid_connected_mst(loader, expected_nodes):
    nodes, edges = loader()
    result = kruskal(nodes, edges)
    node_ids = [n["id"] for n in nodes]
    raw = [(e["u"], e["v"], e["weight"]) for e in edges]

    assert result.num_nodes == expected_nodes
    assert result.is_connected
    assert result.num_edges == expected_nodes - 1
    _assert_valid_spanning_forest(node_ids, raw, result)
    # Kruskal và Prim phải cho cùng tổng chi phí MST.
    assert result.total_weight == pytest.approx(_reference_msf_total(node_ids, raw))


def test_small_dataset_known_total_and_rejected_cycle_edge():
    nodes, edges = _load_csv("small")
    result = kruskal(nodes, edges)
    assert result.total_weight == pytest.approx(276.74)  # tính tay từ small_edges.csv
    chosen = {frozenset((e["u"], e["v"])) for e in result.edges}
    # D3-D4 (45.62) đóng chu trình D3-W2-D4 nên không được chọn.
    assert frozenset(("D3", "D4")) not in chosen
    # Các cạnh trọng số nhỏ nhất, không tạo chu trình, phải được chọn.
    assert frozenset(("D5", "W3")) in chosen
    assert frozenset(("D3", "W2")) in chosen


def test_real_dataset_edge_extra_fields_survive():
    nodes, edges = _load_csv("small")
    result = kruskal(nodes, edges)
    assert all("road_type" in e for e in result.edges)


def test_matches_networkx_on_real_datasets():
    nx = pytest.importorskip("networkx")
    for prefix in ("small", "medium", "large"):
        nodes, edges = _load_csv(prefix)
        graph = nx.Graph()
        graph.add_nodes_from(n["id"] for n in nodes)
        graph.add_weighted_edges_from((e["u"], e["v"], e["weight"]) for e in edges)
        expected = sum(d["weight"] for _, _, d in nx.minimum_spanning_edges(graph, data=True))
        assert kruskal(nodes, edges).total_weight == pytest.approx(expected)


# ---------------------------------------------------------------------------
# Hồi quy: dữ liệu "hiểm" tìm ra khi tự tấn công code (không treo, không lỗi lạ)
# ---------------------------------------------------------------------------
class TestHostileInput:
    @pytest.mark.parametrize("bad_nodes", [[float("nan")], [{"id": float("nan")}, "B"]])
    def test_nan_node_id_rejected_instead_of_hanging(self, bad_nodes):
        with pytest.raises(ValueError, match="NaN"):
            _run_with_timeout(lambda: kruskal(bad_nodes, []))

    def test_nan_node_id_from_json_rejected(self):
        # json.loads chấp nhận literal NaN của Python.
        data = json.loads(
            '{"nodes":[{"id":NaN},{"id":"B"}],'
            '"edges":[{"u":NaN,"v":"B","weight":1}]}'
        )
        with pytest.raises(ValueError):
            _run_with_timeout(lambda: kruskal(data["nodes"], data["edges"]))

    def test_nan_edge_endpoint_rejected(self):
        with pytest.raises(ValueError, match="không tồn tại"):
            _run_with_timeout(lambda: kruskal("AB", [(float("nan"), "B", 1)]))

    @pytest.mark.parametrize(
        "weight", [10**400, -(10**400), Fraction(10**400), Decimal(1), Decimal("NaN")]
    )
    def test_out_of_range_or_unsupported_weight_rejected(self, weight):
        with pytest.raises(ValueError, match="trọng số"):
            kruskal("AB", [_edge("A", "B", weight)])

    def test_total_overflow_raises_value_error(self):
        # Mỗi trọng số hữu hạn nhưng tổng vượt phạm vi float.
        edges = [_edge("A", "B", 1e308), _edge("B", "C", 1e308)]
        with pytest.raises(ValueError, match="Tổng trọng số"):
            kruskal("ABC", edges)

    def test_unhashable_ids_rejected_with_value_error(self):
        with pytest.raises(ValueError, match="hashable"):
            kruskal([["a"], ["b"]], [])
        with pytest.raises(ValueError, match="hashable"):
            kruskal([{"id": ["a"]}], [])
        with pytest.raises(ValueError, match="hashable"):
            kruskal("AB", [(["A"], "B", 1)])
        with pytest.raises(ValueError, match="hashable"):
            kruskal("AB", [("A", {"x": 1}, 1)])

    @pytest.mark.parametrize("bad", [None, 5, 3.14])
    def test_non_iterable_arguments_raise_type_error(self, bad):
        with pytest.raises(TypeError):
            kruskal(bad, [])
        with pytest.raises(TypeError):
            kruskal([], bad)

    def test_only_value_error_or_valid_result_for_garbage_input(self):
        """Quét tổ hợp giá trị rác: chỉ được trả kết quả hợp lệ hoặc ValueError."""
        junk = [0, 1, 1.5, "x", None, True, [1], float("nan"), float("inf"), Decimal(1)]
        base_nodes = [0, 1, "x"]

        def sweep():
            outcomes = {"ok": 0, "value_error": 0}
            edge_candidates = list(product(junk, repeat=3)) + [
                {"u": a, "v": b, "weight": c} for a, b, c in product(junk, repeat=3)
            ] + junk
            for edge in edge_candidates:
                try:
                    result = kruskal(base_nodes, [edge], warn_if_disconnected=False)
                except ValueError:
                    outcomes["value_error"] += 1
                    continue
                assert result.num_edges == result.num_nodes - result.num_components
                outcomes["ok"] += 1
            for node_junk in product(junk, repeat=2):
                try:
                    result = kruskal(list(node_junk), [], warn_if_disconnected=False)
                except ValueError:
                    outcomes["value_error"] += 1
                    continue
                assert result.num_components == result.num_nodes
                outcomes["ok"] += 1
            return outcomes

        outcomes = _run_with_timeout(sweep)
        assert outcomes["ok"] > 0 and outcomes["value_error"] > 0  # cả hai nhánh đều được thử


# ---------------------------------------------------------------------------
# Đối chứng ngẫu nhiên cỡ vừa với cài đặt Prim độc lập (gồm đồ thị không liên thông)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("seed", range(40))
def test_matches_independent_prim_on_medium_random_graphs(seed):
    rng = random.Random(1000 + seed)
    n = rng.randint(20, 80)
    node_ids = [f"N{i}" for i in range(n)]
    use_ties = seed % 2 == 0

    def weight():
        return rng.randint(1, 8) if use_ties else round(rng.uniform(0.01, 200), 2)

    raw = [
        (rng.choice(node_ids), rng.choice(node_ids), weight())
        for _ in range(rng.randint(0, 4 * n))
    ]

    result = kruskal(node_ids, raw, warn_if_disconnected=False)

    assert result.total_weight == pytest.approx(_reference_msf_total(node_ids, raw))
    _assert_valid_spanning_forest(node_ids, raw, result)


# ---------------------------------------------------------------------------
# Tích hợp với code của đồng đội (src/generators/dataset_generator.py trên nhánh dev)
# ---------------------------------------------------------------------------
def _dataset_generator():
    try:
        from src.generators import dataset_generator as gen

        return gen.load_nodes_csv, gen.load_edges_csv, gen.generate_knn_edges
    except (ImportError, AttributeError):
        pytest.skip("dataset_generator.py chưa có nội dung: hãy merge origin/dev về nhánh này")


@pytest.mark.parametrize("prefix", ["small", "medium", "large"])
def test_integration_with_team_csv_loaders(prefix):
    load_nodes, load_edges, _ = _dataset_generator()
    nodes = load_nodes(str(DATA_DIR / f"{prefix}_nodes.csv"))
    edges = load_edges(str(DATA_DIR / f"{prefix}_edges.csv"))
    result = kruskal(nodes, edges)
    node_ids = [n["id"] for n in nodes]
    raw = [(e["u"], e["v"], e["weight"]) for e in edges]
    assert result.is_connected
    assert result.total_weight == pytest.approx(_reference_msf_total(node_ids, raw))
    _assert_valid_spanning_forest(node_ids, raw, result)


@pytest.mark.parametrize("prefix", ["small", "medium", "large"])
@pytest.mark.parametrize("k", [1, 2, 3])
def test_integration_with_knn_generated_sparse_graphs(prefix, k):
    """Đồ thị thưa do generate_knn_edges sinh ra thường KHÔNG liên thông (MST Forest)."""
    load_nodes, _, generate_knn_edges = _dataset_generator()
    nodes = load_nodes(str(DATA_DIR / f"{prefix}_nodes.csv"))
    edges = generate_knn_edges(nodes, k=k)
    node_ids = [n["id"] for n in nodes]
    raw = [(e["u"], e["v"], e["weight"]) for e in edges]

    result = kruskal(nodes, edges, warn_if_disconnected=False)

    assert result.total_weight == pytest.approx(_reference_msf_total(node_ids, raw))
    _assert_valid_spanning_forest(node_ids, raw, result)


# ---------------------------------------------------------------------------
# Dữ liệu thực tế Hà Nội của đồng đội (data/reallife_data/, có trên nhánh dev)
# ---------------------------------------------------------------------------
HANOI_DIR = DATA_DIR / "reallife_data"


def _load_hanoi_csv():
    nodes_path, edges_path = HANOI_DIR / "hanoi_nodes.csv", HANOI_DIR / "hanoi_edges.csv"
    if not (nodes_path.exists() and edges_path.exists()):
        pytest.skip("thiếu data/reallife_data/hanoi_*.csv: hãy merge origin/dev về nhánh này")
    with nodes_path.open(encoding="utf-8", newline="") as f:
        nodes = list(csv.DictReader(f))
    with edges_path.open(encoding="utf-8", newline="") as f:
        edges = [{**row, "weight": float(row["weight"])} for row in csv.DictReader(f)]
    return nodes, edges


def _load_hanoi_json():
    path = HANOI_DIR / "hanoi_network.json"
    if not path.exists():
        pytest.skip("thiếu data/reallife_data/hanoi_network.json: hãy merge origin/dev về nhánh này")
    data = json.loads(path.read_text(encoding="utf-8"))
    return data["nodes"], data["edges"]


@pytest.mark.parametrize("loader", [_load_hanoi_csv, _load_hanoi_json], ids=["csv", "json"])
def test_hanoi_network_gives_valid_connected_mst(loader):
    nodes, edges = loader()
    result = kruskal(nodes, edges)
    node_ids = [n["id"] for n in nodes]
    raw = [(e["u"], e["v"], e["weight"]) for e in edges]

    assert result.num_nodes == 22
    assert result.is_connected
    assert result.num_edges == 21
    # 138.2 = tổng MST đã đối chiếu độc lập bằng networkx.minimum_spanning_tree.
    assert result.total_weight == pytest.approx(138.2)
    assert result.total_weight == pytest.approx(_reference_msf_total(node_ids, raw))
    _assert_valid_spanning_forest(node_ids, raw, result)
    assert all("road_type" in e for e in result.edges)


def test_hanoi_csv_and_json_agree():
    csv_nodes, csv_edges = _load_hanoi_csv()
    json_nodes, json_edges = _load_hanoi_json()
    from_csv = kruskal(csv_nodes, csv_edges)
    from_json = kruskal(json_nodes, json_edges)
    assert from_csv.total_weight == pytest.approx(from_json.total_weight)
    assert {frozenset((e["u"], e["v"])) for e in from_csv.edges} == {
        frozenset((e["u"], e["v"])) for e in from_json.edges
    }


# ===========================================================================
# BỔ SUNG THEO ĐẶC TẢ: happy path, trường hợp biên, thuộc tính MST, stress
# ===========================================================================
# Các hàm kiểm chứng bên dưới chỉ dùng DFS/BFS thuần, KHÔNG dùng DSU của dự án,
# để bộ test không "tự chấm bài mình".
def _has_cycle_dfs(node_ids, edges):
    """
    Phát hiện chu trình bằng DFS lặp (không đệ quy).

    ``edges`` là danh sách ``(u, v, ...)``. Khuyên và cạnh song song đều tính là
    chu trình: DFS nhớ *id cạnh* đã dùng để tới một đỉnh (không phải đỉnh cha),
    nên hai cạnh song song được nhận ra đúng là chu trình độ dài 2.
    """
    adjacency = defaultdict(list)
    for edge_id, (u, v, *_) in enumerate(edges):
        if u == v:
            return True
        adjacency[u].append((v, edge_id))
        adjacency[v].append((u, edge_id))
    visited = set()
    for root in node_ids:
        if root in visited:
            continue
        visited.add(root)
        stack = [(root, None)]
        while stack:
            node, arrived_by = stack.pop()
            for neighbor, edge_id in adjacency[node]:
                if edge_id == arrived_by:
                    continue
                if neighbor in visited:
                    return True
                visited.add(neighbor)
                stack.append((neighbor, edge_id))
    return False


def _component_partition(node_ids, edges):
    """Phân hoạch đỉnh thành các thành phần liên thông (BFS, độc lập DSU)."""
    adjacency = defaultdict(list)
    for u, v, *_ in edges:
        adjacency[u].append(v)
        adjacency[v].append(u)
    seen = set()
    parts = set()
    for root in node_ids:
        if root in seen:
            continue
        seen.add(root)
        queue, part = deque([root]), []
        while queue:
            node = queue.popleft()
            part.append(node)
            for neighbor in adjacency[node]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append(neighbor)
        parts.add(frozenset(part))
    return parts


def _assert_cycle_optimality(edges, result):
    """
    Chứng chỉ tối ưu của MST (tính chất chu trình), không cần thuật toán đối chứng.

    Một rừng bao trùm F là nhỏ nhất khi và chỉ khi MỌI cạnh (u, v, w) của đồ thị
    đều có w >= trọng số lớn nhất trên đường đi u-v trong F.
    """
    adjacency = defaultdict(list)
    for edge in result.edges:
        adjacency[edge["u"]].append((edge["v"], edge["weight"]))
        adjacency[edge["v"]].append((edge["u"], edge["weight"]))

    for u, v, weight in edges:
        if u == v:
            continue
        heaviest = {u: -math.inf}  # trọng số lớn nhất trên đường đi từ u
        queue = deque([u])
        while queue and v not in heaviest:
            node = queue.popleft()
            for neighbor, w in adjacency[node]:
                if neighbor not in heaviest:
                    heaviest[neighbor] = max(heaviest[node], w)
                    queue.append(neighbor)
        assert v in heaviest, f"{u!r}-{v!r} cùng thành phần của đồ thị nhưng khác cây"
        assert weight >= heaviest[v], (
            f"cạnh {u!r}-{v!r} ({weight}) nhẹ hơn cạnh nặng nhất ({heaviest[v]}) "
            "trên đường đi tương ứng trong MST"
        )


def _all_spanning_forests(node_ids, edges):
    """Mọi tập cạnh (theo chỉ số) là cây/rừng bao trùm: V-C cạnh và không chu trình."""
    k = len(node_ids) - len(_component_partition(node_ids, edges))
    return [
        combo
        for combo in combinations(range(len(edges)), k)
        if not _has_cycle_dfs(node_ids, [edges[i] for i in combo])
    ]


def _pairs(edge_dicts):
    """Tập các cặp đỉnh (không phân biệt chiều) của danh sách cạnh kết quả."""
    return {frozenset((e["u"], e["v"])) for e in edge_dicts}


def _chosen(result):
    """Các cạnh kết quả dưới dạng (u, v) để đưa vào hàm kiểm chứng."""
    return [(e["u"], e["v"]) for e in result.edges]


# ---------------------------------------------------------------------------
# Happy path bổ sung: tính tay, MST duy nhất, nhiều MST cùng tổng tối thiểu
# ---------------------------------------------------------------------------
class TestHappyPathAdditional:
    def test_five_vertex_graph_hand_computed(self):
        # Sắp xếp: B-C 1 nhận, A-B 2 nhận, A-C 3 bỏ (chu trình A-B-C), B-D 4 nhận,
        # C-D 5 bỏ, C-E 6 nhận, D-E 7 bỏ  =>  1 + 2 + 4 + 6 = 13.
        edges = [
            ("A", "B", 2), ("A", "C", 3), ("B", "C", 1), ("B", "D", 4),
            ("C", "D", 5), ("C", "E", 6), ("D", "E", 7),
        ]
        result = kruskal("ABCDE", edges)
        assert result.total_weight == 13
        assert [(e["u"], e["v"], e["weight"]) for e in result.edges] == [
            ("B", "C", 1), ("A", "B", 2), ("B", "D", 4), ("C", "E", 6),
        ]

    def test_unique_mst_matches_exhaustive_search(self):
        # Trọng số phân biệt => đúng MỘT cây khung nhỏ nhất; Kruskal phải chọn đúng cây đó.
        nodes = list(range(5))
        pairs = list(combinations(nodes, 2))
        weights = random.Random(3).sample(range(1, 100), len(pairs))
        edges = [(i, j, w) for (i, j), w in zip(pairs, weights)]

        forests = _all_spanning_forests(nodes, edges)
        totals = [sum(edges[i][2] for i in combo) for combo in forests]
        best = min(totals)
        optimal = [combo for combo, total in zip(forests, totals) if total == best]

        assert len(forests) == 5 ** 3  # công thức Cayley: K5 có 5^(5-2) cây khung
        assert len(optimal) == 1
        result = kruskal(nodes, edges)
        assert _pairs(result.edges) == {frozenset(edges[i][:2]) for i in optimal[0]}
        assert result.total_weight == best

    def test_several_different_msts_share_the_same_minimum_total(self):
        # Chu trình 1-2-3-4 trọng số 1 + hai đường chéo trọng số 2: bỏ đi bất kỳ cạnh nào
        # của chu trình cho một MST khác nhau, cả 4 MST đều có tổng 3.
        nodes = [1, 2, 3, 4]
        edges = [(1, 2, 1), (2, 3, 1), (3, 4, 1), (4, 1, 1), (1, 3, 2), (2, 4, 2)]
        forests = _all_spanning_forests(nodes, edges)
        totals = {combo: sum(edges[i][2] for i in combo) for combo in forests}
        best = min(totals.values())
        optimal_trees = [
            {frozenset(edges[i][:2]) for i in combo}
            for combo, total in totals.items()
            if total == best
        ]
        assert best == 3
        assert len(optimal_trees) == 4  # bốn cây khung nhỏ nhất KHÁC NHAU

        result = kruskal(nodes, edges)
        assert result.total_weight == best  # mọi MST có cùng tổng
        assert _pairs(result.edges) in optimal_trees

    def test_tie_break_follows_input_order(self):
        base = [("A", "B", 1), ("B", "C", 2), ("A", "C", 2)]
        first = kruskal("ABC", base)
        swapped = kruskal("ABC", [base[0], base[2], base[1]])
        assert _pairs(first.edges) == {frozenset("AB"), frozenset("BC")}
        assert _pairs(swapped.edges) == {frozenset("AB"), frozenset("AC")}
        assert first.total_weight == swapped.total_weight == 3

    @pytest.mark.parametrize(
        "ids",
        [[0, 1, 2, 3], [1, 2, 3, 4], ["A", "B", "C", "D"], ["H1", "W1", "D1", "D2"]],
        ids=["0-indexed", "1-indexed", "letters", "hub-codes"],
    )
    def test_int_and_string_vertex_ids_give_the_same_answer(self, ids):
        shape = [(0, 1, 4), (1, 2, 1), (0, 2, 3), (2, 3, 2), (1, 3, 5)]
        edges = [(ids[i], ids[j], w) for i, j, w in shape]
        result = kruskal(ids, edges)
        assert result.total_weight == 1 + 2 + 3
        assert result.num_edges == 3

    def test_mixed_type_vertex_ids_with_tied_weights(self):
        # Sắp xếp cả tuple (w, u, v) sẽ phải so sánh id khi trùng trọng số và vỡ vì int < str.
        nodes = [1, "1", (1, 2), 2.5]
        edges = [(1, "1", 3), ("1", (1, 2), 3), ((1, 2), 2.5, 3), (1, 2.5, 3)]
        result = kruskal(nodes, edges)
        assert result.num_edges == 3
        assert result.total_weight == 9


# ---------------------------------------------------------------------------
# Trọng số âm và bằng 0
# ---------------------------------------------------------------------------
class TestNegativeAndZeroWeights:
    def test_negative_triangle_picks_the_two_most_negative_edges(self):
        edges = [_edge("A", "B", -5), _edge("B", "C", -3), _edge("A", "C", -4)]
        result = kruskal("ABC", edges)
        assert result.total_weight == -9
        assert _pairs(result.edges) == {frozenset("AB"), frozenset("AC")}

    def test_all_negative_complete_graph_still_spans_with_v_minus_1_edges(self):
        nodes = list(range(5))
        edges = [(i, j, -1 - i - j) for i, j in combinations(nodes, 2)]
        result = kruskal(nodes, edges)
        assert result.num_edges == 4  # không được "lấy hết mọi cạnh âm"
        assert not _has_cycle_dfs(nodes, _chosen(result))
        assert result.total_weight == pytest.approx(_reference_msf_total(nodes, edges))
        _assert_cycle_optimality(edges, result)

    def test_positive_bridge_is_forced_when_it_is_the_only_connection(self):
        result = kruskal("ABC", [_edge("A", "B", -10), _edge("B", "C", 7)])
        assert result.num_edges == 2  # MST vẫn phải bao trùm, kể cả phải nhận cạnh dương
        assert result.total_weight == -3

    def test_negative_self_loop_is_still_ignored(self):
        # Lấy nhầm khuyên -100 sẽ làm tổng sai và tạo chu trình độ dài 1.
        result = kruskal("AB", [_edge("A", "A", -100), _edge("A", "B", 3)])
        assert result.num_edges == 1
        assert result.total_weight == 3

    def test_negative_parallel_edge_is_the_one_chosen(self):
        edges = [_edge("A", "B", 2), _edge("A", "B", -1), _edge("B", "A", 0)]
        result = kruskal("AB", edges)
        assert result.edges == [_edge("A", "B", -1)]
        assert result.total_weight == -1

    def test_zero_weight_edges_are_ordinary_edges(self):
        edges = [_edge("A", "B", 0), _edge("B", "C", 0), _edge("A", "C", 0), _edge("C", "D", 5)]
        result = kruskal("ABCD", edges)
        assert result.num_edges == 3
        assert result.total_weight == 5
        assert not _has_cycle_dfs("ABCD", _chosen(result))

    def test_all_zero_weights_give_a_valid_tree(self):
        nodes = list(range(5))
        edges = [(i, j, 0) for i, j in combinations(nodes, 2)]
        result = kruskal(nodes, edges)
        assert result.num_edges == 4
        assert result.total_weight == 0
        assert not _has_cycle_dfs(nodes, _chosen(result))

    @pytest.mark.parametrize("shift", [-10_000, -1, 0, 1, 10_000])
    def test_shifting_every_weight_does_not_change_the_tree(self, shift):
        # Kruskal chỉ so sánh trọng số: cộng cùng một hằng số (kể cả khiến mọi trọng số âm)
        # giữ nguyên cây; tổng dịch chuyển đúng shift * (V - 1).
        nodes = list(range(8))
        pairs = list(combinations(nodes, 2))
        weights = random.Random(11).sample(range(1, 500), len(pairs))  # phân biệt: MST duy nhất
        base = kruskal(nodes, [(i, j, w) for (i, j), w in zip(pairs, weights)])
        shifted = kruskal(nodes, [(i, j, w + shift) for (i, j), w in zip(pairs, weights)])
        assert _pairs(shifted.edges) == _pairs(base.edges)
        assert shifted.total_weight == base.total_weight + shift * (len(nodes) - 1)


# ---------------------------------------------------------------------------
# Trường hợp biên bổ sung
# ---------------------------------------------------------------------------
class TestEdgeCasesAdditional:
    def test_single_vertex_with_only_a_self_loop(self):
        result = kruskal(["A"], [("A", "A", 5)])
        assert result.edges == []
        assert result.total_weight == 0
        assert result.is_connected

    def test_only_self_loops_leave_every_vertex_isolated(self):
        with pytest.warns(UserWarning, match="2 thành phần"):
            result = kruskal("AB", [("A", "A", 1), ("B", "B", -2)])
        assert result.num_edges == 0
        assert result.num_components == 2
        assert result.total_weight == 0

    def test_many_parallel_edges_keep_only_the_cheapest(self):
        edges = [("A", "B", w) for w in range(100, 0, -1)] + [("B", "A", 0.5)]
        result = kruskal("AB", edges)
        assert result.edges == [_edge("B", "A", 0.5)]
        assert result.total_weight == 0.5

    def test_equal_parallel_edges_keep_exactly_one(self):
        result = kruskal("AB", [("A", "B", 2), ("B", "A", 2), ("A", "B", 2)])
        assert result.num_edges == 1
        assert result.total_weight == 2


# ---------------------------------------------------------------------------
# Các trọng số bằng nhau: kết quả phải là cây/rừng khung hợp lệ, không chu trình
# ---------------------------------------------------------------------------
class TestEqualWeights:
    @pytest.mark.parametrize("n", [3, 4, 6, 9])
    def test_complete_graph_with_equal_weights(self, n):
        nodes = list(range(n))
        edges = [(i, j, 5) for i, j in combinations(nodes, 2)]
        result = kruskal(nodes, edges)
        assert result.num_edges == n - 1
        assert result.total_weight == 5 * (n - 1)
        assert not _has_cycle_dfs(nodes, _chosen(result))
        assert _component_partition(nodes, _chosen(result)) == {frozenset(nodes)}

    def test_grid_with_equal_weights(self):
        side = 4
        nodes = [(r, c) for r in range(side) for c in range(side)]  # id đỉnh dạng tuple
        edges = [((r, c), (r, c + 1), 7) for r in range(side) for c in range(side - 1)]
        edges += [((r, c), (r + 1, c), 7) for r in range(side - 1) for c in range(side)]
        result = kruskal(nodes, edges)
        assert result.num_edges == side * side - 1
        assert result.total_weight == 7 * (side * side - 1)
        assert not _has_cycle_dfs(nodes, _chosen(result))

    def test_disconnected_graph_with_equal_weights_gives_a_forest(self):
        first, second = ["a0", "a1", "a2", "a3"], ["b0", "b1", "b2", "b3"]
        nodes = first + second + ["lonely"]  # V = 9, C = 3
        edges = [(u, v, 2) for group in (first, second) for u, v in combinations(group, 2)]
        with pytest.warns(UserWarning):
            result = kruskal(nodes, edges)
        assert result.num_edges == 6
        assert result.total_weight == 12
        assert result.num_components == 3
        assert not _has_cycle_dfs(nodes, _chosen(result))
        assert _component_partition(nodes, _chosen(result)) == {
            frozenset(first), frozenset(second), frozenset(["lonely"]),
        }


# ---------------------------------------------------------------------------
# Kiểm tra thuộc tính MST trên đồ thị ngẫu nhiên (có âm, có 0, trùng trọng số,
# khuyên, cạnh song song, không liên thông)
# ---------------------------------------------------------------------------
_WEIGHT_MODES = {
    "ties": lambda rng: rng.randint(1, 4),  # rất nhiều cạnh trùng trọng số
    "mixed_sign": lambda rng: rng.randint(-10, 10),  # có âm, có 0, có dương
    "float": lambda rng: round(rng.uniform(-5.0, 5.0), 2),
}
PROPERTY_CASES = [(mode, seed) for mode in _WEIGHT_MODES for seed in range(12)]


def _random_multigraph(rng, mode, *, connected, max_nodes=25):
    """Đa đồ thị ngẫu nhiên (id chuỗi) có khuyên và cạnh song song."""
    n = rng.randint(2, max_nodes)
    node_ids = [f"v{i}" for i in range(n)]
    draw = _WEIGHT_MODES[mode]
    edges = []
    if connected:  # một cây ngẫu nhiên bảo đảm đồ thị liên thông
        edges += [(node_ids[i], node_ids[rng.randrange(i)], draw(rng)) for i in range(1, n)]
    edges += [
        (rng.choice(node_ids), rng.choice(node_ids), draw(rng))
        for _ in range(rng.randint(0, 3 * n))
    ]
    rng.shuffle(edges)
    return node_ids, edges


def _solve(mode, seed, *, connected):
    rng = random.Random(f"{mode}/{seed}/{connected}")
    node_ids, edges = _random_multigraph(rng, mode, connected=connected)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return node_ids, edges, kruskal(node_ids, edges)


@pytest.mark.parametrize(("mode", "seed"), PROPERTY_CASES)
class TestMSTProperties:
    def test_chosen_edges_are_acyclic(self, mode, seed):
        node_ids, _, result = _solve(mode, seed, connected=False)
        assert not _has_cycle_dfs(node_ids, _chosen(result))

    def test_edge_count_is_v_minus_c(self, mode, seed):
        node_ids, edges, result = _solve(mode, seed, connected=False)
        components = _component_partition(node_ids, edges)
        assert result.num_edges == len(node_ids) - len(components)
        assert result.num_components == len(components)
        assert result.is_connected == (len(components) == 1)

    def test_connected_graph_returns_exactly_v_minus_1_edges(self, mode, seed):
        node_ids, _, result = _solve(mode, seed, connected=True)
        assert result.is_connected
        assert result.num_edges == len(node_ids) - 1

    def test_every_vertex_with_a_real_edge_is_covered(self, mode, seed):
        # "Bậc" đếm cạnh KHÔNG phải khuyên: đỉnh chỉ có khuyên (u, u) thực chất bị cô lập
        # và không thể thuộc MST, nên không bị đòi phải xuất hiện.
        node_ids, edges, result = _solve(mode, seed, connected=False)
        degree = defaultdict(int)
        for u, v, _ in edges:
            if u != v:
                degree[u] += 1
                degree[v] += 1
        covered = {x for e in result.edges for x in (e["u"], e["v"])}
        for node in node_ids:
            assert (node in covered) == (degree[node] > 0), node

    def test_forest_keeps_exactly_the_connectivity_of_the_graph(self, mode, seed):
        node_ids, edges, result = _solve(mode, seed, connected=False)
        expected = _component_partition(node_ids, edges)
        assert _component_partition(node_ids, _chosen(result)) == expected
        assert {frozenset(c) for c in result.components} == expected

    def test_chosen_edges_come_from_the_input_and_are_never_reused(self, mode, seed):
        _, edges, result = _solve(mode, seed, connected=False)
        available = Counter((frozenset((u, v)), w) for u, v, w in edges)
        for e in result.edges:
            assert e["u"] != e["v"], "khuyên không được vào MST"
            key = (frozenset((e["u"], e["v"])), e["weight"])
            assert available[key] > 0, f"cạnh {key} không có trong đầu vào (hoặc bị dùng lại)"
            available[key] -= 1

    def test_optimality_certificate_and_independent_prim_total(self, mode, seed):
        node_ids, edges, result = _solve(mode, seed, connected=False)
        _assert_cycle_optimality(edges, result)
        assert result.total_weight == pytest.approx(_reference_msf_total(node_ids, edges))


# ---------------------------------------------------------------------------
# kruskal_mst: điểm vào gọn trả về (danh sách cạnh MST, tổng trọng số)
# ---------------------------------------------------------------------------
@requires_kruskal_mst
class TestKruskalMst:
    def test_returns_edge_list_and_total_weight(self):
        edges, total = kruskal_mst([("A", "B", 1), ("B", "C", 2), ("A", "C", 3)])
        assert edges == [_edge("A", "B", 1), _edge("B", "C", 2)]
        assert total == 3
        assert isinstance(total, float)

    def test_vertices_are_inferred_from_the_edges_when_nodes_is_omitted(self):
        with warnings.catch_warnings():
            warnings.simplefilter("error")  # 2 đỉnh A, B suy ra được: liên thông, không cảnh báo
            edges, total = kruskal_mst([("A", "B", 4)])
        assert (edges, total) == ([_edge("A", "B", 4)], 4)

    def test_isolated_vertices_need_explicit_nodes(self):
        with pytest.warns(UserWarning, match="2 thành phần"):
            edges, total = kruskal_mst([("A", "B", 1)], nodes=["A", "B", "C"])
        assert edges == [_edge("A", "B", 1)]
        assert total == 1

    def test_empty_inputs(self):
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            assert kruskal_mst([]) == ([], 0.0)
            assert kruskal_mst([], nodes=[]) == ([], 0.0)
            assert kruskal_mst([], nodes=["only"]) == ([], 0.0)

    def test_self_loop_only_graph_has_one_known_vertex(self):
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            assert kruskal_mst([("A", "A", 3)]) == ([], 0.0)

    def test_accepts_generators_and_dict_edges(self):
        edges = (
            e
            for e in [_edge("H1", "W1", 31.62, road_type="highway"), _edge("W1", "D1", 11.18)]
        )
        mst, total = kruskal_mst(edges)
        assert mst == [_edge("W1", "D1", 11.18), _edge("H1", "W1", 31.62, road_type="highway")]
        assert total == pytest.approx(42.8)

    def test_nodes_is_keyword_only_so_argument_order_cannot_be_mixed_up(self):
        with pytest.raises(TypeError):
            kruskal_mst(["A", "B"], [("A", "B", 1)])

    def test_input_is_not_mutated(self):
        edges = [_edge("B", "C", 5), _edge("A", "B", 1), _edge("A", "C", 2)]
        before = copy.deepcopy(edges)
        kruskal_mst(edges)
        assert edges == before

    @pytest.mark.parametrize("seed", range(20))
    def test_agrees_with_kruskal_on_random_graphs(self, seed):
        rng = random.Random(f"mst/{seed}")
        node_ids, edges = _random_multigraph(rng, "mixed_sign", connected=True)
        expected = kruskal(node_ids, edges)
        for kwargs in ({"nodes": node_ids}, {}):  # có nodes / tự suy ra nodes
            mst, total = kruskal_mst(edges, **kwargs)
            assert mst == expected.edges
            assert total == expected.total_weight

    def test_validation_errors_are_the_same_as_kruskal(self):
        with pytest.raises(ValueError, match=r"edges\[1\].*trọng số"):
            kruskal_mst([("A", "B", 1), ("B", "C", math.nan)])
        with pytest.raises(ValueError, match="hashable"):
            kruskal_mst([(["A"], "B", 1)])
        with pytest.raises(ValueError, match="không tồn tại"):
            kruskal_mst([("A", "Z", 1)], nodes="AB")
        with pytest.raises(ValueError, match="NaN"):
            kruskal_mst([(math.nan, "B", 1)])

    def test_non_iterable_arguments_raise_type_error(self):
        with pytest.raises(TypeError):
            kruskal_mst(None)
        with pytest.raises(TypeError):
            kruskal_mst([], nodes=5)


# ---------------------------------------------------------------------------
# Cảnh báo đồ thị không liên thông phải trỏ tới dòng gọi của người dùng.
# Mặc định Python chỉ hiện một cảnh báo cho mỗi (module, dòng): nếu cảnh báo bị
# gán vào bên trong kruskal.py, mọi lần gọi sau đều bị nuốt mất.
# ---------------------------------------------------------------------------
class TestWarningAttribution:
    CALLS = {
        "kruskal": lambda: kruskal("AB", []),
        "kruskal_mst": lambda: kruskal_mst([], nodes="AB"),
    }

    @pytest.mark.parametrize(
        "name", ["kruskal", pytest.param("kruskal_mst", marks=requires_kruskal_mst)]
    )
    def test_warning_points_at_the_callers_file(self, name):
        with pytest.warns(UserWarning) as record:
            self.CALLS[name]()
        assert Path(record[0].filename).name == Path(__file__).name

    def test_default_filter_reports_every_distinct_call_site(self):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("default")
            kruskal("AB", [])
            kruskal("AB", [])
        assert len(caught) == 2

    @requires_kruskal_mst
    def test_default_filter_reports_every_distinct_kruskal_mst_call_site(self):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("default")
            kruskal_mst([], nodes="AB")
            kruskal_mst([], nodes="AB")
        assert len(caught) == 2


# ---------------------------------------------------------------------------
# Stress / hiệu năng: V = 1000, E = 10.000 phải chạy dưới 1 giây, không tràn
# bộ nhớ, không phụ thuộc đệ quy
# ---------------------------------------------------------------------------
def _random_connected_graph(rng, num_nodes, num_edges):
    """
    Đồ thị liên thông gồm đúng ``num_edges`` cạnh: cây ngẫu nhiên + cạnh ngẫu nhiên.

    Phần cạnh thừa có thể là cạnh song song hoặc khuyên (dữ liệu "bẩn" ngoài đời).
    """
    nodes = list(range(num_nodes))
    edges = [(i, rng.randrange(i), rng.random()) for i in range(1, num_nodes)]
    while len(edges) < num_edges:
        edges.append((rng.randrange(num_nodes), rng.randrange(num_nodes), rng.random()))
    rng.shuffle(edges)
    return nodes, edges


def _best_time(fn, runs=3):
    """Thời gian tốt nhất sau ``runs`` lần chạy (giảm nhiễu do máy bận) và kết quả."""
    best, result = math.inf, None
    for _ in range(runs):
        start = time.perf_counter()
        result = fn()
        best = min(best, time.perf_counter() - start)
    return best, result


def _stack_depth():
    depth, frame = 0, sys._getframe()
    while frame is not None:
        depth += 1
        frame = frame.f_back
    return depth


def _call_with_tight_recursion_limit(fn, headroom=60):
    """Chạy ``fn`` khi giới hạn đệ quy chỉ cao hơn độ sâu ngăn xếp hiện tại ``headroom`` tầng."""
    previous = sys.getrecursionlimit()
    sys.setrecursionlimit(_stack_depth() + headroom)
    try:
        return fn()
    finally:
        sys.setrecursionlimit(previous)


class TestStressAndPerformance:
    def test_v1000_e10000_runs_under_one_second_and_is_correct(self):
        nodes, edges = _random_connected_graph(random.Random(2026), 1000, 10_000)
        elapsed, result = _best_time(lambda: kruskal(nodes, edges))
        assert elapsed < 1.0, f"V=1000, E=10000 mất {elapsed:.3f}s"
        assert result.is_connected
        assert result.num_edges == 999
        assert not _has_cycle_dfs(nodes, _chosen(result))
        assert result.total_weight == pytest.approx(_reference_msf_total(nodes, edges))

    @requires_kruskal_mst
    def test_kruskal_mst_is_just_as_fast_with_inferred_vertices(self):
        nodes, edges = _random_connected_graph(random.Random(2027), 1000, 10_000)
        elapsed, (mst, total) = _best_time(lambda: kruskal_mst(edges))
        assert elapsed < 1.0, f"kruskal_mst mất {elapsed:.3f}s"
        assert len(mst) == 999
        assert total == pytest.approx(_reference_msf_total(nodes, edges))

    def test_dense_complete_graph_300_vertices(self):
        rng = random.Random(8)
        nodes = list(range(300))
        edges = [(i, j, rng.random()) for i, j in combinations(nodes, 2)]  # 44.850 cạnh
        elapsed, result = _best_time(lambda: kruskal(nodes, edges))
        assert elapsed < 1.0, f"K300 mất {elapsed:.3f}s"
        assert result.num_edges == 299
        assert result.total_weight == pytest.approx(_reference_msf_total(nodes, edges))

    def test_sparse_disconnected_graph_5000_vertices(self):
        rng = random.Random(9)
        nodes = [f"N{i}" for i in range(5000)]
        edges = [(rng.choice(nodes), rng.choice(nodes), rng.randint(-50, 50)) for _ in range(3000)]
        elapsed, result = _best_time(lambda: kruskal(nodes, edges, warn_if_disconnected=False))
        components = _component_partition(nodes, edges)
        assert elapsed < 1.0, f"đồ thị thưa mất {elapsed:.3f}s"
        assert len(components) > 1
        assert result.num_edges == len(nodes) - len(components)
        assert result.total_weight == pytest.approx(_reference_msf_total(nodes, edges))

    def test_large_scale_v20000_e100000(self):
        nodes, edges = _random_connected_graph(random.Random(10), 20_000, 100_000)
        elapsed, result = _best_time(lambda: kruskal(nodes, edges), runs=1)
        assert elapsed < 5.0, f"V=20000, E=100000 mất {elapsed:.3f}s"
        assert result.num_edges == 19_999
        assert result.total_weight == pytest.approx(_reference_msf_total(nodes, edges))

    def test_stress_graph_runs_under_a_tight_recursion_limit(self):
        nodes, edges = _random_connected_graph(random.Random(12), 1000, 10_000)
        result = _call_with_tight_recursion_limit(lambda: kruskal(nodes, edges))
        assert result.num_edges == 999

    @pytest.mark.parametrize("shape", ["path", "star"])
    def test_very_long_or_very_wide_trees_need_no_recursion(self, shape):
        # MST 50.000 cạnh: sắp xếp, duyệt cạnh, gom thành phần đều phải là vòng lặp,
        # chạy được dưới giới hạn đệ quy chỉ cao hơn ngăn xếp hiện tại 60 tầng.
        n = 50_000
        nodes = list(range(n))
        if shape == "star":
            edges = [(0, i, i) for i in range(1, n)]
        else:
            edges = [(i, i + 1, i) for i in range(n - 1)]
        result = _call_with_tight_recursion_limit(lambda: kruskal(nodes, edges))
        assert result.is_connected
        assert result.num_edges == n - 1
        assert result.total_weight == sum(w for _, _, w in edges)

    @pytest.mark.parametrize("chain_edge", [lambda i: (i + 1, i, i), lambda i: (i, i + 1, i)],
                             ids=["edges-(i+1,i)", "edges-(i,i+1)"])
    def test_adversarial_chain_cannot_make_the_dsu_degenerate(self, chain_edge):
        # Dựng chuỗi hợp nhất khiến DSU THIẾU Union by Rank suy biến thành đường thẳng sâu
        # 20.000 nút, rồi cho một cạnh nặng chạm vào nút sâu nhất (nút 0) để find() phải đi
        # hết đường. Cạnh (i+1, i) làm sụp DSU luôn "gắn gốc thứ hai vào gốc thứ nhất",
        # cạnh (i, i+1) làm sụp DSU luôn "gắn gốc thứ nhất vào gốc thứ hai": thử cả hai.
        # Có Union by Rank, cây luôn thấp (<= log2 n) nên chạy được dưới giới hạn đệ quy
        # chỉ cao hơn ngăn xếp 60 tầng; DSU suy biến + find đệ quy sẽ văng RecursionError.
        n = 20_000
        nodes = list(range(n + 1))  # đỉnh n lẻ loi, chỉ nối bằng cạnh nặng nhất
        edges = [chain_edge(i) for i in range(n - 1)] + [(0, n, n)]
        result = _call_with_tight_recursion_limit(lambda: kruskal(nodes, edges))
        assert result.is_connected
        assert result.num_edges == n
        assert result.total_weight == sum(range(n - 1)) + n

    def test_peak_memory_grows_linearly_with_edge_count(self):
        def peak_bytes(num_edges):
            nodes, edges = _random_connected_graph(random.Random(5), 1000, num_edges)
            was_tracing = tracemalloc.is_tracing()
            if not was_tracing:
                tracemalloc.start()
            baseline = tracemalloc.get_traced_memory()[0]
            tracemalloc.reset_peak()
            try:
                kruskal(nodes, edges)
                return tracemalloc.get_traced_memory()[1] - baseline
            finally:
                if not was_tracing:
                    tracemalloc.stop()

        small, large = peak_bytes(10_000), peak_bytes(40_000)
        assert small < 20 * 1024 * 1024  # E = 10.000 chỉ cần vài MB
        assert large < 8 * small  # E tăng 4 lần => bộ nhớ ~4 lần (O(E^2) sẽ là ~16 lần)