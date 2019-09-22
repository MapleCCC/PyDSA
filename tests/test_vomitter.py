import unittest

from hypothesis import given
from hypothesis.strategies import integers, lists

from algorithms.vomitter import Vomitter


class VomitterTestCase(unittest.TestCase):
    def setUp(self):
        self.vomitter = Vomitter()

    def setup_example(self):
        self.vomitter = Vomitter()

    def tearDown(self):
        del self.vomitter

    @given(integers())
    def test_add(self, i):
        self.vomitter.add(i)
        self.assertEqual(self.vomitter.emit(), i)

    @given(lists(integers()))
    def test_emit(self, l):
        for element in l:
            self.vomitter.add(element)

        if not l:
            with self.assertRaises(IndexError):
                self.vomitter.emit()
        else:
            self.assertIn(self.vomitter.emit(), l)
