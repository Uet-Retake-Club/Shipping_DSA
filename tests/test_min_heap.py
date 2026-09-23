"""
Unit tests for MinHeap data structure.
Compatible with standard library unittest and pytest.
"""

import unittest
from src.algorithms.min_heap import MinHeap


class TestMinHeap(unittest.TestCase):
    def test_empty_heap(self):
        heap: MinHeap[int] = MinHeap()
        self.assertTrue(heap.is_empty())
        self.assertEqual(len(heap), 0)

        with self.assertRaises(IndexError):
            heap.pop()

        with self.assertRaises(IndexError):
            heap.peek()

    def test_min_heap_ordering(self):
        heap: MinHeap[int] = MinHeap()
        numbers = [15, 3, 2, 8, 1, 9, 10, 5]
        for n in numbers:
            heap.push(n)

        self.assertEqual(len(heap), len(numbers))
        self.assertFalse(heap.is_empty())
        self.assertEqual(heap.peek(), 1)

        extracted = []
        while not heap.is_empty():
            extracted.append(heap.pop())

        self.assertEqual(extracted, sorted(numbers))

    def test_min_heap_tuple_elements(self):
        heap: MinHeap[tuple] = MinHeap()
        heap.push((3.5, "edge_3"))
        heap.push((1.2, "edge_1"))
        heap.push((2.8, "edge_2"))

        self.assertEqual(heap.pop(), (1.2, "edge_1"))
        self.assertEqual(heap.pop(), (2.8, "edge_2"))
        self.assertEqual(heap.pop(), (3.5, "edge_3"))


if __name__ == "__main__":
    unittest.main()
