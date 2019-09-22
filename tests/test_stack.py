import unittest

from hypothesis import given
from hypothesis.strategies import integers, lists

from algorithms.stack import Stack


class TestStack(unittest.TestCase):
    def setUp(self):
        self.stack = Stack()

    def setup_example(self):
        self.stack = Stack()

    def tearDown(self):
        del self.stack

    @given(lists(integers()))
    def test_push_pop_consistency(self, l):
        for element in l:
            self.stack.push(element)

        l2 = []
        while True:
            try:
                element = self.stack.pop()
                l2.append(element)
            except:
                break
        self.assertEqual(l, l2[::-1])

    @given(lists(integers()))
    def test_clear(self, l):
        for element in l:
            self.stack.push(element)

        self.stack.clear()
        self.assertEqual(len(self.stack), 0)
        self.assertTrue(self.stack.isEmpty())

    @given(lists(integers()))
    def test_size(self, l):
        for element in l:
            self.stack.push(element)

        self.assertEqual(len(self.stack), len(l))
        self.assertEqual(len(self.stack), self.stack.size)

    @given(lists(integers()))
    def test_copy(self, l):
        for element in l:
            self.stack.push(element)

        l2 = self.stack.copy()

        for _ in range(len(l)):
            self.assertEqual(l2.pop(), self.stack.pop())

    def test_pop_from_empty_stack(self):
        with self.assertRaises(IndexError):
            self.stack.pop()

    @given(lists(integers()))
    def test_top(self, l):
        for element in l:
            self.stack.push(element)

        if not l:
            with self.assertRaises(KeyError):
                self.stack.top
        else:
            self.assertEqual(l[-1], self.stack.top)


if __name__ == '__main__':
    unittest.main()
