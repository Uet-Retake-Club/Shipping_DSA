"""
Disjoint Set Union (DSU) / Union-Find Data Structure.
Implemented from scratch for Kruskal's algorithm without external libraries.
Optimizations:
1. Path Compression (in find)
2. Union by Rank (in union)
Amortized time complexity per operation: O(alpha(V)), where alpha is the Inverse Ackermann function.
"""

from typing import Dict, Generic, Iterable, List, Optional, Set, TypeVar

T = TypeVar("T")


class DisjointSetUnion(Generic[T]):
    """
    Disjoint Set Union (DSU) supporting generic elements (strings, ints, etc.).
    """

    def __init__(self, elements: Optional[Iterable[T]] = None):
        self.parent: Dict[T, T] = {}
        self.rank: Dict[T, int] = {}
        self.size: Dict[T, int] = {}
        self._num_sets: int = 0

        if elements is not None:
            for el in elements:
                self.make_set(el)

    def make_set(self, element: T) -> None:
        """Initializes a new set containing only the given element."""
        if element not in self.parent:
            self.parent[element] = element
            self.rank[element] = 0
            self.size[element] = 1
            self._num_sets += 1

    def find(self, element: T) -> T:
        """
        Finds the representative root of the set containing `element`.
        Uses Path Compression to flatten the tree during traversal.
        """
        if element not in self.parent:
            self.make_set(element)
            return element

        # Path Compression: recursively set parent of every visited node directly to the root
        if self.parent[element] != element:
            self.parent[element] = self.find(self.parent[element])
        return self.parent[element]

    def union(self, a: T, b: T) -> bool:
        """
        Merges the sets containing elements `a` and `b`.
        Uses Union by Rank to attach the shallower tree under the root of the deeper tree.
        Returns:
            True if `a` and `b` were in different sets and have been merged.
            False if `a` and `b` were already in the same set (i.e. adding an edge would form a cycle).
        """
        root_a = self.find(a)
        root_b = self.find(b)

        if root_a == root_b:
            return False  # Already in the same set; cycle detected!

        # Union by Rank: attach smaller rank tree to larger rank tree
        if self.rank[root_a] < self.rank[root_b]:
            self.parent[root_a] = root_b
            self.size[root_b] += self.size[root_a]
        elif self.rank[root_a] > self.rank[root_b]:
            self.parent[root_b] = root_a
            self.size[root_a] += self.size[root_b]
        else:
            self.parent[root_b] = root_a
            self.rank[root_a] += 1
            self.size[root_a] += self.size[root_b]

        self._num_sets -= 1
        return True

    def connected(self, a: T, b: T) -> bool:
        """Checks whether two elements belong to the same component."""
        return self.find(a) == self.find(b)

    @property
    def num_sets(self) -> int:
        """Returns the current number of disjoint components."""
        return self._num_sets

    def get_components(self) -> Dict[T, List[T]]:
        """Returns a mapping from root representative to list of members in each set."""
        components: Dict[T, List[T]] = {}
        for element in list(self.parent.keys()):
            root = self.find(element)
            components.setdefault(root, []).append(element)
        return components

    def __len__(self) -> int:
        return len(self.parent)
