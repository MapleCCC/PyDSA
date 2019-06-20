"""
    BinarySearchTree

    Interface:
    ==========
    insert(key, value): `value` defaults to `None`.
    delete(key)
    find(key): Return matched value, or `None` if not found.
    traverse(func, order): `func` takes `key` and `value` as parameters. `order` can be one of `pre_order`, `post_order`, in_order`, `out_order`, or `breadth_first_order`.
    flatten(order): Similar to `traverse()` but return an `OrderedDict`.
    isEmpty()
    height()
    clear()
    size

    Private helper methods: (DON'T use them in user code!)
    ==================
    find_min_node
    find_max_node
    delete_min_node
    delete_max_node

    Methods prefixed with underscore are private helper methods.
    They are not intended for public exposure or usage out of its containing scope.
    Their implementation detail might be subject to change in the future.
    It's recommended to adhere to API explicitly provided.


    Complexity:
    ===========
    | Operation | Complexity |
    ----------------------
    | insert() | O(H) |
    | find() | O(H) |
    | delete() | O(H) |
    | traverse() | O(N) |
    | clear() | O(1) |
    | get size | O(1) |
    | get height | O(N) |

    where N is number of nodes.
    where H denotes tree height, which is in average O(logN). Reference: https://www.sciencedirect.com/science/article/pii/0022000082900046
"""

__all__ = ["BinarySearchTree", "BST"]


from functools import wraps

from ..utils import decorate_all_methods
from .abstract_tree import BinaryTree, BinaryNode as Node


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
        return self._height(self._root)

    def _height(self, node):
        if node is None:
            return 0
        return 1 + max(self._height(node.left), self._height(node.right))

    def insert(self, value):
        self._root = self._insert(self._root, value)

    def _insert(self, node, value):
        if node is None:
            self.size += 1
            return Node(value)

        if value == node.value:
            return node
        elif value < node.value:
            node.left = self._insert(node.left, value)
            return node
        else:
            node.right = self._insert(node.right, value)
            return node

    def find(self, value):
        return self._find(self._root, value)

    def _find(self, node, value):
        if node is None:
            return False

        if value == node.value:
            return True
        elif value > node.value:
            return self._find(node.right, value)
        else:
            return self._find(node.left, value)

    def delete(self, value):
        self._root = self._delete(self._root, value)

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

    def delete_min_node(self):
        self._root = self._delete_min_node(self._root)

    def _delete_min_node(self, node):
        if node is None:
            return None
        if node.left is None:
            self.size -= 1
            return None
        node.left = self._delete_min_node(node.left)
        return node

    def delete_max_node(self):
        self._root = self._delete_max_node(self._root)

    def _delete_max_node(self, node):
        if node is None:
            return None
        if node.right is None:
            self.size -= 1
            return None
        node.right = self._delete_max_node(node.right)
        return node

    def find_min_node(self):
        return self._find_min_node(self._root)

    def _find_min_node(self, node):
        if node is None:
            return None
        if node.left is None:
            return node
        return self._find_min_node(node.left)

    def find_max_node(self):
        return self._find_max_node(self._root)

    def _find_max_node(self, node):
        if node is None:
            return None
        if node.right is None:
            return node
        else:
            return self._find_max_node(node.right)

    default_traversal_order = "in_order"

    def in_order_traverse(self):
        """
            `in_order` traversal retrieves nodes in sorted order
        """
        return self._in_order_traverse(self._root)

    def _in_order_traverse(self, node):
        if node is None:
            return
        yield from self._in_order_traverse(node.left)
        yield node
        yield from self._in_order_traverse(node.right)

    def out_order_traverse(self):
        return self._out_order_traverse(self._root)

    def _out_order_traverse(self, node):
        if node is None:
            return
        yield from self._out_order_traverse(node.right)
        yield node
        yield from self._out_order_traverse(node.left)


# Alias
BST = BinarySearchTree
