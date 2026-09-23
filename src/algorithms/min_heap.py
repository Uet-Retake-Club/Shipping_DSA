"""
Custom Binary Min-Heap / Priority Queue.
Implemented from scratch without using Python's built-in `heapq` module,
conforming to Data Structures & Algorithms (DSA) course standards.
Time Complexity:
- push: O(log N)
- pop: O(log N)
- peek: O(1)
- is_empty: O(1)
"""

from typing import Any, Generic, List, Optional, TypeVar

T = TypeVar("T")


class MinHeap(Generic[T]):
    """
    Array-based binary min-heap where parent <= children.
    For element at index i (0-based):
    - Parent: (i - 1) // 2
    - Left Child: 2 * i + 1
    - Right Child: 2 * i + 2
    """

    def __init__(self):
        self._heap: List[T] = []

    def __len__(self) -> int:
        return len(self._heap)

    def is_empty(self) -> bool:
        return len(self._heap) == 0

    def peek(self) -> T:
        """Returns the minimum element without removing it. Raises IndexError if empty."""
        if self.is_empty():
            raise IndexError("peek from empty heap")
        return self._heap[0]

    def push(self, item: T) -> None:
        """Adds a new item to the heap and restores heap invariant via sift_up."""
        self._heap.append(item)
        self._sift_up(len(self._heap) - 1)

    def pop(self) -> T:
        """Removes and returns the minimum element; restores invariant via sift_down."""
        if self.is_empty():
            raise IndexError("pop from empty heap")

        # Swap root with last element
        min_item = self._heap[0]
        last_item = self._heap.pop()

        if not self.is_empty():
            self._heap[0] = last_item
            self._sift_down(0)

        return min_item

    def _sift_up(self, idx: int) -> None:
        """Bubbles the item at `idx` upward until parent <= item."""
        curr = idx
        while curr > 0:
            parent = (curr - 1) // 2
            if self._heap[curr] < self._heap[parent]:
                self._heap[curr], self._heap[parent] = self._heap[parent], self._heap[curr]
                curr = parent
            else:
                break

    def _sift_down(self, idx: int) -> None:
        """Sinks the item at `idx` downward until item <= both children."""
        curr = idx
        n = len(self._heap)
        while True:
            left = 2 * curr + 1
            right = 2 * curr + 2
            smallest = curr

            if left < n and self._heap[left] < self._heap[smallest]:
                smallest = left
            if right < n and self._heap[right] < self._heap[smallest]:
                smallest = right

            if smallest != curr:
                self._heap[curr], self._heap[smallest] = self._heap[smallest], self._heap[curr]
                curr = smallest
            else:
                break

    def clear(self) -> None:
        self._heap.clear()
