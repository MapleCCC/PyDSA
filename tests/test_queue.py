import unittest

from hypothesis import given
from hypothesis.strategies import integers, lists

from algorithms.queue import Queue


class TestQueue(unittest.TestCase):
    def setUp(self):
        self.queue = Queue()

    def setup_example(self):
        self.queue = Queue()

    def tearDown(self):
        del self.queue

    @given(lists(integers()))
    def test_enqueue_dequeue_consistency(self, l):
        for element in l:
            self.queue.enqueue(element)

        l2 = []
        while True:
            try:
                element = self.queue.dequeue()
                l2.append(element)
            except:
                break
        self.assertEqual(l, l2)

    @given(lists(integers()))
    def test_clear(self, l):
        for element in l:
            self.queue.enqueue(element)

        self.queue.clear()
        self.assertEqual(len(self.queue), 0)
        self.assertTrue(self.queue.isEmpty())

    @given(lists(integers()))
    def test_size(self, l):
        for element in l:
            self.queue.enqueue(element)

        self.assertEqual(len(self.queue), len(l))
        self.assertEqual(len(self.queue), self.queue.size)

    @given(lists(integers()))
    def test_copy(self, l):
        for element in l:
            self.queue.enqueue(element)

        l2 = self.queue.copy()

        for _ in range(len(l)):
            self.assertEqual(l2.dequeue(), self.queue.dequeue())

    def test_dequeue_from_empty_queue(self):
        with self.assertRaises(IndexError):
            self.queue.dequeue()

    @given(lists(integers()))
    def test_top(self, l):
        for element in l:
            self.queue.enqueue(element)

        if not l:
            with self.assertRaises(KeyError):
                self.queue.head
        else:
            self.assertEqual(l[0], self.queue.head)


if __name__ == '__main__':
    unittest.main()
