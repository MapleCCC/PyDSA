class Queue:
    def __init__(self):
        self.storage = []

    @property
    def size(self):
        return len(self.storage)

    def isEmpty(self):
        return self.size == 0

    @property
    def head(self):
        if self.isEmpty():
            return None
        return self.storage[0]

    def enqueue(self, element):
        self.storage.append(element)

    def dequeue(self):
        if self.isEmpty():
            raise BaseException("Cannot dequeue an empty queue.")
        temp = self.head
        self.storage = self.storage[1:]
        return temp