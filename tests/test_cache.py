import unittest
from random import randint
from time import time

from algorithms.cache import (Clock_Cache, LRU_Cache, SplayTree_Cache,
                              cache_decorator)


class TestLRUCache(unittest.TestCase):
    def setUp(self):
        self.cache = LRU_Cache(maxsize=9)

    def tearDown(self):
        del self.cache

    def trivial_case(self):
        self.cache[6] = 600
        self.cache[9] = 900
        self.cache[4] = 400
        self.cache[1] = 100
        self.cache[5] = 500
        self.cache[3] = 300
        self.cache[7] = 700
        self.cache[8] = 800
        self.cache[2] = 200

    def test(self):
        self.cache[1] = 100
        self.assertEqual(self.cache[1], 100)
        self.cache[1] = 200
        self.assertEqual(self.cache[1], 200)

    def test_delete(self):
        self.cache[1] = 100
        del self.cache[1]
        with self.assertRaises(KeyError):
            self.cache[1]

    def test_maxsize(self):
        self.trivial_case()
        self.assertEqual(self.cache.size, 9)
        self.cache[10] = 1000
        self.assertEqual(self.cache.size, 9)
        with self.assertRaises(KeyError):
            self.cache[6]
        self.cache[11] = 1100
        self.assertEqual(self.cache.size, 9)
        with self.assertRaises(KeyError):
            self.cache[9]


@unittest.skip("Not Implemented")
class TestClockCache(TestLRUCache):
    def setUp(self):
        self.cache = Clock_Cache()


class TestSplayTreeCache(TestLRUCache):
    def setUp(self):
        self.cache = SplayTree_Cache()

    def test_maxsize(self):
        self.trivial_case()
        self.assertEqual(self.cache.size, 9)
        self.cache[10] = 1000
        self.assertEqual(self.cache.size, 9)
        self.cache[11] = 1100
        self.assertEqual(self.cache.size, 9)


def Fibonacci(n):
    assert isinstance(n, int) and n > 0
    if n == 1 or n == 2:
        return 1
    return Fibonacci(n - 1) + Fibonacci(n - 2)


def time_benchmark(func, extent, times):
    begin = time()
    for _ in range(times):
        func(randint(1, extent))
        # print(i)
        # if '__cache__' in dir(func):
        #     print(func.__cache__.size)
    end = time()
    return end - begin


class TestLRUCacheDecorator(unittest.TestCase):
    # def setUp(self):
    #     self.decorator = cache_decorator(maxsize=cache_size)

    def test_wrapping_is_functional(self):
        wrapped_function = cache_decorator(128)(max)
        self.assertEqual(wrapped_function(1, 2), 2)

    @unittest.skip("Time spending. And the test result is unstable.")
    def test_cache_performance(self):
        cache_size = 10
        extent = 30
        times = 50

        wrapped_function = cache_decorator(maxsize=cache_size)(Fibonacci)

        original = time_benchmark(Fibonacci, extent, times)
        new = time_benchmark(wrapped_function, extent, times)

        self.assertLess(new, original)

        # hit = wrapped_function.__cache__.hit
        # miss = wrapped_function.__cache__.miss
        # print("Hit rate: {:.2f}%".format(hit/(hit+miss)*100))

        # print("Hit: {}\n"
        #       "Miss: {}".format(wrapped_function.__cache__.hit, wrapped_function.__cache__.miss))

        # print("Original: {}\nNew: {}".format(original, new))


@unittest.skip("Not implemented")
class TestClockCacheDecorator(TestLRUCacheDecorator):
    pass


class TestSplayTreeCacheDecorator(TestLRUCacheDecorator):
    pass


if __name__ == "__main__":
    unittest.main()
