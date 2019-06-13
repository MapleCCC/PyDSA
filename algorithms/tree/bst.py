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
        return iter(self.flatten().items())

    def insert(self, key, value=None):
        if self.root is None:
            self.root = Node(key, value)
            self.size += 1
        else:
            self._insert(self.root, key, value)

    def _insert(self, node, key, value):
        if key == node.key:
            node.value = value
            return

        if key > node.key:
            if node.right is None:
                node.right = Node(key, value)
                self.size += 1
            else:
                self._insert(node.right, key, value)
            return

        if key < node.key:
            if node.left is None:
                node.left = Node(key, value)
                self.size += 1
            else:
                self._insert(node.left, key, value)
            return

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

    # DONE: improve delete performance
    # Done: delete routine also returns the deleted nodes' value. So as to has consistent behaviour with Queue.dequeue, Stack.pop.
    # TODO: Simplify delete routine, right now is too complicated, this should not be such non-trivial.
    def delete(self, key):
        if self.root is None:
            return
        if self.root.key == key:
            if self.root.left is None and self.root.right is None:
                value = self.root.value
                self.root = None
                self.size -= 1
                return value
            else:
                return self._delete_intermediate_node(self.root)
        else:
            return self._delete(self.root, key)

    def _delete(self, node, key):
        if key > node.key:
            if node.right is None:
                return None
            if node.right.key == key:
                return self._delete_child(node, node.right)
            else:
                return self._delete(node.right, key)

        if key < node.key:
            if node.left is None:
                return None
            if key == node.left.key:
                return self._delete_child(node, node.left)
            else:
                return self._delete(node.left, key)

    def _delete_child(self, node, child):
        if child.left is None and child.right is None:
            value = child.value
            if node.left is child:
                node.left = None
            elif node.right is child:
                node.right = None
            else:
                raise ValueError("Fake child !")
            self.size -= 1
            return value
        else:
            return self._delete_intermediate_node(child)

    def _delete_intermediate_node(self, node):
        value = node.value

        if node.left is None:
            if node.right.left is None:
                temp = node.right
                node.right = node.right.right
                self.size -= 1
            else:
                temp = self._delete_min_node(node.right)
            node.key, node.value = temp.key, temp.value
        elif node.right is None:
            if node.left.right is None:
                temp = node.left
                node.left = node.left.left
                self.size -= 1
            else:
                temp = self._delete_max_node(node.left)
            node.key, node.value = temp.key, temp.value

        return value

    def delete_min_node(self):
        """
        Return the min node.
        Return None if tree is empty.
        """
        if self.root is None:
            return None
        if self.root.left is None:
            temp = self.root
            self.root = self.root.right
            self.size -= 1
            return temp
        return self._delete_min_node(self.root)

    def _delete_min_node(self, node):
        if node.left.left is None:
            temp = node.left
            node.left = node.left.right
            self.size -= 1
            return temp
        return self._delete_min_node(node.left)

    def delete_max_node(self):
        """
        Return the max node.
        Return None if tree is empty.
        """
        if self.root is None:
            return None
        if self.root.right is None:
            temp = self.root
            self.root = self.root.left
            self.size -= 1
            return temp
        return self._delete_max_node(self.root)

    def _delete_max_node(self, node):
        if node.right.right is None:
            temp = node.right
            node.right = node.right.left
            self.size -= 1
            return temp
        return self._delete_max_node(node.right)

    def clear(self):
        self.root = None
        self.size = 0

    def find_min_node(self):
        if self.root is None:
            return None
        return self._find_min_node(self.root)

    def _find_min_node(self, node):
        if node.left is None:
            return node
        return self._find_min_node(node.left)

    def find_max_node(self):
        if self.root is None:
            return None
        return self._find_max_node(self.root)

    def _find_max_node(self, node):
        if node.right is None:
            return node
        return self._find_max_node(node.right)

    def flatten(self, order="in_order"):
        flattened = OrderedDict()

        # while self.size != 0:
        #     min_node = self.find_min_node()
        #     order_by_rank[min_node.key] = min_node.value
        #     self.delete(min_node)

        def store_to_result(node):
            flattened[node.key] = node.value
        self.traverse(store_to_result, order)

        return flattened

    def traverse(self, func, order="in_order"):
        """
        func takes a node (of type Node) as parameter
        """
        if order == "pre_order":
            self.pre_order_traverse(func)
        elif order == "post_order":
            self.post_order_traverse(func)
        elif order == "in_order":
            self.in_order_traverse(func)
        else:
            raise ValueError("Wrong ordering chosen.")

    def pre_order_traverse(self, func):
        if self.root is None:
            return
        q = Queue()
        q.enqueue(self.root)
        while not q.isEmpty():
            node = q.dequeue()
            func(node)
            if node.left is not None:
                q.enqueue(node.left)
            if node.right is not None:
                q.enqueue(node.right)

    def post_order_traverse(self, func):
        if self.root is None:
            return
        VISITED = 1
        UNVISITED = 0
        s = Stack()
        s.push([self.root, UNVISITED])
        while not s.isEmpty():
            node, is_visited = s.pop()
            if is_visited == UNVISITED:
                s.push([node, VISITED])
                if node.right is not None:
                    s.push([node.right, UNVISITED])
                if node.left is not None:
                    s.push([node.left, UNVISITED])
            else:
                func(node)

    def in_order_traverse(self, func):
        if self.root is None:
            return
        VISITED = 1
        UNVISITED = 0
        s = Stack()
        s.push([self.root, UNVISITED])
        while not s.isEmpty():
            node, is_visited = s.pop()
            if is_visited == UNVISITED:
                if node.right is not None:
                    s.push([node.right, UNVISITED])
                s.push([node, VISITED])
                if node.left is not None:
                    s.push([node.left, UNVISITED])
            else:
                func(node)

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
