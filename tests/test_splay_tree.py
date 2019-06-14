from algorithms.tree.splay_tree import TopDownSplayTree, ButtomUpSplayTree
import unittest


class TestTopDownSplayTree(unittest.TestCase):
    def setUp(self):
        self.st = TopDownSplayTree()

    def tearDown(self):
        del self.st

    def test_insert(self):
        self.st.insert(1, 13)
        # print(self.st)
        self.assertEqual(self.st.find(1), 13)

    def test_deletion(self):
        self.st.insert(1, 13)
        self.st.delete(1)
        self.assertEqual(self.st.size, 0)

    def test_size(self):
        self.assertEqual(self.st.size, 0)
        self.st.insert(1, 13)
        self.assertEqual(self.st.size, 1)
        self.st.insert(2, 13)
        self.assertEqual(self.st.size, 2)

    def test_find(self):
        self.st.insert(1, 13)
        self.assertEqual(self.st.find(2), None)
        self.assertEqual(self.st.find(1), 13)
        # self.assertEqual(self.st.find('a'), None)

    def test_splay(self):
        self.st.insert(1, 13)
        self.assertEqual(self.st.root.key, 1)
        self.st.insert(2, 14)
        self.assertEqual(self.st.size, 2)
        self.assertEqual(self.st.root.key, 2)
        self.st.insert(5, 13)
        self.assertEqual(self.st.root.key, 5)

    # def test_cut_by_half(self):
    #     self.st.insert(1, 13)
    #     self.st.insert(2, 14)
    #     self.st.insert(5, 13)
    #     self.st.insert(8, 89)
    #     # print(self.st)
    #     self.st.cut_by_half()
    #     # print(self.st)
    #     self.assertEqual(self.st.size, 2)


class TestButtomUpSplayTree(TestTopDownSplayTree):
    def setUp(self):
        self.st = ButtomUpSplayTree()


if __name__ == '__main__':
    unittest.main()
