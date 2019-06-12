from algorithms.tree.bst import BST, LazyBinarySearchTree
import unittest


class TestBinarySearchTree(unittest.TestCase):
    def setUp(self):
        self.bst = BST()

    def tearDown(self):
        del self.bst

    def _construct_trivial_case(self):
        self.bst.insert(6, 100)
        self.bst.insert(7)
        self.bst.insert(4)
        self.bst.insert(1)
        self.bst.insert(5)
        self.bst.insert(3)

    def test_insert(self):
        self.bst.insert(1, 100)
        self.assertEqual(self.bst.find(1), 100)

    def test_delete(self):
        self.bst.insert(1, 100)
        self.bst.delete(1)
        self.assertIsNone(self.bst.find(1))

    def test_trivial_case(self):
        self._construct_trivial_case()
        self.bst.delete(1)
        self.assertEqual(self.bst.size, 5)
        self.assertIsNone(self.bst.find(1))

    def test_incomparable_key_type(self):
        self.bst.insert([])
        with self.assertRaises(ValueError):
            self.bst.insert({})

    def test_in_order_traversal(self):
        self._construct_trivial_case()
        result = []

        def log(node):
            result.append(node.key)
        self.bst.traverse(log, "in_order")
        self.assertEqual(result, [1, 3, 4, 5, 6, 7])

    def test_pre_order_traversal(self):
        self._construct_trivial_case()
        result = []

        def log(node):
            result.append(node.key)
        self.bst.traverse(log, "pre_order")
        self.assertEqual(result, [6, 4, 7, 1, 5, 3])

    def test_post_order_traversal(self):
        self._construct_trivial_case()
        result = []

        def log(node):
            result.append(node.key)
        self.bst.traverse(log, "post_order")
        self.assertEqual(result, [3, 1, 5, 4, 7, 6])

    def test_height(self):
        self._construct_trivial_case()
        self.bst.delete(1)
        self.assertEqual(self.bst.height, 3)

    def test_iterator_type(self):
        self._construct_trivial_case()
        result = []
        for k, v in self.bst:
            result.append((k, v))
        self.assertEqual(
            result, [(1, None), (3, None), (4, None), (5, None), (6, 100), (7, None)])


class TestLazyBinarySearchTree(TestBinarySearchTree):
    def setUp(self):
        self.bst = LazyBinarySearchTree()


if __name__ == "__main__":
    unittest.main()
