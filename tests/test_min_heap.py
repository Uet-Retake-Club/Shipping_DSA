import unittest
from src.algorithms.min_heap import MinHeap


class TestMinHeap(unittest.TestCase):
    def setUp(self):
        self.heap = MinHeap()

    def test_empty_heap(self):
        self.assertTrue(self.heap.is_empty())
        self.assertEqual(len(self.heap), 0)
        with self.assertRaises(IndexError):
            self.heap.pop()
        with self.assertRaises(IndexError):
            self.heap.peek()

    def test_push_and_pop_integers(self):
        elements = [10, 4, 15, 20, 1, 8, 3]
        for x in elements:
            self.heap.push(x)

        self.assertFalse(self.heap.is_empty())
        self.assertEqual(len(self.heap), len(elements))

        # Kiểm tra thứ tự lấy ra phải tăng dần
        extracted = []
        while not self.heap.is_empty():
            extracted.append(self.heap.pop())

        self.assertEqual(extracted, sorted(elements))

    def test_peek(self):
        self.heap.push(5)
        self.heap.push(2)
        self.heap.push(8)
        self.assertEqual(self.heap.peek(), 2)
        self.assertEqual(len(self.heap), 3)  # peek không làm giảm số phần tử

    def test_tuples_for_prim_edges(self):
        # Tuple định dạng: (weight, to_node, from_node)
        edges = [
            (10.5, "B", "A"),
            (3.2, "C", "A"),
            (7.8, "D", "B"),
            (1.0, "E", "C")
        ]
        for edge in edges:
            self.heap.push(edge)

        # Lấy cạnh rẻ nhất đầu tiên
        best_edge = self.heap.pop()
        self.assertEqual(best_edge, (1.0, "E", "C"))

        next_best = self.heap.pop()
        self.assertEqual(next_best, (3.2, "C", "A"))

    def test_duplicates(self):
        values = [5, 2, 5, 1, 2]
        for val in values:
            self.heap.push(val)

        res = [self.heap.pop() for _ in range(len(values))]
        self.assertEqual(res, [1, 2, 2, 5, 5])


if __name__ == '__main__':
    unittest.main()

