"""
    SplayTree

    Complexity
    ==========
    | Operation | Complexity |
    --------------------------
    | insert | O(H) |
    | delete | O(H) |
    | find | O(H) |
    | splay | O(H) |
    | get size | O(1) |

    where H denotes tree height, which is in average O(logN), where N is number of tree nodes.
    Reference: https://www.sciencedirect.com/science/article/pii/0022000082900046
"""

__all__ = ["SplayTree", "SplayTreeWithMaxsize"]

from .abstract_tree import BinaryTree, BinaryNode as Node
from enum import Enum


class Branch(Enum):
    LEFT = 1
    RIGHT = 0


class SplayTree(BinaryTree):
    def insert(self, data):
        self._splay(data)
        try:
            if data > self._root.data:
                new = Node(data)
                new.left = self._root
                new.right = self._root.right
                self._root.right = None
                self._root = new
                self._size += 1
            elif data < self._root.data:
                new = Node(data)
                new.right = self._root
                new.left = self._root.left
                self._root.left = None
                self._root = new
                self._size += 1
        except AttributeError:
            self._root = Node(data)
            self._size += 1
        return self

    def remove(self, data):
        self._root = self.recur_remove(self._root, data)
        return self

    def recur_remove(self, node, data):
        if node is None:
            return None

        if data == node.data:
            self._size -= 1
            if node.left is not None:
                itr = node.left
                prev = node
                while itr.right is not None:
                    prev = itr
                    itr = itr.right
                prev.right = itr.left
                node.data = itr.data
                return node
            else:
                return node.right
        elif data < node.data:
            node.left = self.recur_remove(node.left, data)
            return node
        else:
            node.right = self.recur_remove(node.right, data)
            return node

    def search(self, data):
        self._splay(data)
        try:
            return True if self._root.data == data else False
        except AttributeError:
            return False

    def _splay(self, data):
        def probe(node):
            if data == node.data:
                return None, None
            elif data < node.data:
                return Branch.LEFT, itr.left
            else:
                return Branch.RIGHT, itr.right

        def zig(parent, branch, child):
            if branch == Branch.LEFT:
                R_min.left = parent
                R_min = parent
                parent.left = None
            else:
                L_max.right = parent
                L_max = parent
                parent.right = None

        def zig_zig(parent, branch1, child, branch2, gchild):
            if branch1 == Branch.LEFT:
                R_min.left = child
                R_min = child
                child.left = None
                parent.left = child.right
                child.right = parent
            else:
                L_max.right = child
                L_max = child
                child.right = None
                parent.right = child.left
                child.left = parent

        def zig_zag(parent, branch1, child, branch2, gchild):
            zig(parent, branch1, child)
            zig(child, branch2, gchild)

        if self.isEmpty():
            return

        # sentinel
        L = Node(None)
        R = Node(None)
        # pointer to mount entry
        L_max = L
        R_min = R

        itr = self._root
        while True:
            branch1, child = probe(itr)
            if child is None:
                break
            branch2, gchild = probe(child)
            if gchild is None:
                zig(itr, branch1, child)
                itr = child
                break
            if branch1 == branch2:
                zig_zig(itr, branch1, child, branch2, gchild)
            else:
                zig_zag(itr, branch1, child, branch2, gchild)
            itr = gchild

        L_max.right = itr.left
        R_min.left = itr.right
        itr.left = L.left
        itr.right = R.right

        self._root = itr


class SplayTreeWithMaxsize(SplayTree):
    """
        The more recently used an entry is, the easier to retrieve it.

        Advantage: can store more amount of data than LRU_Cache
        Disadvantage: uneven access time for different stored data.
        Philosophy is to tradeoff more effort in insertion to save future lookup time. (amortized technique)
        Underlying data structure is splay tree. (linked binary tree)

        Complexity of SplayTreeWithMaxsize is same as those of SplayTree, thanks to careful zero-cost abstraction achieved in programming.

        Complexity
        ==========
        | Operation | Complexity |
        --------------------------
        | insert | O(H) |
        | delete | O(H) |
        | find | O(H) |
        | splay | O(H) |
        | get size | O(1) |

        where H denotes tree height, which is in average O(logN), where N is number of tree nodes.
        Reference: https://www.sciencedirect.com/science/article/pii/0022000082900046
    """

    def __init__(self, maxsize):
        super().__init__()

        if maxsize is not None and not isinstance(maxsize, int):
            raise ValueError("Please use integer value for maxsize.")
        elif maxsize is None:
            self.maxsize = 128
        else:
            self.maxsize = maxsize

    def zig(self, node1, branch, node2):
        super().zig(node1, branch, node2)
        self._update_node_height(node1)
        self._update_node_height(node2)

    def insert(self, data):
        super().insert(data)
        if self._root is None:
            return

        self._update_node_height(self._root.left)
        self._update_node_height(self._root.right)
        self._update_node_height(self._root)

        if self.size > self.maxsize:
            self.delete_deepest_node()

    def _update_node_height(self, node):
        if node is None:
            return

        if node.left is None and node.right is None:
            node.height = 0
        elif node.left is None:
            node.height = node.right.height + 1
        elif node.right is None:
            node.height = node.left.height + 1
        else:
            node.height = max(node.left.height, node.right.height) + 1

    def delete(self, data):
        self._root = self._delete(self._root, data)

    def _delete(self, node, data):
        if node is None:
            return None

        if data == node.data:
            self._size -= 1
            return self._delete_THE_node(node)
        elif data < node.data:
            node.left = self._delete(node.left, data)
        else:
            node.right = self._delete(node.right, data)

        self._update_node_height(node)
        return node

    def _delete_THE_node(self, node):
        if node is None:
            return None
        if node.left is not None:
            bookkeep = []
            self._track_max_node(node.left, bookkeep)
            left_max_node = bookkeep[-1]
            left_max_node.right = node.right
            map(self._update_node_height, bookkeep[::-1])
            return node.left
        else:
            return node.right

    def track_max_node(self):
        bookkeep = []
        self._track_max_node(self._root, bookkeep)
        return bookkeep

    def _track_max_node(self, node, bookkeep):
        if node is None:
            return
        bookkeep.append(node)
        self._track_max_node(node.right, bookkeep)

    def delete_deepest_node(self):
        self._root = self._delete_deepest_node(self._root)

    def _delete_deepest_node(self, node):
        if node is None:
            return None

        if node.left is None and node.right is None:
            self._size -= 1
            return None
        elif node.left is None:
            node.right = self._delete_deepest_node(node.right)
        elif node.right is None:
            node.left = self._delete_deepest_node(node.left)
        elif node.height == node.left.height + 1:
            node.left = self._delete_deepest_node(node.left)
        elif node.height == node.right.height + 1:
            node.right = self._delete_deepest_node(node.right)
        else:
            raise ValueError("Something went wrong.")

        self._update_node_height(node)
        return node
