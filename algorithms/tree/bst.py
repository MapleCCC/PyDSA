"""
    BinarySearchTree

    Interface:
    ==========
    insert(value)
    remove(value)
    search(value): Return True if found and False otherwise.
    traverse(order): `order` can be one of `pre_order`, `post_order`, in_order`, `out_order`, or `breadth_first_order`.
    isEmpty()
    height
    clear()
    size

    Private helper methods: (DON'T use them in user code!)
    ==================
    [......]

    Methods prefixed with underscore are private helper methods.
    They are not intended for public exposure or usage out of its containing scope.
    Their implementation detail might be subject to change in the future.
    It's recommended to adhere to API explicitly provided.


    Complexity:
    ===========
    | Operation | Complexity |
    ----------------------
    | insert() | O(H) |
    | search() | O(H) |
    | remove() | O(H) |
    | traverse() | O(N) |
    | clear() | O(1) |
    | size | O(1) |
    | height | O(N) |

    where N is number of nodes.
    where H denotes tree height, which is in average O(logN). Reference: https://www.sciencedirect.com/science/article/pii/0022000082900046
"""

__all__ = ["BinarySearchTree", "BST"]


import random
from functools import wraps

from ..utils import decorate_all_methods
from .binary_tree import SENTINEL
from .binary_tree import BinaryNode as Node
from .binary_tree import BinaryTree


def check_comparable(func):
    error_messages = {"'<' not supported", "'>' not supported",
                      "'==' not supported", "'>=' not supported", "'<=' not supported"}

    @wraps(func)
    def wrapper(*args, **kw):
        try:
            return func(*args, **kw)
        except TypeError as e:
            for err in error_messages:
                if str(e).startswith(err):
                    raise ValueError("Key should be comparable.")
            raise e
    return wrapper


@decorate_all_methods(check_comparable)
class BinarySearchTree(BinaryTree):
    """
        Key should be comparable (and orderable)?
    """

    # TODO: make height computation O(1) instead of O(N)
    @property
    def height(self):
        return self.recur_height(self._root)

    def recur_height(self, node):
        if node.data is SENTINEL:
            return 0
        return 1 + max(self.recur_height(node.left), self.recur_height(node.right))

    def insert(self, data):
        self._root = self.recur_insert(self._root, data)
        return self

    def recur_insert(self, node, data):
        if node.data is SENTINEL:
            self._size += 1
            new = Node(data)
            new.left = new.right = Node(SENTINEL)
            return new

        if data == node.data:
            return node
        elif data < node.data:
            node.left = self.recur_insert(node.left, data)
            return node
        else:
            node.right = self.recur_insert(node.right, data)
            return node

    def search(self, data):
        return self.recur_search(self._root, data)

    def recur_search(self, node, data):
        if node.data is SENTINEL:
            return False

        if data == node.data:
            return True
        elif data > node.data:
            return self.recur_search(node.right, data)
        else:
            return self.recur_search(node.left, data)

    def remove(self, data):
        self.recur_remove(self._root, data)
        return self

    def recur_remove(self, node, data):
        if node.data is SENTINEL:
            return

        if data < node.data:
            self.recur_remove(node.left, data)
        elif data > node.data:
            self.recur_remove(node.right, data)
        else:
            self._remove_node(node)

    def _remove_node(self, node):

        def replace_with_left_max(node):
            assert node.left.data is not SENTINEL
            left_max = node.left
            prev = node
            while left_max.right.data is not SENTINEL:
                prev = left_max
                left_max = left_max.right
            prev.right = left_max.left
            node.data = left_max.data

        def replace_with_right_min(node):
            assert node.right.data is not SENTINEL
            right_min = node.right
            prev = node
            while right_min.left.data is not SENTINEL:
                prev = right_min
                right_min = right_min.left
            prev.left = right_min.right
            node.data = right_min.data

        if node.data is SENTINEL:
            return

        self._size -= 1

        has_left_child = node.left.data is not SENTINEL
        has_right_child = node.right.data is not SENTINEL

        if not has_left_child and not has_right_child:
            node.data = SENTINEL
            node.left = node.right = None
        elif has_left_child and has_right_child:
            # Randomly pick node to delete from two choices:
            # "max node in left sub tree", or "min node in right sub tree"
            if random.choice([0, 1]):
                replace_with_left_max(node)
            else:
                replace_with_right_min(node)
        elif has_left_child:
            replace_with_left_max(node)
        else:
            replace_with_right_min(node)


    default_traversal_order = "in_order"

    def in_order_traverse(self):
        """
            `in_order` traversal retrieves nodes in sorted order
        """
        return self.recur_in_order_traverse(self._root)

    def recur_in_order_traverse(self, node):
        if node.data is SENTINEL:
            return
        yield from self.recur_in_order_traverse(node.left)
        yield node
        yield from self.recur_in_order_traverse(node.right)

    def out_order_traverse(self):
        return self.recur_out_order_traverse(self._root)

    def recur_out_order_traverse(self, node):
        if node.data is SENTINEL:
            return
        yield from self.recur_out_order_traverse(node.right)
        yield node
        yield from self.recur_out_order_traverse(node.left)


# Alias
BST = BinarySearchTree

if __name__ == '__main__':
    tree1 = BST()
    tree1.insert(2).insert(1).insert(4).insert(3).insert(5).delete(5)

    print(tree1)
