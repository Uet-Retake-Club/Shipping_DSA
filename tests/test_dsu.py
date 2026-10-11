"""Unit tests cho src/algorithms/dsu.py (Union-Find)."""

import random
import threading

import pytest

from src.algorithms.dsu import DSU


def _run_with_timeout(fn, seconds=5):
    """Chạy ``fn`` trong luồng phụ; nếu quá hạn thì báo lỗi thay vì treo cả bộ test.
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


def _root_rank(dsu, element):
    """Hạng của gốc tập chứa ``element`` (kiểm thử hộp trắng)."""
    return dsu._rank[dsu._index[dsu.find(element)]]


# ---------------------------------------------------------------------------
# Khởi tạo và quản lý phần tử
# ---------------------------------------------------------------------------
class TestConstruction:
    def test_empty(self):
        dsu = DSU()
        assert len(dsu) == 0
        assert dsu.count == 0
        assert dsu.components() == []

    def test_each_element_starts_alone(self):
        dsu = DSU(["A", "B", "C"])
        assert len(dsu) == 3
        assert dsu.count == 3
        assert dsu.find("A") == "A"
        assert not dsu.connected("A", "B")

    def test_duplicate_elements_counted_once(self):
        dsu = DSU(["A", "B", "A", "B", "A"])
        assert len(dsu) == 2
        assert dsu.count == 2

    def test_add_returns_true_only_for_new_element(self):
        dsu = DSU()
        assert dsu.add("X") is True
        assert dsu.add("X") is False
        assert len(dsu) == 1
        assert dsu.count == 1

    def test_add_existing_element_keeps_its_set(self):
        dsu = DSU(["A", "B"])
        dsu.union("A", "B")
        dsu.add("A")  # không được reset A về tập riêng
        assert dsu.connected("A", "B")
        assert dsu.count == 1

    def test_contains(self):
        dsu = DSU([1, 2])
        assert 1 in dsu
        assert 3 not in dsu

    def test_accepts_any_hashable_including_mixed_types(self):
        dsu = DSU(["H0", 7, (1, 2)])
        dsu.union("H0", 7)
        dsu.union(7, (1, 2))
        assert dsu.count == 1
        assert dsu.connected("H0", (1, 2))


# ---------------------------------------------------------------------------
# find / union / connected
# ---------------------------------------------------------------------------
class TestFindUnion:
    def test_find_unknown_element_raises_key_error(self):
        dsu = DSU(["A"])
        with pytest.raises(KeyError):
            dsu.find("Z")

    def test_union_unknown_element_raises_key_error(self):
        dsu = DSU(["A"])
        with pytest.raises(KeyError):
            dsu.union("A", "Z")
        with pytest.raises(KeyError):
            dsu.union("Z", "A")

    def test_failed_union_leaves_state_unchanged(self):
        dsu = DSU(["A", "B"])
        with pytest.raises(KeyError):
            dsu.union("A", "Z")
        assert dsu.count == 2
        assert not dsu.connected("A", "B")

    def test_union_merges_and_returns_true(self):
        dsu = DSU(["A", "B", "C"])
        assert dsu.union("A", "B") is True
        assert dsu.connected("A", "B")
        assert not dsu.connected("A", "C")
        assert dsu.count == 2

    def test_union_same_set_returns_false_and_keeps_count(self):
        dsu = DSU(["A", "B", "C"])
        dsu.union("A", "B")
        assert dsu.union("A", "B") is False
        assert dsu.union("B", "A") is False
        assert dsu.count == 2

    def test_union_with_itself_returns_false(self):
        dsu = DSU(["A"])
        assert dsu.union("A", "A") is False
        assert dsu.count == 1

    def test_cycle_detection_as_used_by_kruskal(self):
        # Tam giác A-B-C: hai cạnh đầu hợp nhất được, cạnh thứ ba tạo chu trình.
        dsu = DSU(["A", "B", "C"])
        assert dsu.union("A", "B") is True
        assert dsu.union("B", "C") is True
        assert dsu.union("A", "C") is False

    def test_connected_is_symmetric_and_transitive(self):
        dsu = DSU(range(6))
        dsu.union(0, 1)
        dsu.union(1, 2)
        dsu.union(4, 5)
        assert dsu.connected(0, 2) and dsu.connected(2, 0)
        assert dsu.connected(4, 5)
        assert not dsu.connected(0, 4)
        assert not dsu.connected(3, 0)
        assert dsu.connected(3, 3)

    def test_find_returns_same_root_for_whole_set(self):
        dsu = DSU(range(8))
        for i in range(7):
            dsu.union(i, i + 1)
        assert len({dsu.find(i) for i in range(8)}) == 1

    def test_count_decreases_by_one_per_successful_union(self):
        dsu = DSU(range(10))
        for i in range(9):
            assert dsu.count == 10 - i
            dsu.union(i, i + 1)
        assert dsu.count == 1


# ---------------------------------------------------------------------------
# components()
# ---------------------------------------------------------------------------
class TestComponents:
    def test_groups_and_order_are_deterministic(self):
        dsu = DSU(["A", "B", "C", "D", "E"])
        dsu.union("D", "B")
        dsu.union("E", "A")
        assert dsu.components() == [["A", "E"], ["B", "D"], ["C"]]

    def test_partition_covers_all_elements_exactly_once(self):
        dsu = DSU(range(20))
        for a, b in [(0, 5), (5, 9), (2, 3), (10, 11), (11, 12), (12, 10)]:
            dsu.union(a, b)
        groups = dsu.components()
        flat = [x for g in groups for x in g]
        assert sorted(flat) == list(range(20))
        assert len(groups) == dsu.count


# ---------------------------------------------------------------------------
# Path Compression (kiểm thử hộp trắng qua thuộc tính nội bộ _parent)
# ---------------------------------------------------------------------------
class TestPathCompression:
    def test_find_flattens_a_chain(self):
        dsu = DSU(range(6))
        # Dựng thủ công chuỗi 5 -> 4 -> 3 -> 2 -> 1 -> 0 (gốc là 0).
        # Phần tử range(6) có chỉ số trùng giá trị nên _parent[i] là cha của i.
        dsu._parent = [0, 0, 1, 2, 3, 4]

        assert dsu.find(5) == 0
        # Sau find(5), mọi nút trên đường đi phải trỏ thẳng về gốc.
        assert dsu._parent == [0, 0, 0, 0, 0, 0]

    def test_find_on_root_and_child_is_stable(self):
        dsu = DSU(range(3))
        dsu._parent = [0, 0, 0]
        assert dsu.find(0) == 0
        assert dsu.find(1) == 0
        assert dsu._parent == [0, 0, 0]

    def test_compression_does_not_change_answers(self):
        dsu = DSU(range(6))
        dsu._parent = [0, 0, 1, 2, 3, 4]
        first = [dsu.find(i) for i in range(6)]
        second = [dsu.find(i) for i in range(6)]
        assert first == second == [0] * 6

    def test_very_deep_chain_does_not_hit_recursion_limit(self):
        # find() phải là vòng lặp: một chuỗi sâu hơn giới hạn đệ quy của Python
        # (mặc định ~1000) sẽ làm bản cài đặt đệ quy sụp đổ.
        n = 50_000
        dsu = DSU(range(n))
        dsu._parent = [max(i - 1, 0) for i in range(n)]
        assert dsu.find(n - 1) == 0
        assert dsu._parent[n - 1] == 0
        assert dsu._parent[n // 2] == 0


# ---------------------------------------------------------------------------
# Union by Rank (kiểm thử hộp trắng qua thuộc tính nội bộ _rank)
# ---------------------------------------------------------------------------
class TestUnionByRank:
    def test_equal_rank_merge_raises_rank_by_one(self):
        dsu = DSU(range(2))
        dsu.union(0, 1)
        assert _root_rank(dsu, 0) == 1

    def test_chain_of_unions_keeps_tree_shallow(self):
        # Luôn gắn phần tử đơn lẻ (hạng 0) vào cây hiện có: hạng gốc không tăng
        # quá 1. Nếu cài đặt "gắn tùy ý" thì cây sẽ cao dần.
        dsu = DSU(range(10))
        for i in range(1, 10):
            dsu.union(0, i)
        assert _root_rank(dsu, 0) == 1
        assert dsu.count == 1

    def test_balanced_merging_gives_logarithmic_rank(self):
        dsu = DSU(range(8))
        for a, b in [(0, 1), (2, 3), (4, 5), (6, 7)]:
            dsu.union(a, b)
        dsu.union(0, 2)
        dsu.union(4, 6)
        dsu.union(0, 4)
        assert dsu.count == 1
        assert _root_rank(dsu, 0) == 3  # log2(8)

    def test_lower_rank_attached_under_higher_rank_root(self):
        dsu = DSU(range(5))
        dsu.union(0, 1)
        dsu.union(2, 3)
        dsu.union(0, 2)  # cây hạng 2 gồm {0, 1, 2, 3}
        big_root = dsu.find(0)
        assert _root_rank(dsu, big_root) == 2

        dsu.union(4, 3)  # phần tử đơn (hạng 0) hợp nhất với cây hạng 2
        assert dsu.find(4) == big_root  # gốc của cây lớn phải được giữ nguyên
        assert _root_rank(dsu, big_root) == 2  # và hạng không tăng

        # Đổi thứ tự đối số phải cho cùng kết quả về gốc và hạng.
        dsu2 = DSU(range(5))
        dsu2.union(0, 1)
        dsu2.union(2, 3)
        dsu2.union(0, 2)
        big_root2 = dsu2.find(0)
        dsu2.union(3, 4)
        assert dsu2.find(4) == big_root2
        assert _root_rank(dsu2, big_root2) == 2


# ---------------------------------------------------------------------------
# So sánh với cài đặt ngây thơ (gán nhãn) trên dữ liệu ngẫu nhiên
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("seed", range(20))
def test_matches_naive_labeling_on_random_operations(seed):
    rng = random.Random(seed)
    n = rng.randint(1, 30)
    dsu = DSU(range(n))
    label = list(range(n))  # cài đặt đối chứng: gán nhãn, gộp thì đổi nhãn

    for _ in range(rng.randint(0, 60)):
        a, b = rng.randrange(n), rng.randrange(n)
        expected_merge = label[a] != label[b]
        assert dsu.union(a, b) == expected_merge
        if expected_merge:
            old, new = label[b], label[a]
            label = [new if x == old else x for x in label]

    assert dsu.count == len(set(label))
    for a in range(n):
        for b in range(n):
            assert dsu.connected(a, b) == (label[a] == label[b])


def test_repr_reports_element_and_set_counts():
    dsu = DSU(["A", "B", "C"])
    dsu.union("A", "B")
    assert repr(dsu) == "DSU(elements=3, sets=2)"


# ---------------------------------------------------------------------------
# Hồi quy: phần tử "lạ" không được làm treo hay hỏng DSU
# ---------------------------------------------------------------------------
class TestHostileElements:
    def test_nan_element_does_not_hang(self):
        # float("nan") != float("nan"): bản cài đặt so sánh phần tử trực tiếp sẽ
        # lặp vô hạn khi tìm gốc. Chỉ số nguyên nội bộ tránh được lỗi này.
        nan = float("nan")

        def scenario():
            dsu = DSU([nan, "B"])
            assert dsu.find(nan) is nan
            assert dsu.union(nan, nan) is False
            assert dsu.connected(nan, nan) is True
            assert dsu.union(nan, "B") is True
            assert dsu.connected(nan, "B") is True
            return dsu.count

        assert _run_with_timeout(scenario) == 1

    @pytest.mark.parametrize("bad", [[1], {"a": 1}, {1, 2}])
    def test_unhashable_element_raises_type_error(self, bad):
        dsu = DSU(["A"])
        with pytest.raises(TypeError):
            dsu.add(bad)
        with pytest.raises(TypeError):
            dsu.find(bad)
        with pytest.raises(TypeError):
            dsu.union("A", bad)
        assert len(dsu) == 1 and dsu.count == 1  # trạng thái không bị hỏng

    def test_find_returns_the_stored_object_for_equal_lookups(self):
        stored = "".join(["H", "0"])
        lookup = "".join(["H", "0"])
        assert stored is not lookup
        dsu = DSU([stored])
        assert dsu.find(lookup) is stored