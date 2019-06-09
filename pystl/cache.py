__all__ = ["Cache", "cache_decorator"]

import functools


SPECIAL_OBJECT = object()


def calculate_key(*args, **kw):
    # When there is only one argument and its type is trivial, we simply return itself as a key.
    # This is for accelerating lookup speed, which is critical factor in Cache application.
    # Some of ideas here owe reference and inspiration from Python's built-in
    # functools module's source code.
    if len(args) == 1 and type(args[0]) in {int, str, frozenset, type(None)}:
        return args[0]
    arguments: list = args
    keywords: dict = kw
    pickled = arguments + (SPECIAL_OBJECT,)
    for k, v in enumerate(keywords):
        pickled += (k, v)
    pickled = tuple(pickled)
    try:
        return hash(pickled)
    except TypeError:
        raise ValueError(
            "Function with cache decorator only accepts hashable arguments.")


def cache_decorator(algorithm="LRU", maxsize=None):
    """
    Decorator.
    Arguments to the user function must be hashale.
    """
    def decorator(user_function):
        cache = Cache(algorithm, maxsize)
        @functools.wraps(user_function)
        def wrapper(*args, **kw):
            key = calculate_key(*args, **kw)
            query_result = cache.find(key)
            if query_result is not None:
                return query_result
            return_value = user_function(*args, **kw)
            cache.insert(key, return_value)
            return return_value
        return wrapper
    return decorator


class Cache:
    def __init__(self, algorithm="LRU", maxsize=None):
        if algorithm == "LRU":
            self._cache = LRU_Cache(maxsize)
        elif algorithm == 'Clock':
            self._cache = Clock_Cache(maxsize)
        elif algorithm == "SplayTree":
            self._cache = SplayTree_Cache(maxsize)
        else:
            raise ValueError(
                ('''You should choose a valid cache algorithm. Options include                     following: '''))

    def insert(self, key, value):
        self._cache.insert(key, value)

    def find(self, key):
        return self._cache.find(key)

    def delete(self, key):
        self._cache.delete(key)

    def __str__(self):
        return self._cache.__class__.__name__

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return len(self._cache)


class LRU_Cache:
    """
    Accessing every item is equally fast. The size is limited. When cache is full, further insertion requires that the least recently used item is discarded.

    Advantage: quick access to any items.
    Disadvantage: relatively limited size.
    Philosophy is to tradeoff time with space.
    Underlying data structure is hash table. (dictionary primitive data type in Python)

    Reference to the *LRU cache mechanism* part in the source code of the `functools` standard library.

    Use class level property instead of object level property. This is for persistent cache data through program lifetime.
    """

    def __init__(self, maxsize=128):
        if maxsize is not None and not isinstance(maxsize, int):
            raise ValueError("Please use integer value for maxsize.")
        if maxsize is None:
            self.maxsize = 128
        else:
            self.maxsize = maxsize

        self._cache = {}
        self.recency_bookkeep = []  # keep track of the least recently used entry

    def insert(self, key, value):
        result = self.find(key)
        if result is not None:
            if result == value:
                self.recency_bookkeep.remove(key)
                self.recency_bookkeep.insert(0, key)
                return
            else:
                self.recency_bookkeep.remove(key)
        elif len(self._cache) == self.maxsize:
            # delete the least recently used entry
            lru_entry = self.recency_bookkeep[-1]
            self.delete(lru_entry)

        self._cache[key] = value
        self.recency_bookkeep.insert(0, key)

        # print("The bookkeep is {}".format(self.recency_bookkeep))

    def find(self, key):
        try:
            return self._cache[key]
        except KeyError:
            return None

    def delete(self, key):
        if key in self._cache:
            del self._cache[key]
            self.recency_bookkeep.remove(key)

    def __len__(self):
        return len(self._cache)


class Clock_Cache:
    def __init__(self, maxsize):
        pass


class SplayTree_Cache:
    """
    The more recently used an entry is, the easier to retrieve it.

    Advantage: can store more amount of data than LRU_Cache
    Disadvantage: uneven access time for different stored data
    Philosophy is to tradeoff space with time.
    Underlying data structure is splay tree. (linked binary tree)
    """


# An implementation trick is we can use age_bit and PriorityQueue to
# emulate an actual splay tree. Not as efficient as splay tree, but far
# easier to implement.
