import unittest

from algorithms.heap import Heap

class TestHeap(unittest.TestCase):
    def setUp(self):
        self.h = Heap()

    def tearDown(self):
        self.h.clear()

    def test_insert(self):
        self.h.insert(1, 100)
        self.h.insert(2, 200)
        self.assertEqual(self.h.size, 2)
        self.assertEqual(self.h.find(1), 100)
        self.assertIsNone(self.h.find(3))

    def test_top(self):
        self.h.insert(2, 200)
        self.h.insert(1, 100)
        self.h.insert(3, 300)
        self.assertEqual(self.h.top, (1, 100))

    def test_delete(self):
        self.h.insert(4, 400)
        self.h.insert(3, 300)
        self.h.insert(1, 100)
        self.h.insert(2, 200)
        self.assertEqual(self.h.delete(1), 100)
        self.assertEqual(self.h.size, 3)
        self.assertIsNone(self.h.delete(5))
        self.assertEqual(self.h.top, (2, 200))
        self.h.delete(2)
        self.assertEqual(self.h.top, (3, 300))
        self.h.delete(3)
        self.assertEqual(self.h.top, (4, 400))
        self.h.delete(4)
        self.assertIsNone(self.h.top)

    def test_priority_order(self):
        self.h = Heap(priority_order="max")
        self.h.insert(4, 400)
        self.h.insert(3, 300)
        self.h.insert(1, 100)
        self.h.insert(2, 200)
        self.assertEqual(self.h.delete(1), 100)
        self.assertEqual(self.h.size, 3)
        self.assertIsNone(self.h.delete(5))
        self.assertEqual(self.h.top, (4, 400))
        self.h.delete(4)
        self.assertEqual(self.h.top, (3, 300))
        self.h.delete(3)
        self.assertEqual(self.h.top, (2, 200))
        self.h.delete(2)
        self.assertIsNone(self.h.top)


if __name__ == "__main__":
    unittest.main()
