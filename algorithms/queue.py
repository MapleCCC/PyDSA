class Queue:
    def __init__(self):
        self._storage = []

    __slots__ = ["_storage"]

    def clear(self):
        self._storage.clear()

    def copy(self):
        new = Queue()
        new._storage = self._storage.copy()
        return new

    @property
    def size(self):
        return len(self._storage)

    def __len__(self):
        return self.size

    def isEmpty(self):
        return self.size == 0

    def __str__(self):
        if self.isEmpty():
            return "Empty queue"
        return "Queue({})".format(','.join(map(str, self._storage)))

    def __repr__(self):
        return str(self)

    @property
    def head(self):
        try:
            return self._storage[0]
        except IndexError:
            raise KeyError("empty queue has no head")

    def enqueue(self, element):
        self._storage.append(element)

    # Should we use deque data structure as underlying storage,
    # to decrease *dequeue* method's complexity from linear to constant?
    def dequeue(self):
        try:
            return self._storage.pop(0)
        except IndexError:
            raise IndexError("dequeue from empty queue")


if __name__ == '__main__':
    q = Queue()
    q.enqueue(1)
    q.enqueue(2)
    print(q)
