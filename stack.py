class Stack:
    def __init__(self):
        self.storage = []

    def push(self, element):
        self.storage.append(element)

    def pop(self):
        if self.isEmpty():
            raise BaseException("Cannot pop an empty stack!")
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
            # return None
            raise BaseException("An empty stack has not top.")
        return self.storage[-1]
