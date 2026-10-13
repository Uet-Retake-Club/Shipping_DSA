class IndexedMinHeap:
    """
    Indexed Min Heap (Priority Queue có chỉ số) phục vụ Eager Prim.
    Cho phép tra cứu vị trí đỉnh và giảm trọng số (decrease_key).
    """

    def __init__(self):
        self.heap = []          # Lưu danh sách: [(weight, node), ...]
        self.pos = {}           # Lưu vị trí hiện tại: {node: index_in_heap}

    def __len__(self):
        return len(self.heap)

    def is_empty(self):
        return len(self.heap) == 0

    def contains(self, node):
        return node in self.pos

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.pos[self.heap[i][1]] = i
        self.pos[self.heap[j][1]] = j

    def _sift_up(self, idx):
        parent = (idx - 1) // 2
        while idx > 0 and self.heap[idx][0] < self.heap[parent][0]:
            self._swap(idx, parent)
            idx = parent
            parent = (idx - 1) // 2

    def _sift_down(self, idx):
        n = len(self.heap)
        while True:
            left = 2 * idx + 1
            right = 2 * idx + 2
            smallest = idx

            if left < n and self.heap[left][0] < self.heap[smallest][0]:
                smallest = left
            if right < n and self.heap[right][0] < self.heap[smallest][0]:
                smallest = right

            if smallest == idx:
                break

            self._swap(idx, smallest)
            idx = smallest

    def insert(self, node, weight):
        """Thêm một đỉnh mới vào Heap kèm trọng số."""
        idx = len(self.heap)
        self.heap.append((weight, node))
        self.pos[node] = idx
        self._sift_up(idx)

    def decrease_key(self, node, new_weight):
        """Cập nhật giảm trọng số của một đỉnh đã tồn tại trong Heap trong O(log V)."""
        idx = self.pos[node]
        if new_weight < self.heap[idx][0]:
            self.heap[idx] = (new_weight, node)
            self._sift_up(idx)

    def pop(self):
        """Lấy đỉnh có trọng số nhỏ nhất ra khỏi Heap."""
        if self.is_empty():
            raise IndexError("pop from an empty heap")

        weight, node = self.heap[0]
        last_item = self.heap.pop()
        del self.pos[node]

        if not self.is_empty():
            self.heap[0] = last_item
            self.pos[last_item[1]] = 0
            self._sift_down(0)

        return node, weight