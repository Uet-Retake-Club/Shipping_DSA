
from __future__ import annotations

from collections.abc import Hashable, Iterable


class DSU:
    """Cấu trúc dữ liệu các tập rời nhau (Union-Find) trên phần tử hashable."""

    def __init__(self, elements: Iterable[Hashable] = ()) -> None:
        """
        Khởi tạo, mỗi phần tử ban đầu nằm trong một tập riêng của chính nó.

        Args:
            elements: Các phần tử ban đầu. Phần tử trùng nhau chỉ được tính
                một lần.
        """
        self._index: dict[Hashable, int] = {}  # phần tử -> chỉ số
        self._items: list[Hashable] = []  # chỉ số -> phần tử
        self._parent: list[int] = []
        self._rank: list[int] = []
        self._count = 0  # số tập rời nhau hiện có
        for element in elements:
            self.add(element)

    def add(self, element: Hashable) -> bool:
        """
        Thêm ``element`` thành một tập mới gồm đúng một phần tử.

        Returns:
            True nếu phần tử mới được thêm, False nếu nó đã tồn tại từ trước
            (khi đó không có gì thay đổi).

        Raises:
            TypeError: nếu ``element`` không hashable.
        """
        if element in self._index:
            return False
        index = len(self._items)
        self._index[element] = index
        self._items.append(element)
        self._parent.append(index)
        self._rank.append(0)
        self._count += 1
        return True

    def _root(self, index: int) -> int:
        """Tìm gốc của ``index`` và nén đường đi (chỉ trên số nguyên)."""
        parent = self._parent

        # Lượt 1: đi lên để tìm gốc.
        root = index
        while parent[root] != root:
            root = parent[root]

        # Lượt 2: nén đường đi, trỏ mọi nút trên đường về thẳng gốc.
        while index != root:
            parent[index], index = root, parent[index]

        return root

    def find(self, element: Hashable) -> Hashable:
        """
        Trả về phần tử đại diện (gốc) của tập chứa ``element``.

        Cài đặt bằng vòng lặp hai lượt (không đệ quy) nên an toàn với cây
        rất sâu, không bao giờ gặp ``RecursionError``.

        Raises:
            KeyError: nếu ``element`` chưa từng được thêm vào DSU.
        """
        return self._items[self._root(self._index[element])]

    def union(self, a: Hashable, b: Hashable) -> bool:
        """
        Hợp nhất hai tập chứa ``a`` và ``b`` (Union by Rank).

        Returns:
            True nếu hai tập khác nhau và đã được hợp nhất.
            False nếu ``a`` và ``b`` vốn đã cùng một tập (khi đó không thay
            đổi gì).
            Với Kruskal, False nghĩa là thêm cạnh ``(a, b)`` sẽ tạo chu trình.

        Raises:
            KeyError: nếu ``a`` hoặc ``b`` chưa được thêm vào DSU
                (khi đó không có tập nào bị hợp nhất).
        """
        root_a = self._root(self._index[a])
        root_b = self._root(self._index[b])
        if root_a == root_b:
            return False

        rank = self._rank
        # Đảm bảo root_a có hạng lớn hơn hoặc bằng; root_b sẽ bị gắn vào.
        if rank[root_a] < rank[root_b]:
            root_a, root_b = root_b, root_a

        self._parent[root_b] = root_a
        if rank[root_a] == rank[root_b]:
            # Hai cây cao bằng nhau: cây mới cao hơn đúng một bậc.
            rank[root_a] += 1

        self._count -= 1
        return True

    def connected(self, a: Hashable, b: Hashable) -> bool:
        """Kiểm tra ``a`` và ``b`` có cùng một tập hay không."""
        return self._root(self._index[a]) == self._root(self._index[b])

    @property
    def count(self) -> int:
        """Số tập rời nhau hiện có (với đồ thị: số thành phần liên thông)."""
        return self._count

    def components(self) -> list[list[Hashable]]:
        """
        Trả về danh sách các tập, mỗi tập là danh sách các phần tử của nó.

        Thứ tự có tính xác định: các phần tử giữ thứ tự được thêm vào, và các
        tập xếp theo phần tử xuất hiện sớm nhất của mỗi tập.
        """
        groups: dict[int, list[Hashable]] = {}
        for index, item in enumerate(self._items):
            groups.setdefault(self._root(index), []).append(item)
        return list(groups.values())

    def __len__(self) -> int:
        """Tổng số phần tử (không phải số tập)."""
        return len(self._items)

    def __contains__(self, element: Hashable) -> bool:
        return element in self._index

    def __repr__(self) -> str:
        return f"DSU(elements={len(self)}, sets={self._count})"