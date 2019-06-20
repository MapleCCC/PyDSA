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

LEFT = 1
RIGHT = 0


class BottomUpSplayTree(BinaryTree):
    def insert(self, value):
        self._splay(value)

        if self.root is None:
            self.root = Node(value)
            self.size += 1
            return

        if value == self.root.value:
            return

        if value > self.root.value:
            new = Node(value)
            new.left = self.root
            new.right = self.root.right
            self.root.right = None
            self.root = new
            self.size += 1
            return

        if value < self.root.value:
            new = Node(value)
            new.right = self.root
            new.left = self.root.left
            self.root.left = None
            self.root = new
            self.size += 1
            return

    def delete(self, value):
        self.root = self._delete(self.root, value)

    def _delete(self, node, value):
        if node is None:
            return None

        if value == node.value:
            self.size -= 1
            return self._delete_THE_node(node)
        elif value < node.value:
            node.left = self._delete(node.left, value)
            return node
        else:
            node.right = self._delete(node.right, value)
            return node

    def _delete_THE_node(self, node):
        if node is None:
            return None
        if node.left is not None:
            left_max_node = self._find_max_node(node.left)
            left_max_node.right = node.right
            return node.left
        else:
            return node.right

    def find_min_node(self):
        return self._find_min_node(self.root)

    def _find_min_node(self, node):
        if node is None:
            return None
        if node.left is None:
            return node
        return self._find_min_node(node.left)

    def find_max_node(self):
        return self._find_max_node(self.root)

    def _find_max_node(self, node):
        if node is None:
            return None
        if node.right is None:
            return node
        else:
            return self._find_max_node(node.right)

    def find(self, value):
        self._splay(value)

        if self.root is None:
            return False

        if value == self.root.value:
            return True
        else:
            return False

    def _splay(self, value):
        bookkeep = self.track(value)

        if bookkeep[-1] is None:
            # if the value cannot be found, splay last visited node instead.
            # Such strategy is for some implementation methods of `insert` and `find`
            path_nodes = bookkeep[:-2]
        else:
            path_nodes = bookkeep

        self._splay_helper(path_nodes)

    def _splay_helper(self, path_nodes):
        if len(path_nodes) in {0, 1}:
            return
        elif len(path_nodes) == 3:
            self.single_rotate(*path_nodes[-3:])
            self._splay_helper(path_nodes[:-2])
        elif len(path_nodes) >= 5:
            self.double_rotate(*path_nodes[-5:])
            self._splay_helper(path_nodes[:-4])
        else:
            raise ValueError(
                "Something went wrong. path_nodes is {}".format(path_nodes))

    def single_rotate(self, node1, branch, node2):
        self.zig(node1, branch, node2)

    def double_rotate(self, node1, branch1, node2, branch2, node3):
        if branch1 == branch2:
            self.zig_zig(node1, branch1, node2, branch2, node3)
        else:
            self.zig_zag(node1, branch1, node2, branch2, node3)

    def zig_zag(self, node1, branch1, node2, branch2, node3):
        self.zig(node2, branch2, node3)
        self.zig(node1, branch1, node2)

    def zig_zig(self, node1, branch1, node2, branch2, node3):
        self.zig(node1, branch1, node2)
        self.zig(node1, branch2, node3)

    def zig(self, node1, branch, node2):
        # Note that we should manipulate node1 and node2's pointer
        # instead of directly reassign themselves
        # because of Python's pass-by-object-reference mechanism
        node1.swap(node2)

        if branch == LEFT:
            node1.left = node2.left
            node2.left = node2.right
            node2.right = node1.right
            node1.right = node2
        elif branch == RIGHT:
            node1.right = node2.right
            node2.right = node2.left
            node2.left = node1.left
            node1.left = node2
        else:
            raise ValueError("Something went wrong.")

    def track(self, value):
        bookkeep = []
        self._track(self.root, value, bookkeep)
        return bookkeep

    def _track(self, node, value, bookkeep):
        if node is None:
            bookkeep.append(node)
            return

        if value == node.value:
            bookkeep.append(node)
            return
        elif value < node.value:
            bookkeep += [node, LEFT]
            self._track(node.left, value, bookkeep)
        else:
            bookkeep += [node, RIGHT]
            self._track(node.right, value, bookkeep)


# TODO: implement top down splay tree.
class TopDownSplayTree(BinaryTree):
    pass


SplayTree = BottomUpSplayTree


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

    def insert(self, key, value=None):
        super().insert(key, value)
        if self.root is None:
            return

        self._update_node_height(self.root.left)
        self._update_node_height(self.root.right)
        self._update_node_height(self.root)

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

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if node is None:
            return None

        if key == node.key:
            self.size -= 1
            return self._delete_THE_node(node)
        elif key < node.key:
            node.left = self._delete(node.left, key)
        else:
            node.right = self._delete(node.right, key)

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
        self._track_max_node(self.root, bookkeep)
        return bookkeep

    def _track_max_node(self, node, bookkeep):
        if node is None:
            return
        bookkeep.append(node)
        self._track_max_node(node.right, bookkeep)

    def delete_deepest_node(self):
        self.root = self._delete_deepest_node(self.root)

    def _delete_deepest_node(self, node):
        if node is None:
            return None

        if node.left is None and node.right is None:
            self.size -= 1
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
