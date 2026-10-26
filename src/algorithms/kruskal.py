
from __future__ import annotations

import math
import warnings
from collections.abc import Hashable, Iterable, Mapping, Sequence
from dataclasses import dataclass
from numbers import Real
from typing import Any

from .dsu import DSU

__all__ = ["MSTResult", "kruskal", "kruskal_mst"]

# Một cạnh sau khi chuẩn hóa: (u, v, weight, đối tượng cạnh gốc).
_ParsedEdge = tuple[Hashable, Hashable, Real, Any]


@dataclass(frozen=True)
class MSTResult:
    """
    Kết quả của thuật toán Kruskal.

    Attributes:
        edges: Các cạnh thuộc cây/rừng bao trùm nhỏ nhất, theo thứ tự được
            chọn (trọng số không giảm). Mỗi cạnh là một dict (bản sao, giữ
            nguyên các trường phụ như ``road_type``).
        total_weight: Tổng trọng số các cạnh đã chọn (kiểu float).
        num_nodes: Tổng số đỉnh của đồ thị.
        components: Danh sách các thành phần liên thông, mỗi thành phần là
            danh sách id đỉnh. Có đúng một phần tử nếu đồ thị liên thông.
    """

    edges: list[dict[str, Any]]
    total_weight: float
    num_nodes: int
    components: list[list[Hashable]]

    @property
    def num_edges(self) -> int:
        """Số cạnh trong cây/rừng bao trùm (= num_nodes - num_components)."""
        return len(self.edges)

    @property
    def num_components(self) -> int:
        """Số thành phần liên thông của đồ thị đầu vào."""
        return len(self.components)

    @property
    def is_connected(self) -> bool:
        """True nếu đồ thị liên thông (kết quả là một cây MST duy nhất)."""
        return self.num_components <= 1


def _node_id(node: Any) -> Hashable:
    """Lấy id đỉnh và kiểm tra hợp lệ: hashable và không phải NaN."""
    node_id: Hashable
    if isinstance(node, Mapping):
        if "id" not in node:
            raise ValueError(f"Node thiếu trường 'id': {dict(node)!r}")
        node_id = node["id"]
    else:
        node_id = node

    try:
        hash(node_id)
    except TypeError:
        raise ValueError(
            f"id đỉnh phải là giá trị hashable, nhận được {node_id!r}"
        ) from None
    if node_id != node_id:  # chỉ NaN mới không bằng chính nó
        raise ValueError(f"id đỉnh không hợp lệ (NaN): {node_id!r}")
    return node_id


def _is_valid_weight(weight: Any) -> bool:
    """Trọng số phải là số thực hữu hạn (không bool, NaN, vô cực, quá lớn)."""
    kind = type(weight)
    if kind is not float and kind is not int:  # đường chậm cho kiểu hiếm gặp
        if isinstance(weight, bool) or not isinstance(weight, Real):
            return False
    try:
        return math.isfinite(weight)
    except OverflowError:  # số nguyên / phân số lớn hơn phạm vi float
        return False


def _parse_edge(edge: Any, index: int) -> _ParsedEdge:
    """Chuẩn hóa một cạnh (dict hoặc ``(u, v, weight, ...)``) và kiểm tra."""
    if type(edge) is dict or isinstance(edge, Mapping):
        try:
            u, v, weight = edge["u"], edge["v"], edge["weight"]
        except KeyError as exc:
            raise ValueError(f"edges[{index}] thiếu trường {exc}") from None
    elif (
        (type(edge) is tuple or type(edge) is list)
        or (isinstance(edge, Sequence) and not isinstance(edge, (str, bytes)))
    ) and len(edge) >= 3:
        u, v, weight = edge[0], edge[1], edge[2]
    else:
        raise ValueError(
            f"edges[{index}] phải là dict có u/v/weight hoặc tuple "
            f"(u, v, weight), nhận được {edge!r}"
        )

    if not _is_valid_weight(weight):
        raise ValueError(
            f"edges[{index}]: trọng số phải là số thực hữu hạn, "
            f"nhận được {weight!r}"
        )
    return u, v, weight, edge


def _edge_record(
    edge: Any, u: Hashable, v: Hashable, weight: Real
) -> dict[str, Any]:
    """Tạo bản ghi trả về (bản sao) cho một cạnh được chọn."""
    if isinstance(edge, Mapping):
        return dict(edge)  # bản sao nông, giữ nguyên trường phụ (road_type)
    return {"u": u, "v": v, "weight": weight}


def _check_endpoints(dsu: DSU, u: Any, v: Any, index: int) -> None:
    """Hai đầu mút của cạnh phải là đỉnh đã khai báo (và hashable)."""
    try:
        for endpoint in (u, v):
            if endpoint not in dsu:
                raise ValueError(
                    f"edges[{index}] trỏ tới đỉnh không tồn tại: "
                    f"{endpoint!r}"
                )
    except TypeError:  # endpoint không hashable
        raise ValueError(
            f"edges[{index}]: id đỉnh phải là giá trị hashable, "
            f"nhận được {u!r}, {v!r}"
        ) from None


def _endpoints_in_order(edges: Sequence[Any]) -> list[Hashable]:
    """Suy ra danh sách đỉnh từ đầu mút các cạnh (theo thứ tự xuất hiện)."""
    seen: dict[Hashable, None] = {}
    for index, edge in enumerate(edges):
        u, v, _, _ = _parse_edge(edge, index)
        try:
            seen.setdefault(u)
            seen.setdefault(v)
        except TypeError:  # đầu mút không hashable
            raise ValueError(
                f"edges[{index}]: id đỉnh phải là giá trị hashable, "
                f"nhận được {u!r}, {v!r}"
            ) from None
    return list(seen)


def _warn_disconnected(result: MSTResult, stacklevel: int) -> None:
    """
    Phát ``UserWarning`` nếu mạng lưới bị chia cắt.

    ``stacklevel`` được hàm công khai truyền vào để cảnh báo trỏ đúng tới
    dòng gọi của người dùng (mặc định Python chỉ hiện mỗi vị trí một lần,
    nên nếu trỏ vào bên trong module này, các lần gọi sau sẽ bị nuốt mất).
    """
    if result.is_connected:
        return
    warnings.warn(
        f"Đồ thị không liên thông: mạng lưới bị chia cắt thành "
        f"{result.num_components} thành phần liên thông. "
        f"Kết quả là Rừng cây bao trùm nhỏ nhất gồm {result.num_edges} cạnh.",
        UserWarning,
        stacklevel=stacklevel,
    )


def kruskal(
    nodes: Iterable[Any],
    edges: Iterable[Any],
    *,
    warn_if_disconnected: bool = True,
) -> MSTResult:
    """
    Tìm Cây (hoặc Rừng) bao trùm nhỏ nhất của đồ thị vô hướng có trọng số.

    Args:
        nodes: Các đỉnh. Mỗi phần tử là id hashable (``"H0"``, ``3``, ...)
            hoặc dict có khóa ``"id"`` (định dạng của ``load_nodes_csv`` /
            file JSON chuẩn).
        edges: Các cạnh vô hướng. Mỗi phần tử là dict có ``u``, ``v``,
            ``weight`` (định dạng chuẩn của nhóm) hoặc tuple/list
            ``(u, v, weight, ...)``. Cạnh song song và khuyên (self-loop)
            được chấp nhận: khuyên bị bỏ qua, còn với cạnh song song chỉ
            cạnh nhẹ nhất có thể được chọn. Trọng số có thể âm hoặc bằng 0.
        warn_if_disconnected: Nếu True (mặc định), phát ``UserWarning`` khi
            đồ thị không liên thông (mạng lưới bị chia cắt).

    Returns:
        ``MSTResult`` chứa các cạnh được chọn, tổng trọng số và các thành
        phần liên thông. Nếu đồ thị liên thông thì có đúng V-1 cạnh; nếu
        không liên thông thì có V-C cạnh với C là số thành phần liên thông.

    Raises:
        ValueError: id đỉnh trùng, không hashable hoặc là NaN; cạnh thiếu
            trường hoặc sai định dạng; trọng số không phải số thực hữu hạn;
            cạnh trỏ tới đỉnh không tồn tại; tổng trọng số vượt quá phạm vi
            số thực float.
        TypeError: nếu ``nodes`` hoặc ``edges`` không phải đối tượng duyệt
            được.

    Ghi chú về tính duy nhất: khi có nhiều cạnh cùng trọng số, MST có thể
    không duy nhất. Hàm dùng sắp xếp ổn định theo trọng số nên kết quả xác
    định theo thứ tự cạnh đầu vào; *tổng trọng số* luôn giống nhau với mọi
    cách chọn hợp lệ.
    """
    # 1. Khởi tạo DSU: mỗi đỉnh là một cây riêng biệt.
    dsu = DSU()
    for node in nodes:
        node_id = _node_id(node)
        if not dsu.add(node_id):
            raise ValueError(f"Trùng id đỉnh: {node_id!r}")
    num_nodes = len(dsu)

    # 2. Kiểm tra toàn bộ cạnh TRƯỚC khi chạy, để việc dừng sớm ở bước 4
    #    không che giấu dữ liệu lỗi nằm ở cuối danh sách.
    parsed: list[_ParsedEdge] = []
    for index, edge in enumerate(edges):
        u, v, weight, original = _parse_edge(edge, index)
        _check_endpoints(dsu, u, v, index)
        parsed.append((u, v, weight, original))

    # 3. Sắp xếp cạnh theo trọng số tăng dần (sorted ổn định: giữ thứ tự đầu
    #    vào giữa các cạnh cùng trọng số, và không cần so sánh id đỉnh).
    parsed.sort(key=lambda item: item[2])

    # 4. Duyệt cạnh: nhận cạnh nếu nối hai thành phần khác nhau.
    mst_edges: list[dict[str, Any]] = []
    mst_weights: list[Real] = []
    for u, v, weight, original in parsed:
        if dsu.count <= 1:
            break  # đã liên thông hết, các cạnh còn lại đều tạo chu trình
        if dsu.union(u, v):
            mst_edges.append(_edge_record(original, u, v, weight))
            mst_weights.append(weight)

    # fsum cho tổng chính xác, không phụ thuộc thứ tự cộng, nên tổng của
    # Kruskal và Prim trên cùng đồ thị không bị lệch do sai số dấu phẩy động.
    try:
        total_weight = math.fsum(mst_weights)
    except OverflowError:
        raise ValueError(
            "Tổng trọng số của MST vượt quá phạm vi số thực float"
        ) from None

    result = MSTResult(
        edges=mst_edges,
        total_weight=total_weight,
        num_nodes=num_nodes,
        components=dsu.components(),
    )
    if warn_if_disconnected:
        _warn_disconnected(result, stacklevel=3)
    return result


def kruskal_mst(
    edges: Iterable[Any],
    *,
    nodes: Iterable[Any] | None = None,
    warn_if_disconnected: bool = True,
) -> tuple[list[dict[str, Any]], float]:
    """
    Bản gọn của :func:`kruskal`: trả về ``(mst_edges, total_weight)``.

    Args:
        edges: Các cạnh vô hướng, mỗi phần tử là dict ``{"u", "v",
            "weight", ...}`` hoặc tuple/list ``(u, v, weight, ...)``.
        nodes: Các đỉnh của đồ thị (keyword-only, tránh nhầm thứ tự với
            :func:`kruskal`). Nếu bỏ qua, tập đỉnh được suy ra từ đầu mút
            các cạnh, nên đỉnh cô lập (không có cạnh nào) sẽ không được biết
            tới. Hãy truyền ``nodes`` khi đồ thị có thể có đỉnh cô lập, hoặc
            khi cần phân biệt đồ thị rỗng với đồ thị chỉ có một đỉnh.
        warn_if_disconnected: Như :func:`kruskal`.

    Returns:
        Bộ ``(mst_edges, total_weight)``: danh sách cạnh của cây/rừng bao
        trùm nhỏ nhất (trọng số không giảm) và tổng trọng số của chúng. Cần
        thêm số thành phần liên thông thì dùng :func:`kruskal`.

    Raises:
        ValueError: như :func:`kruskal`.
        TypeError: như :func:`kruskal`.
    """
    edge_list = list(edges)  # ``edges`` có thể là generator: cần duyệt 2 lần
    if nodes is None:
        nodes = _endpoints_in_order(edge_list)
    result = kruskal(nodes, edge_list, warn_if_disconnected=False)
    if warn_if_disconnected:
        _warn_disconnected(result, stacklevel=3)
    return result.edges, result.total_weight