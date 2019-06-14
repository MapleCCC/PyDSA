"""
BinarySearchTree

Complexity:
| Operation | Complexity |
----------------------
| insert() | O(H) |
| find() | O(H) |
| delete() | O(H) |
| get size | O(1) |
| get height | O(N) |

where H denotes tree height, which is in average O(logN), where N is number of nodes.
"""

__all__ = ["BinarySearchTree", "BST", "LazyBinarySearchTree"]

import inspect
import types
import math
from collections import OrderedDict
from ..queue import Queue
from ..stack import Stack


def check_comparable(func):
    error_messages = {"'<' not supported", "'>' not supported",
                      "'==' not supported", "'>=' not supported", "'<=' not supported"}

    def wrapper(*args, **kw):
        try:
            return func(*args, **kw)
        except TypeError as e:
            for err in error_messages:
                if str(e).startswith(err):
                    raise ValueError("Key should be comparable.")
            raise e
    return wrapper


def decorate_all_methods(decorator):
    def decorate(cls):
        for name, func in inspect.getmembers(cls):
            if isinstance(func, types.FunctionType):
                setattr(cls, name, decorator(func))
        return cls
    return decorate


class Node:
    def __init__(self, key, value=None):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

    def __str__(self):
        return "Node(key={}, value={})".format(self.key, self.value)
        # return "({}, {})".format(self.key, self.value)

    def __repr__(self):
        return self.__str__()


@decorate_all_methods(check_comparable)
class BinarySearchTree:
    """
    key should be comparable
    """

    def __init__(self):
        self.root = None
        self.size = 0

    # TODO: make height computation O(1) instead of O(N)
    @property
    def height(self):
        return self._height(self.root)

    def _height(self, node):
        if node is None:
            return 0
        return 1 + max(self._height(node.left), self._height(node.right))

    def isEmpty(self):
        return self.size == 0

    def __len__(self):
        return self.size

    def __iter__(self):
        # in_order traversal retrieves nodes in sorted order
        return iter(self.flatten("in_order").items())

    def insert(self, key, value=None):
        self.root = self._insert(self.root, key, value)

    def _insert(self, node, key, value):
        if node is None:
            self.size += 1
            return Node(key, value)

        if key == node.key:
            node.value = value
        elif key < node.key:
            node.left = self._insert(node.left, key, value)
        else:
            node.right = self._insert(node.right, key, value)

        return node

    def find(self, key):
        """
            Return None if not found.
        """
        return self._find(self.root, key)

    def _find(self, node, key):
        if node is None:
            return None

        if key == node.key:
            return node.value
        elif key > node.key:
            return self._find(node.right, key)
        else:
            return self._find(node.left, key)

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
            return node
        else:
            node.right = self._delete(node.right, key)
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
        self.root = self._delete_min_node(self.root)

    def _delete_min_node(self, node):
        if node is None:
            return None
        if node.left is None:
            return None
        node.left = self._delete_min_node(node.left)
        return node

    def delete_max_node(self):
        self.root = self._delete_max_node(self.root)

    def _delete_max_node(self, node):
        if node is None:
            return None
        if node.right is None:
            return None
        node.right = self._delete_max_node(node.right)
        return node

    def clear(self):
        self.root = None
        self.size = 0

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

    def flatten(self, order="in_order"):
        flattened = OrderedDict()

        def log(key, value):
            flattened[key] = value
        self.traverse(log, order)
        return flattened

    def traverse(self, func, order="in_order"):
        """
        func takes two parameters: key, value
        """
        def wrapper(node):
            return func(node.key, node.value)

        return self._traverse(wrapper, order)

    def _traverse(self, func, order="in_order"):
        """
        func takes one parameter: node
        """
        if order == "pre_order":
            self.pre_order_traverse(func)
        elif order == "post_order":
            self.post_order_traverse(func)
        elif order == "in_order":
            self.in_order_traverse(func)
        elif order == "out_order":
            self.out_order_traverse(func)
        elif order == "breadth_first_order":
            self.breadth_first_order_traverse(func)
        else:
            raise ValueError("Wrong ordering chosen.")

    def pre_order_traverse(self, func):
        self._pre_order_traverse(self.root, func)

    def _pre_order_traverse(self, node, func):
        if node is None:
            return
        func(node)
        self._pre_order_traverse(node.left, func)
        self._pre_order_traverse(node.right, func)

    def post_order_traverse(self, func):
        self._post_order_traverse(self.root, func)

    def _post_order_traverse(self, node, func):
        if node is None:
            return
        self._post_order_traverse(node.left, func)
        self._post_order_traverse(node.right, func)
        func(node)

    def in_order_traverse(self, func):
        self._in_order_traverse(self.root, func)

    def _in_order_traverse(self, node, func):
        if node is None:
            return
        self._in_order_traverse(node.left, func)
        func(node)
        self._in_order_traverse(node.right, func)

    def out_order_traverse(self, func):
        self._out_order_traverse(self.root, func)

    def _out_order_traverse(self, node, func):
        if node is None:
            return
        self._out_order_traverse(node.right, func)
        func(node)
        self._out_order_traverse(node.left, func)

    def breadth_first_order_traverse(self, func):
        q = Queue()
        q.enqueue(self.root)
        while not q.isEmpty():
            node = q.dequeue()
            if node is not None:
                func(node)
                q.enqueue(node.left)
                q.enqueue(node.right)

    # def visualize(self):
    #     q = Queue()

    #     def log(node):
    #         q.enqueue(node.key)
    #     self.traverse(log, order="pre_order")

    #     h = self.height

    #     node_num_of_full_tree = 2 ** h - 1
    #     res = node_num_of_full_tree - q.size
    #     for _ in range(res):
    #         q.enqueue(' ')
    #     print("\n")
    #     for n in range(h):
    #         margin = ' ' * (3 * h - 3 * n -2)
    #         interval = ' ' * 5
    #         s = margin
    #         for _ in range(2 ** n):
    #             s += str(q.dequeue()) + interval
    #         s = s[:-5]
    #         s += margin
    #         print(s)
    #     print("\n")


class LazyBinarySearchTree(BinarySearchTree):
    def __init__(self):
        super().__init__()
        self.gabbages = []

    def clear(self):
        super().clear()
        self.gabbages.clear()

    def gabbage_collect(self):
        flattend = self.flatten(order="pre_order")
        self.root = None
        self.size = 0
        for k, v in flattend.items():
            if k in self.gabbages:
                self.gabbages.remove(k)
            else:
                self.insert(k, v)

    def delete(self, key):
        return self.lazy_delete(key)

    def lazy_delete(self, key):
        if self.root is None:
            return None
        return self._lazy_delete(self.root, key)

    def _lazy_delete(self, node, key):
        if key == node.key:
            value = node.value
            self.gabbages.append(node.key)
            if len(self.gabbages) / self.size >= 0.1:
                self.gabbage_collect()
            return value

        if key < node.key:
            if node.left is None:
                return None
            return self._delete(node.left, key)

        if key > node.key:
            if node.right is None:
                return None
            return self._delete(node.right, key)


# Alias
BST = BinarySearchTree
