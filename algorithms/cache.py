__all__ = ["Cache", "cache_decorator"]

from functools import wraps
from .tree.splay_tree import SplayTreeWithMaxsize


def calculate_key(*args, **kw):
    # When there is only one argument and its type is trivial, we simply return itself as a key.
    # This is for accelerating lookup speed, which is critical factor in Cache application.
    # Some of ideas here owe reference and inspiration from Python's built-in
    # functools module's source code.
    trivial_type = {int, str, frozenset, type(None)}
    if len(args) == 1 and len(kw) == 0 and type(args[0]) in trivial_type:
        return args[0]

    arguments: list = args
    keywords: dict = kw
    global sentinel
    sentinel = object()
    pickled = arguments + (sentinel,)
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
        Arguments to the user function must be hashable.
    """
    def decorator(user_function):
        cache = Cache(algorithm, maxsize)
        @wraps(user_function)
        def wrapper(*args, **kw):
            key = calculate_key(*args, **kw)
            query_result = cache.find(key)
            if query_result is not None:
                return query_result
            return_value = user_function(*args, **kw)
            cache.insert(key, return_value)
            return return_value
        wrapper.__cache__ = cache
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
                ('''You should choose a valid cache algorithm. Options include following:
                1. LRU
                    Least recently used entry is discarded when the cache is full.
                2. Clock
                    [......]
                3. SplayTree
                    More recently accessed entry is easier to retrieve.'''))
        self.algorithm = algorithm

    def insert(self, key, value):
        self._cache.insert(key, value)

    def find(self, key):
        return self._cache.find(key)

    def delete(self, key):
        self._cache.delete(key)

    @property
    def hit(self):
        return self._cache.hit

    @property
    def miss(self):
        return self._cache.miss

    @property
    def hit_rate(self):
        return self._cache.hit_rate

    @property
    def size(self):
        return self._cache.size

    def __str__(self):
        return self._cache.__class__.__name__

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return self.size


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
        | insert | O(1) |
        | delete | O(N) |
        | find | O(1) |
    """

    def __init__(self, maxsize=128):
        if maxsize is not None and not isinstance(maxsize, int):
            raise ValueError("Please use integer value for maxsize.")
        if maxsize is None:
            self.maxsize = 128
        else:
            self.maxsize = maxsize

        self._cache = {}
        self._recency_bookkeep = []  # keep track of the least recently used entry
        self._hit = 0
        self._miss = 0

    def insert(self, key, value):
        result = self._find(key)
        if result is not None:
            if result == value:
                self._recency_bookkeep.remove(key)
                self._recency_bookkeep.insert(0, key)
                return
            else:
                self._recency_bookkeep.remove(key)
        elif len(self._cache) == self.maxsize:
            # delete the least recently used entry
            lru_entry = self._recency_bookkeep[-1]
            self.delete(lru_entry)

        self._cache[key] = value
        self._recency_bookkeep.insert(0, key)

        # print("The bookkeep is {}".format(self._recency_bookkeep))

    def _find(self, key):
        if key in self._cache.keys():
            return self._cache[key]
        else:
            return None

    def find(self, key):
        result = self._find(key)
        if result is None:
            self._miss += 1
        else:
            self._hit += 1
        return result

    def delete(self, key):
        if key in self._cache:
            del self._cache[key]
            self._recency_bookkeep.remove(key)

    @property
    def hit(self):
        return self._hit

    @property
    def miss(self):
        return self._miss

    @property
    def size(self):
        return len(self._cache)

    def __len__(self):
        return self.size

    @property
    def hit_rate(self):
        return self.hit/(self.hit+self.miss)


class Clock_Cache:
    def __init__(self, maxsize):
        pass


class SplayTree_Cache(SplayTreeWithMaxsize):
    def __init__(self, maxsize):
        super().__init__(maxsize)
        self._hit = 0
        self._miss = 0

    def find(self, key):
        result = super().find(key)
        if result is None:
            self._miss += 1
        else:
            self._hit += 1
        return result

    @property
    def hit(self):
        return self._hit

    @property
    def miss(self):
        return self._miss

    @property
    def hit_rate(self):
        return self.hit/(self.hit+self.miss)

# An implementation trick is we can use age_bit and PriorityQueue to
# emulate an actual splay tree. Not as efficient as splay tree, but far
# easier to implement.
