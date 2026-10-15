from __future__ import annotations

from collections.abc import Hashable, Iterable
from typing import Any, Dict, Optional, Set


class DSU:
    """Cấu trúc dữ liệu các tập rời nhau (Union-Find) trên phần tử hashable."""

    def __init__(self, elements: Iterable[Hashable] = ()) -> None:
        """
        Khởi tạo, mỗi phần tử ban đầu nằm trong một tập riêng của chính nó.

        Args:
            elements: Các phần tử ban đầu. Phần tử trùng nhau chỉ được tính
                một lần.
        """
        self._index: dict[Hashable, int] = {}
        self._items: list[Hashable] = []
        self._parent: list[int] = []
        self._rank: list[int] = []
        self._count = 0
        for element in elements:
            self.add(element)

    def add(self, element: Hashable) -> bool:
        """Thêm element thành một tập mới; trả về False nếu đã tồn tại."""
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
        """Tìm gốc và nén đường đi bằng vòng lặp."""
        parent = self._parent
        root = index
        while parent[root] != root:
            root = parent[root]
        while index != root:
            parent[index], index = root, parent[index]
        return root

    def find(self, element: Hashable) -> Hashable:
        """Trả về phần tử đại diện; raises KeyError nếu chưa được thêm."""
        return self._items[self._root(self._index[element])]

    def union(self, a: Hashable, b: Hashable) -> bool:
        """Hợp nhất hai tập; trả về False nếu chúng đã cùng một tập."""
        root_a = self._root(self._index[a])
        root_b = self._root(self._index[b])
        if root_a == root_b:
            return False
        rank = self._rank
        if rank[root_a] < rank[root_b]:
            root_a, root_b = root_b, root_a
        self._parent[root_b] = root_a
        if rank[root_a] == rank[root_b]:
            rank[root_a] += 1
        self._count -= 1
        return True

    def connected(self, a: Hashable, b: Hashable) -> bool:
        """Kiểm tra hai phần tử có cùng một tập hay không."""
        return self._root(self._index[a]) == self._root(self._index[b])

    @property
    def count(self) -> int:
        """Số tập rời nhau hiện có."""
        return self._count

    def components(self) -> list[list[Hashable]]:
        """Trả về các tập theo thứ tự phần tử được thêm vào."""
        groups: dict[int, list[Hashable]] = {}
        for index, item in enumerate(self._items):
            groups.setdefault(self._root(index), []).append(item)
        return list(groups.values())

    def __len__(self) -> int:
        """Tổng số phần tử."""
        return len(self._items)

    def __contains__(self, element: Hashable) -> bool:
        return element in self._index

    def __repr__(self) -> str:
        return f"DSU(elements={len(self)}, sets={self._count})"


class DisjointSetUnion:
    """DSU tương thích với API được Boruvka sử dụng."""

    def __init__(self, elements: Optional[Iterable[Any]] = None) -> None:
        self.parent: Dict[Any, Any] = {}
        self.rank: Dict[Any, int] = {}
        self.num_sets: int = 0
        if elements is not None:
            for elem in elements:
                self.make_set(elem)

    def make_set(self, x: Any) -> None:
        """Thêm phần tử x vào tập hợp mới nếu chưa tồn tại."""
        if x not in self.parent:
            self.parent[x] = x
            self.rank[x] = 0
            self.num_sets += 1

    def find(self, x: Any) -> Any:
        """Tìm gốc và nén đường đi; tự thêm phần tử chưa tồn tại."""
        if x not in self.parent:
            self.make_set(x)
            return x
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: Any, y: Any) -> bool:
        """Hợp nhất hai tập; trả về False nếu chúng đã cùng một tập."""
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return False
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
        self.num_sets -= 1
        return True

    def is_connected(self, x: Any, y: Any) -> bool:
        """Kiểm tra hai phần tử có cùng thành phần liên thông hay không."""
        return self.find(x) == self.find(y)

    @property
    def count(self) -> int:
        """Số tập rời nhau hiện có."""
        return self.num_sets

    def get_components(self) -> Dict[Any, Set[Any]]:
        """Trả về ánh xạ từ gốc tới các phần tử trong thành phần."""
        components: Dict[Any, Set[Any]] = {}
        for elem in self.parent:
            root = self.find(elem)
            components.setdefault(root, set()).add(elem)
        return components

