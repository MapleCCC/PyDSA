from ..cache import *
import unittest
from time import time
from random import randint


class TestCache(unittest.TestCase):
    cache_algorithm = "LRU"

    def setUp(self):
        self.cache = Cache(self.__class__.cache_algorithm)

    def tearDown(self):
        del self.cache

    def test_insert(self):
        self.cache.insert(1, 100)
        self.assertEqual(self.cache.find(1), 100)

    def test_delete(self):
        self.cache.insert(1, 100)
        self.cache.delete(1)
        self.assertIsNone(self.cache.find(1))


class TestLRUCache(TestCache):
    cache_algorithm = "LRU"


@unittest.skip("No Implemented")
class TestSplayTreeCache(TestCache):
    cache_algorithm = "SplayTree_Cache"


def Fibonacci(n):
    if not isinstance(n, int) and n > 0:
        raise ValueError("Invalid input value.")
    if n == 1 or n == 2:
        return 1
    return Fibonacci(n - 1) + Fibonacci(n - 2)


def duration_benchmark(func):
    extent = 30
    times = 50
    begin = time()
    for i in range(times):
        func(randint(1, extent))
        # print(i)
    end = time()
    return end - begin


class TestCacheDecorator(unittest.TestCase):
    def test_wrapping_functional(self):
        wrapped_function = cache_decorator("LRU", 128)(max)
        self.assertEqual(wrapped_function(1, 2), 2)

    @unittest.skip("Time spending.")
    def test_cache_performance(self):
        cache_size = 10

        wrapped_function = cache_decorator("LRU", cache_size)(Fibonacci)

        original = duration_benchmark(Fibonacci)
        new = duration_benchmark(wrapped_function)

        # print("Original: {}\nNew: {}".format(original, new))

        self.assertLess(new, original)
