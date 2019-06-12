"""
Heap

Complexity:
| Operation | Complexity |
__________________________
| insert | O(N) |
| delete | O(N) |
| find | O(N) |
| clear | O(1) |
| get top | O(1) |
| get size | O(1) |
"""

__all__ = ['Heap']

from math import floor


class Node:
    def __init__(self, key, value=None):
        self.key = key
        self.value = value

    def __lt__(self, node):
        return self.key < node.key

    def __gt__(self, node):
        return self.key > node.key


class RevNode(Node):
    def __lt__(self, node):
        return self.key > node.key

    def __gt__(self, node):
        return self.key < node.key


class Heap:
    def __init__(self, priority_order="min"):
        self._heap = []
        if priority_order not in {"min", "max"}:
            raise ValueError("Invalid priority_order option.")
        self.priority_order = priority_order

    def insert(self, key, value=None):
        index = self._find(key)
        if index is None:
            if self.priority_order == "min":
                node = Node(key, value)
            elif self.priority_order == "max":
                node = RevNode(key, value)
            self._heap.append(node)
            new_node_index = self.size - 1
            self._try_move_up(new_node_index)
        else:
            self[index].value = value

    def delete(self, key):
        index = self._find(key)
        if index is None:
            return None

        node = self[index]
        value = node.value
        if self.size == 1:
            self._heap = self[:-1]
            return value
        else:
            tail = self[-1]
            self._swap(node, tail)
            self._heap = self[:-1]

            self._try_move_up(index)
            self._try_move_down(index)
            return value

    def find(self, key):
        index = self._find(key)
        if index is None:
            return None
        return self[index].value

    # TODO: use more clever algorithm to improve performance
    # When heap used as priority_queue, _find() degrade to top()
    def _find(self, key):
        for index, node in enumerate(self._heap):
            if node.key == key:
                return index
        return None

    def _try_move_up(self, index):
        if index == 0:
            return
        node = self[index]
        parent_index = floor((index - 1) / 2)
        parent = self[parent_index]
        if node < parent:
            self._swap(node, parent)
            self._try_move_up(parent_index)

    def _try_move_down(self, index):
        node = self[index]

        left_child_index = 2 * index + 1
        right_child_index = 2 * index + 2

        sentinel = self.size - 1

        if left_child_index > sentinel:
            return
        elif node > self[left_child_index]:
            self._swap(node, self[left_child_index])
            self._try_move_down(left_child_index)
        elif right_child_index > sentinel:
            return
        elif node > self[right_child_index]:
            self._swap(node, self[right_child_index])
            self._try_move_down(right_child_index)
        else:
            return

    def _swap(self, node1, node2):
        node1.key, node2.key = node2.key, node1.key
        node1.value, node2.value = node2.value, node1.value

    def clear(self):
        self._heap.clear()

    @property
    def top(self):
        if self.isEmpty():
            return None
        node = self[0]
        return node.key, node.value

    @property
    def size(self):
        return len(self._heap)

    def __len__(self):
        return self.size

    def isEmpty(self):
        return self.size == 0

    def __iter__(self):
        return iter(self._heap)

    def __str__(self):
        pass

    # TODO: Customize __getitem__ to cover more cases.
    def __getitem__(self, n):
        if isinstance(n, int):
            return self._heap[n]
        elif isinstance(n, slice):
            return self._heap[n]
        else:
            raise IndexError("Invalid index.")
