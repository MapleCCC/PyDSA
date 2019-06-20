"""
    BinarySearchTree

    Interface:
    ==========
    insert(value)
    delete(value)
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
    | delete() | O(H) |
    | traverse() | O(N) |
    | clear() | O(1) |
    | size | O(1) |
    | height | O(N) |

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
        return self.recur_height(self._root)

    def recur_height(self, node):
        if node is None:
            return 0
        return 1 + max(self.recur_height(node.left), self.recur_height(node.right))

    def insert(self, value):
        self._root = self.recur_insert(self._root, value)
        return self

    def recur_insert(self, node, value):
        if node is None:
            self._size += 1
            return Node(value)

        if value == node.value:
            return node
        elif value < node.value:
            node.left = self.recur_insert(node.left, value)
            return node
        else:
            node.right = self.recur_insert(node.right, value)
            return node

    def search(self, value):
        return self.recur_search(self._root, value)

    def recur_search(self, node, value):
        if node is None:
            return False

        if value == node.value:
            return True
        elif value > node.value:
            return self.recur_search(node.right, value)
        else:
            return self.recur_search(node.left, value)

    def delete(self, value):
        self._root = self.recur_delete(self._root, value)
        return self

    def recur_delete(self, node, value):
        if node is None:
            return None

        if value == node.value:
            self._size -= 1
            if node.left is not None:
                itr = node.left
                prev = node
                while itr.left is not None:
                    prev = itr
                    itr = itr.left
                prev.left = None
                node.value = itr.value
                return node
            else:
                return node.right
        elif value < node.value:
            node.left = self.recur_delete(node.left, value)
            return node
        else:
            node.right = self.recur_delete(node.right, value)
            return node

    default_traversal_order = "in_order"

    def in_order_traverse(self):
        """
            `in_order` traversal retrieves nodes in sorted order
        """
        return self.recur_in_order_traverse(self._root)

    def recur_in_order_traverse(self, node):
        if node is None:
            return
        yield from self.recur_in_order_traverse(node.left)
        yield node
        yield from self.recur_in_order_traverse(node.right)

    def out_order_traverse(self):
        return self.recur_out_order_traverse(self._root)

    def recur_out_order_traverse(self, node):
        if node is None:
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
