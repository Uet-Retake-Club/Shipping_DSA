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


class TestIndexedMinHeap(unittest.TestCase):
    def setUp(self):
        from src.algorithms.indexed_min_heap import IndexedMinHeap
        self.ipq = IndexedMinHeap()

    def test_insert_and_pop(self):
        self.ipq.insert("NodeA", 10.0)
        self.ipq.insert("NodeB", 4.0)
        self.ipq.insert("NodeC", 7.0)

        self.assertEqual(len(self.ipq), 3)
        self.assertTrue(self.ipq.contains("NodeB"))

        node, weight = self.ipq.pop()
        self.assertEqual(node, "NodeB")
        self.assertEqual(weight, 4.0)

    def test_decrease_key(self):
        self.ipq.insert("H1", 20)
        self.ipq.insert("H2", 15)
        self.ipq.insert("H3", 25)

        # Giảm trọng số của H3 từ 25 xuống 5 -> H3 phải vươn lên thành nhỏ nhất
        self.ipq.decrease_key("H3", 5)

        top_node, top_weight = self.ipq.pop()
        self.assertEqual(top_node, "H3")
        self.assertEqual(top_weight, 5)


if __name__ == '__main__':
    unittest.main()

