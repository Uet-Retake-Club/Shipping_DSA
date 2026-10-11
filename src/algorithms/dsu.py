"""
Disjoint Set Union (DSU) / Union-Find Data Structure.
Phục vụ các thuật toán Cây khung nhỏ nhất (Kruskal, Boruvka)
với 2 kỹ thuật tối ưu hóa cốt lõi:
1. Path Compression (Nén đường đi)
2. Union by Rank (Hợp nhất theo hạng)
"""

from typing import Any, Dict, Iterable, Optional, Set


class DisjointSetUnion:
    """
    Cấu trúc dữ liệu các tập hợp rời nhau (Disjoint Set Union - DSU).
    Hỗ trợ các phần tử có định danh bất kỳ (string, int,...).
    """

    def __init__(self, elements: Optional[Iterable[Any]] = None) -> None:
        """
        Khởi tạo DSU. Nếu truyền danh sách elements, mỗi phần tử tự tạo 1 tập hợp riêng.
        """
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
        """
        Tìm đại diện (gốc) của tập hợp chứa x.
        Áp dụng tối ưu Path Compression (Nén đường đi): O(alpha(V)).
        """
        if x not in self.parent:
            self.make_set(x)
            return x

        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: Any, y: Any) -> bool:
        """
        Hợp nhất 2 tập hợp chứa x và y.
        Áp dụng tối ưu Union by Rank (Gắn cây thấp vào gốc cây cao hơn).

        Returns:
            True nếu x và y thuộc 2 tập hợp khác nhau và đã được gộp thành công.
            False nếu x và y đã thuộc cùng một tập hợp (tạo chu trình).
        """
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
        """Kiểm tra x và y có cùng thuộc một thành phần liên thông hay không."""
        return self.find(x) == self.find(y)

    @property
    def count(self) -> int:
        """Trả về số lượng tập hợp con rời nhau hiện tại."""
        return self.num_sets

    def get_components(self) -> Dict[Any, Set[Any]]:
        """Trả về từ điển gồm root -> tập hợp các nút thuộc component đó."""
        components: Dict[Any, Set[Any]] = {}
        for elem in self.parent:
            root = self.find(elem)
            if root not in components:
                components[root] = set()
            components[root].add(elem)
        return components
