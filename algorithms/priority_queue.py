"""
PriorityQueue

Complexity
----------
| Operation | Complexity |
--------------------------
| enqueue | O(logN) |
| dequeue | O(logN) |
| head | O(1) |
"""

from .heap import Heap


class PriorityQueue(Heap):
    def enqueue(self, key, value=None):
        self.insert(key, value)

    def dequeue(self):
        key, value = self.top
        self.delete(key)
        return key, value

    def head(self):
        return self.top
