__all__ = ["SplayTree"]

from .bst import BinarySearchTree


LEFT = 1
RIGHT = 0


class SplayTreeImpl1(BinarySearchTree):
    def insert(self, key, value=None):
        super().insert(key, value)
        self.splay(key)

    def find(self, key):
        result = super().find(key)
        if result is not None:
            self.splay(key)
        return result

    def splay(self, key):
        bookkeep = self.track(key)
        if len(bookkeep) == 1:
            return
        if bookkeep[-1] is None:
            bookkeep = bookkeep[:-2]
        self._splay_helper(bookkeep)

    def _splay_helper(self, bookkeep):
        if len(bookkeep) == 1:
            return
        if len(bookkeep) == 3:
            self.single_rotate(bookkeep)
            return
        self.double_rotate(bookkeep)
        self._splay_helper(bookkeep[:-5])

    def single_rotate(self, bookkeep):
        self.zig(*bookkeep[-3:])

    def double_rotate(self, bookkeep):
        branch1 = bookkeep[-4]
        branch2 = bookkeep[-2]
        if branch1 == branch2:
            self.zig_zig(*bookkeep[-5:])
        else:
            self.zig_zag(*bookkeep[-5:])

    def zig_zag(self, node1, branch1, node2, branch2, node3):
        self.zig(node2, branch2, node3)
        self.zig(node1, branch1, node2)

    def zig_zig(self, node1, branch1, node2, branch2, node3):
        self.zig(node1, branch1, node2)
        self.zig(node1, branch2, node3)

    def zig(self, node1, branch, node2):
        if branch == LEFT:
            node1.key, node2.key = (node2.key, node1.key)
            node1.value, node2.value = (node2.value, node1.value)
            node1.left = node2.left
            node2.left = node2.right
            node2.right = node1.right
            node1.right = node2
            return
        if branch == RIGHT:
            node1.key, node2.key = (node2.key, node1.key)
            node1.value, node2.value = (node2.value, node1.value)
            node1.right = node2.right
            node2.right = node2.left
            node2.left = node1.left
            node1.left = node2
            return

    def _track(self, node, key, bookkeep):
        if key == node.key:
            bookkeep.append(node)
            return

        if key < node.key:
            bookkeep += [node, LEFT]
            if node.left is None:
                bookkeep.append(None)
                return
            self._track(node.left, key, bookkeep)
            return

        if key > node.key:
            bookkeep += [node, RIGHT]
            if node.right is None:
                bookkeep.append(None)
                return
            self._track(node.right, key, bookkeep)
            return

    def track(self, key):
        bookkeep = []
        if self.root is None:
            bookkeep.append(None)
        self._track(self.root, key, bookkeep)
        return bookkeep


class SplayTreeImpl2(BinarySearchTree):
    pass


SplayTree = SplayTreeImpl1
