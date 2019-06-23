__all__ = ["Cache", "cache_decorator"]

import gc
from functools import wraps
from .tree.splay_tree import SplayTreeWithMaxsize


sentinel = object()

MAX_MEM_ALLOC = 2 ** 12


class ValueWrapper:
    # provide zero-argument initializatioon
    def __init__(self, value=None, index=None):
        self.value = value
        self.index = index

    def __str__(self):
        return "(value={}, index={})".format(self.value, self.index)

    def __repr__(self):
        return str(self)


class LRU_Cache:
    """
        Accessing every item is equally fast. The size is limited. When cache is full, further insertion requires that the least recently used item is discarded.

        Advantage: quick access to any items.
        Disadvantage: relatively limited size.
        Philosophy is to tradeoff time with space.
        Underlying data structure is hash table. (dictionary primitive data type in Python)

        Reference to the *LRU cache mechanism* part in the source code of the `functools` standard library.

        Complexity
        ----------
        | Operation | Complexity |
        ==========================
        | get item | Amortized analysis needed |
        | set item | O(1) |
        | delete item | O(1) |
    """

    def __init__(self, maxsize=128):
        assert isinstance(maxsize, int)
        self._maxsize = maxsize if maxsize > 0 else 1
        self._storage = {}
        self._recency = []  # keep track of the recency ranking
        self._hit = 0
        self._miss = 0
        self._offset = 0

    __slots__ = ["_maxsize", "_storage",
                 "_recency", "_hit", "_miss", "_offset"]

    def clear(self):
        self._storage.clear()
        self._recency.clear()
        self._hit = 0
        self._miss = 0
        self._offset = 0

    @property
    def size(self):
        return len(self._storage)

    def __len__(self):
        return self.size

    def statistic(self):
        return self._hit, self._miss

    def update_MRU(self, key):
        try:
            self._recency[self._storage[key].index] = sentinel
        except TypeError:
            pass
        self._recency.append(key)
        self._storage[key].index = len(self._recency) - 1

    def __getitem__(self, key):
        try:
            value = self._storage[key].value
            self._hit += 1
            self.update_MRU(key)
            return value
        except KeyError:
            self._miss += 1
            raise

    def __setitem__(self, key, value):
        self._storage[key] = ValueWrapper(value)
        self.update_MRU(key)

        # TODO: concurrency, multi-threaded
        if self.size > self._maxsize:
            self.discard_lru()
            assert self.size <= self._maxsize

        # no need to calculate _storage size, since it's bounded by self._maxsize, just subtract _maxsize frm MAX_MEM_ALLOC will do the trick.
        if len(self._recency) > MAX_MEM_ALLOC:
            self.squash()

    def discard_lru(self):
        for index, key in enumerate(self._recency[self._offset:]):
            if key is not sentinel:
                del self[key]
                self._offset = index + 1
                break

    # Garbage collect
    def squash(self):
        temp = []
        for key in self._recency[self._offset:]:
            if key is not sentinel:
                temp.append(key)
                self._storage[key].index = len(temp) - 1
        self._recency = temp
        gc.collect()

    def __delitem__(self, key):
        self._recency[self._storage[key].index] = sentinel
        del self._storage[key]


class Clock_Cache:
    def __init__(self, maxsize=128):
        pass


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
    global sentinel
    sentinel = object()
    return hash((*args, sentinel, *kw.items()))


def cache_decorator(maxsize=128):
    """
        Decorator.
        Arguments to the user function must be hashable.
    """
    def decorator(user_function):
        cache = Cache()
        @wraps(user_function)
        def wrapper(*args, **kw):
            key = hash_function_arguments(*args, **kw)
            try:
                return cache[key]
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
