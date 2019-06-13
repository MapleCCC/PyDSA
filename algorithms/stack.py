class Stack:
    def __init__(self):
        self.storage = []

    def push(self, element):
        self.storage.append(element)

    def pop(self):
        if self.isEmpty():
            return None
        temp = self.top
        self.storage = self.storage[:-1]
        return temp

    @property
    def size(self):
        return len(self.storage)

    def isEmpty(self):
        return self.size == 0

    @property
    def top(self):
        if self.isEmpty():
            return None
        return self.storage[-1]
