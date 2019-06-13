class Queue:
    def __init__(self):
        self._q = []

    @property
    def size(self):
        return len(self._q)

    def __len__(self):
        return self.size

    def isEmpty(self):
        return self.size == 0

    @property
    def head(self):
        if self.isEmpty():
            return None
        return self._q[0]

    def enqueue(self, element):
        self._q.append(element)

    def dequeue(self):
        if self.isEmpty():
            return None
        temp = self.head
        self._q = self._q[1:]
        return temp
