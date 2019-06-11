from ..bst import BST
import unittest


class TestBinarySearchTree(unittest.TestCase):
    def setUp(self):
        self.bst = BST()

    def tearDown(self):
        del self.bst

    def test_insert(self):
        self.bst.insert(1, 100)
        self.assertEqual(self.bst.find(1), 100)

    def test_delete(self):
        self.bst.insert(1, 100)
        self.bst.delete(1)
        self.assertIsNone(self.bst.find(1))

    def test_trivial_case(self):
        self.bst.insert(6, 100)
        self.bst.insert(7)
        self.bst.insert(4)
        self.bst.insert(1)
        self.bst.insert(5)
        self.bst.insert(3)
        self.bst.delete(1)
        self.assertEqual(self.bst.size, 5)
        self.assertIsNone(self.bst.find(1))

    def test_incomparable_key_type(self):
        self.bst.insert([])
        with self.assertRaises(ValueError):
            self.bst.insert({})
