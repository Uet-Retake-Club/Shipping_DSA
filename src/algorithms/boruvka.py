"""
Borůvka's Algorithm for Minimum Spanning Tree (MST).
Phục vụ đề tài Thiết kế mạng lưới vận chuyển thông minh (Shipping_DSA).

Nguyên lý hoạt động:
1. Khởi tạo mỗi đỉnh là một thành phần liên thông riêng biệt (Component).
2. Ở mỗi vòng lặp (Round):
   - Với mỗi component, tìm cạnh nối ra ngoài có trọng số nhỏ nhất (Cheapest Outgoing Edge).
   - Thêm tất cả các cạnh rẻ nhất này vào cây khung và hợp nhất các component (sử dụng DSU).
3. Lặp lại cho đến khi chỉ còn 1 component duy nhất (đồ thị liên thông)
   hoặc không còn cạnh nào để kết nối các component (rừng cây khung - MST Forest).

Độ phức tạp: O(E log V).
"""

from dataclasses import dataclass, field
import json
import os
import sys
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple, Union

# Đảm bảo import được module DSU dù chạy trực tiếp hay qua package
try:
    from src.algorithms.dsu import DisjointSetUnion
except ImportError:
    from dsu import DisjointSetUnion  # type: ignore


@dataclass
class EdgeRecord:
    """Đại diện cho một cạnh có định danh và metadata."""
    edge_id: int
    u: Any
    v: Any
    weight: float
    data: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Chuyển đổi thành từ điển chuẩn theo format dự án."""
        res = {"u": self.u, "v": self.v, "weight": self.weight}
        if self.data:
            res.update(self.data)
        return res


@dataclass
class BoruvkaResult:
    """Kết quả trả về sau khi chạy thuật toán Boruvka."""
    mst_edges: List[Dict[str, Any]]
    total_weight: float
    num_components: int
    is_connected: bool
    iterations: int
    rounds_log: List[Dict[str, Any]]

    def __repr__(self) -> str:
        return (
            f"BoruvkaResult(num_edges={len(self.mst_edges)}, "
            f"total_weight={self.total_weight:.2f}, "
            f"components={self.num_components}, "
            f"iterations={self.iterations}, "
            f"is_connected={self.is_connected})"
        )


def _normalize_edge(
    raw_edge: Union[Dict[str, Any], Tuple, List],
    edge_id: int,
) -> Optional[EdgeRecord]:
    """
    Chuẩn hóa cạnh từ dạng Dict, Tuple hoặc List về EdgeRecord.
    Bỏ qua khuyên (self-loop: u == v).
    """
    if isinstance(raw_edge, dict):
        u = raw_edge["u"]
        v = raw_edge["v"]
        weight = float(raw_edge["weight"])
        extra_data = {k: val for k, val in raw_edge.items() if k not in ("u", "v", "weight")}
    elif isinstance(raw_edge, (tuple, list)):
        if len(raw_edge) < 3:
            raise ValueError(f"Edge tuple phải có ít nhất 3 phần tử (u, v, weight): {raw_edge}")
        u = raw_edge[0]
        v = raw_edge[1]
        weight = float(raw_edge[2])
        extra_data = raw_edge[3] if len(raw_edge) > 3 and isinstance(raw_edge[3], dict) else {}
    else:
        raise TypeError(f"Dạng dữ liệu cạnh không hỗ trợ: {type(raw_edge)}")

    if u == v:
        # Bỏ qua khuyên vì không bao giờ thuộc cây khung
        return None

    return EdgeRecord(edge_id=edge_id, u=u, v=v, weight=weight, data=extra_data)


def boruvka_mst(
    edges: Iterable[Union[Dict[str, Any], Tuple, List]],
    nodes: Optional[Iterable[Any]] = None,
) -> BoruvkaResult:
    """
    Chạy thuật toán Borůvka để tìm Cây khung nhỏ nhất (MST) hoặc Rừng cây khung (MST Forest).

    Args:
        edges: Danh sách các cạnh (dạng dict `{'u': ..., 'v': ..., 'weight': ...}`
               hoặc tuple `(u, v, weight)`).
        nodes: Danh sách tập đỉnh (tùy chọn). Nếu không truyền, tập đỉnh sẽ được
               tự động trích xuất từ các cạnh.

    Returns:
        BoruvkaResult chứa danh sách cạnh MST, tổng trọng số, số thành phần liên thông,
        và lịch sử chi tiết từng vòng lặp.
    """
    # 1. Trích xuất danh sách cạnh chuẩn hóa và tập đỉnh
    normalized_edges: List[EdgeRecord] = []
    discovered_nodes: Set[Any] = set()

    for idx, e in enumerate(edges):
        rec = _normalize_edge(e, edge_id=idx)
        if rec is not None:
            normalized_edges.append(rec)
            discovered_nodes.add(rec.u)
            discovered_nodes.add(rec.v)

    all_nodes: Set[Any] = set(nodes) if nodes is not None else discovered_nodes

    # Trường hợp đặc biệt: đồ thị rỗng hoặc chỉ có 1 đỉnh
    if len(all_nodes) <= 1:
        return BoruvkaResult(
            mst_edges=[],
            total_weight=0.0,
            num_components=len(all_nodes),
            is_connected=True,
            iterations=0,
            rounds_log=[],
        )

    # 2. Khởi tạo Disjoint Set Union
    dsu = DisjointSetUnion(all_nodes)
    mst_edges: List[EdgeRecord] = []
    total_weight = 0.0
    rounds_log: List[Dict[str, Any]] = []
    iteration = 0

    # 3. Lặp lại các pha của Boruvka
    while dsu.count > 1:
        iteration += 1
        num_components_before = dsu.count

        # Map lưu cạnh rẻ nhất cho mỗi component (root -> EdgeRecord)
        # Tie-breaking: so sánh (weight, edge_id) để đảm bảo không tạo chu trình
        cheapest: Dict[Any, EdgeRecord] = {}

        for edge in normalized_edges:
            root_u = dsu.find(edge.u)
            root_v = dsu.find(edge.v)

            # Cạnh nội bộ cùng 1 component thì bỏ qua
            if root_u == root_v:
                continue

            # Cập nhật cạnh tốt nhất cho component chứa u
            if root_u not in cheapest or (edge.weight, edge.edge_id) < (
                cheapest[root_u].weight,
                cheapest[root_u].edge_id,
            ):
                cheapest[root_u] = edge

            # Cập nhật cạnh tốt nhất cho component chứa v
            if root_v not in cheapest or (edge.weight, edge.edge_id) < (
                cheapest[root_v].weight,
                cheapest[root_v].edge_id,
            ):
                cheapest[root_v] = edge

        # Nếu không còn cạnh nào kết nối giữa các component khác nhau -> Đồ thị bị chia cắt
        if not cheapest:
            break

        added_edges_this_round: List[EdgeRecord] = []

        # Thêm các cạnh rẻ nhất đã tìm được vào MST
        for comp_root, edge in cheapest.items():
            # Kiểm tra nếu 2 đầu mút chưa được gộp bởi một cạnh khác trong cùng vòng này
            if dsu.union(edge.u, edge.v):
                mst_edges.append(edge)
                total_weight += edge.weight
                added_edges_this_round.append(edge)

        rounds_log.append({
            "round": iteration,
            "components_before": num_components_before,
            "components_after": dsu.count,
            "edges_added": [e.to_dict() for e in added_edges_this_round],
            "count_added": len(added_edges_this_round),
        })

        # Nếu vòng này không thể kết nạp thêm cạnh nào, dừng lại để tránh lặp vô tận
        if len(added_edges_this_round) == 0:
            break

    is_connected = (dsu.count == 1)

    return BoruvkaResult(
        mst_edges=[e.to_dict() for e in mst_edges],
        total_weight=round(total_weight, 4),
        num_components=dsu.count,
        is_connected=is_connected,
        iterations=iteration,
        rounds_log=rounds_log,
    )


def boruvka_from_json(json_filepath: str) -> BoruvkaResult:
    """Đọc dữ liệu mạng lưới từ file JSON chuẩn và chạy thuật toán Boruvka."""
    if not os.path.exists(json_filepath):
        raise FileNotFoundError(f"Không tìm thấy file: {json_filepath}")

    with open(json_filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    node_ids = [n["id"] for n in data.get("nodes", [])]
    edges = data.get("edges", [])

    return boruvka_mst(edges=edges, nodes=node_ids)
