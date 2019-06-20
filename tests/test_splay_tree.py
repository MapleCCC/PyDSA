from algorithms.tree.splay_tree import TopDownSplayTree, BottomUpSplayTree
import unittest


class TestSplayTree(unittest.TestCase):
    def setUp(self):
        self.st = BottomUpSplayTree()

    def tearDown(self):
        del self.st

    def test_insert(self):
        self.st.insert(1)
        # print(self.st)
        self.assertTrue(self.st.find(1))

    def test_deletion(self):
        self.st.insert(1)
        self.st.delete(1)
        self.assertEqual(self.st.size, 0)

    def test_size(self):
        self.assertEqual(self.st.size, 0)
        self.st.insert(1)
        self.assertEqual(self.st.size, 1)
        self.st.insert(2)
        self.assertEqual(self.st.size, 2)

    def test_find(self):
        self.st.insert(1)
        self.assertFalse(self.st.find(2))
        self.assertTrue(self.st.find(1))
        # self.assertEqual(self.st.find('a'), None)

    def test_splay(self):
        self.st.insert(1)
        self.assertEqual(self.st.root.value, 1)
        self.st.insert(2)
        self.assertEqual(self.st.size, 2)
        self.assertEqual(self.st.root.value, 2)
        self.st.insert(5)
        self.assertEqual(self.st.root.value, 5)

    # def test_cut_by_half(self):
    #     self.st.insert(1, 13)
    #     self.st.insert(2, 14)
    #     self.st.insert(5, 13)
    #     self.st.insert(8, 89)
    #     # print(self.st)
    #     self.st.cut_by_half()
    #     # print(self.st)
    #     self.assertEqual(self.st.size, 2)


class TestBottomUpSplayTree(TestSplayTree):
    def setUp(self):
        self.st = BottomUpSplayTree()


@unittest.skip("Not implemented")
class TestTopDownSplayTree(TestSplayTree):
    def setUp(self):
        self.st = TopDownSplayTree()


if __name__ == '__main__':
    unittest.main()
