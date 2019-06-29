__all__ = ["Cache", "cache_decorator"]

import gc
from functools import wraps

from .recency_tracker import RecencyTracker
from .tree.splay_tree import SplayTreeWithMaxsize


class LRU_Cache:
    """
        Accessing every item is equally fast. The size is limited. When cache is full, further insertion requires that the least recently used item is discarded.

        Advantage: quick access to any items.
        Disadvantage: relatively limited size.
        Philosophy is to tradeoff time with space.
        Underlying data structure is hash table. (dictionary primitive data type in Python)

        Reference: the *LRU cache mechanism* part in the source code of the `functools` standard library.

        Complexity
        ----------
        | Operation | Complexity |
        ==========================
        | get item | Amortized analysis needed |
        | set item | O(1) |
        | delete item | O(1) |
    """

    def __init__(self, maxsize=128):
        if not isinstance(maxsize, int) or maxsize <= 0:
            raise ValueError("Invalid *maxsize* setting")
        self._maxsize = maxsize
        self._storage = {}
        self._recency_tracker = RecencyTracker()
        self._hit = 0
        self._miss = 0

    __slots__ = ["_maxsize", "_storage",
                 "_recency_tracker", "_hit", "_miss"]

    def clear(self):
        self._storage.clear()
        self._recency_tracker.clear()
        self._hit = 0
        self._miss = 0

    @property
    def size(self):
        return len(self._storage)

    def __len__(self):
        return self.size

    def statistic(self):
        return self._hit, self._miss

    def __getitem__(self, key):
        try:
            value = self._storage[key]
            self._hit += 1
            self._recency_tracker.update_mru(key)
            return value
        except KeyError:
            self._miss += 1
            raise

    def __setitem__(self, key, value):
        self._storage[key] = value
        self._recency_tracker.update_mru(key)

        # TODO: concurrency, multi-threaded
        if self.size > self._maxsize:
            self.discard_lru()
            assert self.size <= self._maxsize

    def discard_lru(self):
        try:
            key = self._recency_tracker.pop_lru()
            del self._storage[key]
        except IndexError:
            raise IndexError("Empty cache has nothing to discard")

    def __delitem__(self, key):
        del self._storage[key]
        self._recency_tracker.remove(key)



class Clock_Cache:
    def __init__(self, maxsize=128):
        raise NotImplementedError


class ComparableWrapper:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __lt__(self, arg):
        assert isinstance(arg, ComparableWrapper)
        return self.key < arg.key

    def __gt__(self, arg):
        assert isinstance(arg, ComparableWrapper)
        return self.key > arg.key

    def __eq__(self, arg):
        assert isinstance(arg, ComparableWrapper)
        return self.key == arg.key


class SplayTree_Cache(SplayTreeWithMaxsize):
    def __init__(self, maxsize=128):
        super().__init__(maxsize)
        self._hit = 0
        self._miss = 0

    def insert(self, key, value):
        result = self.find(key)
        if result is None:
            super().insert(ComparableWrapper(key, value))
        elif result == value:
            return
        else:
            self.delete(key)
            super().insert(ComparableWrapper(key, value))

    def find(self, key):
        result = super().find(ComparableWrapper(key, None))
        if result is True:
            self._hit += 1
            return self.root.value
        else:
            self._miss += 1
            return None

    def delete(self, key):
        super().delete(ComparableWrapper(key, None))

    @property
    def hit(self):
        return self._hit

    @property
    def miss(self):
        return self._miss

    @property
    def hit_rate(self):
        return self._hit / (self._hit + self._miss)


# Alias
Cache = LRU_Cache


def hash_function_arguments(*args, **kw):
    # When there is only one argument and its type is trivial, we simply return itself as a key.
    # This is for accelerating lookup speed, which is critical factor in Cache application.
    # Some of ideas here owe reference and inspiration from Python's built-in
    # functools module's source code.
    trivial_type = (int, str, frozenset, type(None))
    if len(args) == 1 and len(kw) == 0 and isinstance(args[0], trivial_type):
        return args[0]

    global SENTINEL
    SENTINEL = object()
    return hash((*args, SENTINEL, *kw.items()))


def cache_decorator(maxsize=128):
    """
        Decorator.
        Arguments to the user function must be hashable.
    """
    def decorator(user_function):
        cache = Cache()

        @wraps(user_function)
        def wrapper(*args, **kw):
            try:
                key = hash_function_arguments(*args, **kw)
                return cache[key]
            except TypeError:
                raise ValueError("arguments passed to function {} is unhashable: {}".format(user_function.__name__, (args, kw)))
            except KeyError:
                value = user_function(*args, **kw)
                cache[key] = value
                return value

        wrapper.__cache__ = cache
        return wrapper

    return decorator


# An implementation trick is we can use age_bit and PriorityQueue to
# emulate an actual splay tree. Not as efficient as splay tree, but far
# easier to implement.
