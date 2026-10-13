import os
import sys
from collections import defaultdict
from typing import Any, Optional

try:
    from src.algorithms.min_heap import MinHeap
    from src.algorithms.indexed_min_heap import IndexedMinHeap
except ImportError:
    from min_heap import MinHeap
    from indexed_min_heap import IndexedMinHeap


def lazyPrims(
    n: Optional[int | list] = None,
    edges: Optional[list] = None,
    start: Optional[Any] = None,
    nodes: Optional[list | set] = None
) -> tuple[float | int, list[tuple], bool]:
    """
    Thuật toán Lazy Prim tìm cây khung nhỏ nhất với MinHeap tự cài đặt.

    Args:
        n: Số lượng đỉnh (hoặc danh sách edges nếu gọi rút gọn).
        edges: Danh sách các cạnh [(u, v, weight), ...].
        start: Đỉnh xuất phát (mặc định: tự chọn đỉnh đầu tiên).
        nodes: Danh sách/tập hợp các đỉnh (phát hiện đỉnh cô lập).

    Returns:
        tuple: (total_weight, mst_edges, is_connected)
            - total_weight: Tổng trọng số của MST.
            - mst_edges: Danh sách cạnh kết nạp vào cây [(from_u, to_v, weight), ...].
            - is_connected: True nếu cây khung kết nối toàn bộ mạng lưới, False nếu đồ thị bị phân mảnh.
    """
    # Xử lý trường hợp người dùng truyền thẳng danh sách cạnh vào vị trí đầu tiên
    if isinstance(n, list) and edges is None:
        edges = n
        n = None

    if edges is None:
        edges = []

    # 1. Thu thập tập hợp đỉnh
    if nodes is not None:
        all_nodes = set(nodes)
    else:
        all_nodes = set()
        for u, v, _ in edges:
            all_nodes.add(u)
            all_nodes.add(v)

    # Nếu truyền số đỉnh n cụ thể (int), xác định tổng số đỉnh cần kết nối
    if isinstance(n, int):
        total_nodes_count = n
    else:
        total_nodes_count = len(all_nodes)

    # Trường hợp biên: đồ thị rỗng hoặc chỉ có 1 đỉnh
    if total_nodes_count <= 1:
        return 0, [], True

    # Nếu không có cạnh nào mà số đỉnh > 1 -> đồ thị không liên thông
    if not edges:
        return 0, [], False

    # 2. Xây dựng danh sách kề
    adj = defaultdict(list)
    for u, v, w in edges:
        adj[u].append((w, v))
        adj[v].append((w, u))

    # 3. Chọn đỉnh xuất phát nếu chưa có
    if start is None:
        if all_nodes:
            start = next(iter(all_nodes))
        else:
            start = edges[0][0]

    visited = set()
    pq = MinHeap()
    total_weight = 0
    mst_edges = []

    def visit(u):
        visited.add(u)
        for weight, to_node in adj[u]:
            if to_node not in visited:
                pq.push((weight, to_node, u))

    # Bắt đầu duyệt từ đỉnh xuất phát
    visit(start)

    while not pq.is_empty() and len(mst_edges) < total_nodes_count - 1:
        weight, to_node, from_node = pq.pop()

        if to_node in visited:
            continue

        total_weight += weight
        mst_edges.append((from_node, to_node, weight))

        # Thêm đỉnh mới vào cây khung
        visit(to_node)

    # Kiểm tra liên thông: cây khung phải có đúng V - 1 cạnh
    is_connected = (len(mst_edges) == total_nodes_count - 1)
    return total_weight, mst_edges, is_connected


def eagerPrims(
    n: Optional[int | list] = None,
    edges: Optional[list] = None,
    start: Optional[Any] = None,
    nodes: Optional[list | set] = None
) -> tuple[float | int, list[tuple], bool]:
    """
    Thuật toán Eager Prim tìm cây khung nhỏ nhất (MST) tối ưu bộ nhớ O(V).
    Sử dụng IndexedMinHeap hỗ trợ thao tác decrease_key.

    Args:
        n: Số lượng đỉnh (hoặc danh sách edges nếu gọi rút gọn).
        edges: Danh sách các cạnh [(u, v, weight), ...].
        start: Đỉnh xuất phát (mặc định: tự chọn đỉnh đầu tiên).
        nodes: Danh sách/tập hợp các đỉnh (phát hiện đỉnh cô lập).

    Returns:
        tuple: (total_weight, mst_edges, is_connected)
    """
    if isinstance(n, list) and edges is None:
        edges = n
        n = None

    if edges is None:
        edges = []

    # 1. Thu thập tập hợp đỉnh
    if nodes is not None:
        all_nodes = set(nodes)
    else:
        all_nodes = set()
        for u, v, _ in edges:
            all_nodes.add(u)
            all_nodes.add(v)

    if isinstance(n, int):
        total_nodes_count = n
    else:
        total_nodes_count = len(all_nodes)

    if total_nodes_count <= 1:
        return 0, [], True

    if not edges:
        return 0, [], False

    # 2. Xây dựng danh sách kề
    adj = defaultdict(list)
    for u, v, w in edges:
        adj[u].append((w, v))
        adj[v].append((w, u))

    # 3. Chọn đỉnh xuất phát
    if start is None:
        if all_nodes:
            start = next(iter(all_nodes))
        else:
            start = edges[0][0]

    # dist_to[v]: Trọng số nhỏ nhất hiện tại của cạnh nối v vào MST
    dist_to = {u: float('inf') for u in all_nodes}
    # edge_to[v]: Cạnh tốt nhất kết nối v vào MST (u, v, weight)
    edge_to = {u: None for u in all_nodes}
    visited = set()

    # IndexedMinHeap lưu các đỉnh chưa vào MST cùng khoảng cách dist_to của chúng
    pq = IndexedMinHeap()

    dist_to[start] = 0
    pq.insert(start, 0)

    while not pq.is_empty():
        # Lấy đỉnh có khoảng cách tới cây khung nhỏ nhất
        u, _ = pq.pop()
        visited.add(u)

        # Duyệt các cạnh kề của u
        for weight, to_node in adj[u]:
            if to_node in visited:
                continue

            # Nếu tìm thấy đường nối ngắn hơn tới to_node
            if weight < dist_to[to_node]:
                dist_to[to_node] = weight
                edge_to[to_node] = (u, to_node, weight)

                if pq.contains(to_node):
                    pq.decrease_key(to_node, weight)
                else:
                    pq.insert(to_node, weight)

    # Thu thập các cạnh của MST
    mst_edges = [edge for node, edge in edge_to.items() if edge is not None]
    total_weight = sum(weight for _, _, weight in mst_edges)
    is_connected = (len(mst_edges) == total_nodes_count - 1)

    return total_weight, mst_edges, is_connected



if __name__ == '__main__':
    # Kiểm tra xem có dữ liệu truyền qua pipe/stdin không
    # Nếu chạy trực tiếp bằng lệnh `python prim.py`, tự động chạy dữ liệu mẫu
    if sys.stdin.isatty():
        print("=== CHẠY THỬ NGHIỆM THUẬT TOÁN PRIM VỚI DỮ LIỆU MẪU ===")
        sample_n = 5
        sample_edges = [
            (1, 2, 3),
            (1, 3, 4),
            (2, 3, 1),
            (2, 4, 7),
            (3, 5, 2),
            (4, 5, 5),
        ]
        sample_start = 1

        cost_lazy, edges_lazy, conn_lazy = lazyPrims(sample_n, sample_edges, sample_start)
        cost_eager, edges_eager, conn_eager = eagerPrims(sample_n, sample_edges, sample_start)

        print("[LAZY PRIM]")
        print(f"  Tổng trọng số MST: {cost_lazy}")
        print(f"  Các cạnh MST: {edges_lazy}")
        print(f"  Liên thông: {conn_lazy}")

        print("\n[EAGER PRIM (Indexed Min Heap)]")
        print(f"  Tổng trọng số MST: {cost_eager}")
        print(f"  Các cạnh MST: {edges_eager}")
        print(f"  Liên thông: {conn_eager}")

        print(f"\n=> Kết quả hai biến thể khớp nhau 100%: {cost_lazy == cost_eager and conn_lazy == conn_eager}")
    else:
        first_multiple_input = input().rstrip().split()
        n = int(first_multiple_input[0])
        m = int(first_multiple_input[1])
        edges = []
        for _ in range(m):
            edges.append(list(map(int, input().rstrip().split())))
        start = int(input().strip())
        cost, tree_edges, _ = eagerPrims(n, edges, start)
        print(cost)