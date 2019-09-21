import unittest

from algorithms.tree.splay_tree import SplayTree


class TestSplayTree(unittest.TestCase):
    def setUp(self):
        self.st = SplayTree()

    def tearDown(self):
        del self.st

    def test_insert(self):
        self.st.insert(1)
        # print(self.st)
        self.assertTrue(self.st.search(1))

    def test_deletion(self):
        self.st.insert(1)
        self.st.remove(1)
        self.assertEqual(self.st.size, 0)

    def test_size(self):
        self.assertEqual(self.st.size, 0)
        self.st.insert(1)
        self.assertEqual(self.st.size, 1)
        self.st.insert(2)
        self.assertEqual(self.st.size, 2)

    def test_search(self):
        self.st.insert(1)
        self.assertFalse(self.st.search(2))
        self.assertTrue(self.st.search(1))
        # self.assertEqual(self.st.search('a'), None)

    def test_splay(self):
        self.st.insert(1)
        self.assertEqual(self.st.root, 1)
        self.st.insert(2)
        self.assertEqual(self.st.size, 2)
        self.assertEqual(self.st.root, 2)
        self.st.insert(5)
        self.assertEqual(self.st.root, 5)

    # def test_cut_by_half(self):
    #     self.st.insert(1, 13)
    #     self.st.insert(2, 14)
    #     self.st.insert(5, 13)
    #     self.st.insert(8, 89)
    #     # print(self.st)
    #     self.st.cut_by_half()
    #     # print(self.st)
    #     self.assertEqual(self.st.size, 2)


if __name__ == '__main__':
    unittest.main()
