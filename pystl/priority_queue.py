class PriorityQueue:
    def __init__(self, min=True):
        self.storage = []

    @property
    def size(self):
        return len(self.storage)

    def isEmpty(self):
        return self.size == 0

    @property
    def top(self):
        if self.isEmpty():
            return None
        return self.storage[0]

    def enqueue(self, element):
        self.storage.append(element)
        self.push_up(len(self.storage)-1)

    def parent(self, index):
        return (index - 1) // 2

    def push_up(self, index):
        pass