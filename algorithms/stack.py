class Stack:
    def __init__(self):
        self._storage = []

    __slots__ = ['_storage']

    def clear(self):
        self._storage.clear()

    def copy(self):
        new = Stack()
        new._storage = self._storage.copy()
        return new

    def push(self, element):
        self._storage.append(element)

    def pop(self):
        try:
            return self._storage.pop()
        except IndexError:
            raise IndexError("pop from empty stack")

    @property
    def size(self):
        return len(self._storage)

    def __len__(self):
        return self.size

    def isEmpty(self):
        return self.size == 0

    @property
    def top(self):
        try:
            return self._storage[-1]
        except IndexError:
            raise KeyError("Empty stack has no top")

    def __str__(self):
        if self.isEmpty():
            return "Empty stack"
        if self.size == 1:
            return "Stack(top={})".format(self.top)
        if self.size == 2:
            return "Stack(top={}, bottom={})".format(self.top, self._storage[0])

        other = ",".join(map(str, self._storage[1:-1][::-1]))
        return "Stack(top={}, {}, bottom={})".format(self.top, other, self._storage[0])

    def __repr__(self):
        return str(self)


if __name__ == '__main__':
    a = Stack()
    a.push(1)
    a.push(2)
    a.push(3)
    print(a)
