__all__ = ["BinarySearchTree", "BST"]

import inspect
import types
import math
from queue import Queue

# class Tree:
#     pass

# Empty_Tree = object()


def check_comparable(func):
    error_messages = {"'<' not supported",
                      "'>' not supported", "'==' not supported", "'>=' not supported", "'<=' not supported"}

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

    def _insert(self, node, key, value=None):
        if key == node.key:
            node.value = value
            return

        if key > node.key:
            if node.right is None:
                node.right = Node(key, value)
                self.size += 1
                return
            else:
                self._insert(node.right, key, value)

        if key < node.key:
            if node.left is None:
                node.left = Node(key, value)
                self.size += 1
                return
            else:
                self._insert(node.left, key, value)

    def insert(self, key, value=None):
        if self.root is None:
            self.root = Node(key, value)
            self.size += 1
        else:
            self._insert(self.root, key, value)

    def _find(self, node, key):
        if key == node.key:
            return node.value

        if key > node.key:
            if node.right is None:
                return None
            return self._find(node.right, key)

        if key < node.key:
            if node.left is None:
                return None
            return self._find(node.left, key)

    def find(self, key):
        """
            Return None if not found.
        """
        if self.root is None:
            return None
        return self._find(self.root, key)

    def delete_node(self, node):
        # This comment block not workable, because Python is pass-by-object-reference.
        # if node.left is None and node.right is None:
        #     node = None
        #     self.size -= 1
        #     return

        if node.left is None:
            new = self._find_min_node(node.right)
            key, value = new.key, new.value
            self._delete(node, new.key)
            node.key, node.value = key, value
            return

        if node.right is None:
            new = self._find_max_node(node.left)
            key, value = new.key, new.value
            self._delete(node, new.key)
            node.key, node.value = key, value
            return

    def _delete(self, node, key):
        if key == node.key:
            self.delete_node(node)
            return

        if key > node.key:
            if node.right is None:
                return
            if key == node.right.key and node.right.left is None and node.right.right is None:
                node.right = None
                self.size -= 1
            else:
                self._delete(node.right, key)
            return

        if key < node.key:
            if node.left is None:
                return
            if key == node.left.key and node.left.left is None and node.left.right is None:
                node.right = None
                self.size -= 1
            else:
                self._delete(node.left, key)
            return

    def delete(self, key):
        if self.root is None:
            return
        if key == self.root.key and self.root.left is None and self.root.right is None:
            self.root = None
            self.size -= 1
        else:
            self._delete(self.root, key)

    def _find_min_node(self, node):
        if node.left is None:
            return node
        return self._find_min_node(node.left)

    def find_min_node(self):
        if self.root is None:
            return None
        return self._find_min_node(self.root)

    def _find_max_node(self, node):
        if node.right is None:
            return node
        return self._find_max_node(node.right)

    def find_max_node(self):
        if self.root is None:
            return None
        return self._find_max_node(self.root)


# Alias
BST = BinarySearchTree
