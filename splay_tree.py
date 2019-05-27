__all__ = ['SplayTree']

from .splay_tree_impl import SplayTree


class SplayTreeStub:
    def __init__(self):
        pass

    def find(self, key):
        return None

    def insert(self, key, value):
        pass

    @property
    def size(self):
        return 0

    def prune(self):
        pass


# class SplayTree(SplayTreeStub):
#     pass
