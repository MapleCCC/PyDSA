from ..splay_tree_impl import SplayTree
import unittest
import pysnooper
import os


class SplayTreeTest(unittest.TestCase):
    def test_insert(self):
        st = SplayTree()
        st.insert(1, 13)
        # print(st)
        self.assertEqual(st.find(1), 13)

    # @pysnooper.snoop(os.path.join(os.path.dirname(__file__), 'test_deletion.log'))
    def test_deletion(self):
        st = SplayTree()
        st.insert(1, 13)
        st.delete(1)
        self.assertEqual(st.size, 0)

    def test_size(self):
        st = SplayTree()
        self.assertEqual(st.size, 0)
        st.insert(1, 13)
        self.assertEqual(st.size, 1)
        st.insert(2, 13)
        self.assertEqual(st.size, 2)

    def test_find(self):
        st = SplayTree()
        st.insert(1, 13)
        self.assertEqual(st.find(2), None)
        self.assertEqual(st.find(1), 13)
        # self.assertEqual(st.find('a'), None)

    def test_splay(self):
        st = SplayTree()
        st.insert(1, 13)
        self.assertEqual(st.node.key, 1)
        st.insert(2, 14)
        self.assertEqual(st.size, 2)
        self.assertEqual(st.node.key, 2)
        st.insert(5, 13)
        self.assertEqual(st.node.key, 5)

    # @pysnooper.snoop(os.path.join(os.path.dirname(__file__), 'test_cut_by_half.log'))
    def test_cut_by_half(self):
        st = SplayTree()
        st.insert(1, 13)
        st.insert(2, 14)
        st.insert(5, 13)
        st.insert(8, 89)
        # print(st)
        st.cut_by_half()
        # print(st)
        self.assertEqual(st.size, 2)


if __name__ == '__main__':
    unittest.main()
