import unittest

from algorithms.tree.bst import BST


class TestBinarySearchTree(unittest.TestCase):
    def setUp(self):
        self.bst = BST()

    def tearDown(self):
        del self.bst

    def _construct_trivial_case(self):
        self.bst.insert(6)
        self.bst.insert(9)
        self.bst.insert(4)
        self.bst.insert(1)
        self.bst.insert(5)
        self.bst.insert(3)
        self.bst.insert(7)
        self.bst.insert(8)
        self.bst.insert(2)

    def test_insert(self):
        self.bst.insert(1)
        self.assertTrue(self.bst.search(1))
        self.assertEqual(len(self.bst), 1)
        self.bst.insert(1)
        self.assertEqual(len(self.bst), 1)

    def test_remove(self):
        self.bst.insert(1)
        self.assertTrue(self.bst.search(1))
        self.bst.remove(1)
        self.assertFalse(self.bst.search(1))

    def test_trivial_case(self):
        self._construct_trivial_case()
        self.bst.remove(4)
        self.assertEqual(self.bst.size, 8)
        self.assertFalse(self.bst.search(4))

    def test_incomparable_key_type(self):
        self.bst.insert([])
        with self.assertRaises(ValueError):
            self.bst.insert({})

    def test_copy(self):
        self._construct_trivial_case()
        new = self.bst.copy()
        self.assertFalse(new is self.bst)
        self.assertEqual(list(new.traverse("in_order")),
                         [1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.assertEqual(list(new.traverse("pre_order")),
                         [6, 4, 1, 3, 2, 5, 9, 7, 8])

    def test_in_order_traversal(self):
        self._test_traverse("in_order", [1, 2, 3, 4, 5, 6, 7, 8, 9])

    def test_out_order_traversal(self):
        self._test_traverse("out_order", [9, 8, 7, 6, 5, 4, 3, 2, 1])

    def test_pre_order_traversal(self):
        self._test_traverse("pre_order", [6, 4, 1, 3, 2, 5, 9, 7, 8])

    def test_post_order_traversal(self):
        self._test_traverse("post_order", [2, 3, 1, 5, 4, 8, 7, 9, 6])

    def test_breadth_first_order_traversal(self):
        self._test_traverse("breadth_first_order", [
                            6, 4, 9, 1, 5, 7, 3, 8, 2])

    def _test_traverse(self, order, supposed_result):
        self._construct_trivial_case()
        result = list(self.bst.traverse(order))
        self.assertEqual(result, supposed_result)

    def test_height(self):
        self.assertEqual(self.bst.height, 0)
        self._construct_trivial_case()
        self.assertEqual(self.bst.height, 5)
        # Should not test height after any deletion operation.
        # Unlike insertion operation, which lead to deterministic tree layout.
        # deletion operation have non-unique implementation approach (up to concrete implementation algorithm) that could lead to different tree layout afterwards.

    def test_iterator_type(self):
        self._construct_trivial_case()
        result = list(iter(self.bst))
        self.assertEqual(result, [i+1 for i in range(9)])


if __name__ == "__main__":
    unittest.main()
