from algorithms.cache import Cache, cache_decorator
import unittest
from time import time
from random import randint


class TestCache(unittest.TestCase):
    cache_algorithm = "LRU"

    def setUp(self):
        self.cache = Cache(self.__class__.cache_algorithm, maxsize=9)

    def tearDown(self):
        del self.cache

    def trivial_case(self):
        self.cache.insert(6, 600)
        self.cache.insert(9, 900)
        self.cache.insert(4, 400)
        self.cache.insert(1, 100)
        self.cache.insert(5, 500)
        self.cache.insert(3, 300)
        self.cache.insert(7, 700)
        self.cache.insert(8, 800)
        self.cache.insert(2, 200)

    def test_insert(self):
        self.cache.insert(1, 100)
        self.assertEqual(self.cache.find(1), 100)
        self.cache.insert(1, 200)
        self.assertEqual(self.cache.find(1), 200)

    def test_delete(self):
        self.cache.insert(1, 100)
        self.cache.delete(1)
        self.assertIsNone(self.cache.find(1))

    def test_maxsize(self):
        self.trivial_case()
        self.assertEqual(self.cache.size, 9)
        self.cache.insert(10, 1000)
        self.assertEqual(self.cache.size, 9)
        self.assertIsNone(self.cache.find(6))
        self.cache.insert(11, 1100)
        self.assertEqual(self.cache.size, 9)


class TestLRUCache(TestCache):
    cache_algorithm = "LRU"


@unittest.skip("Not Implemented")
class TestClockCache(TestCache):
    cache_algorithm = "Clock"


class TestSplayTreeCache(TestCache):
    cache_algorithm = "SplayTree"

    def test_maxsize(self):
        self.trivial_case()
        self.assertEqual(self.cache.size, 9)
        self.cache.insert(10, 1000)
        self.assertEqual(self.cache.size, 9)
        self.cache.insert(11, 1100)
        self.assertEqual(self.cache.size, 9)


def Fibonacci(n):
    if not isinstance(n, int) and n > 0:
        raise ValueError("Invalid input value.")
    if n == 1 or n == 2:
        return 1
    return Fibonacci(n - 1) + Fibonacci(n - 2)


def duration_benchmark(func, extent, times):
    begin = time()
    for _ in range(times):
        func(randint(1, extent))
        # print(i)
        # if '__cache__' in dir(func):
        #     print(func.__cache__.size)
    end = time()
    return end - begin


class TestCacheDecorator(unittest.TestCase):
    cache_algorithm = "LRU"

    def test_wrapping_is_functional(self):
        wrapped_function = cache_decorator(
            self.__class__.cache_algorithm, 128)(max)
        self.assertEqual(wrapped_function(1, 2), 2)

    @unittest.skip("Time spending. And the test result is unstable.")
    def test_cache_performance(self):
        cache_size = 10
        extent = 30
        times = 50

        wrapped_function = cache_decorator(
            self.__class__.cache_algorithm, maxsize=cache_size)(Fibonacci)

        original = duration_benchmark(Fibonacci, extent, times)
        new = duration_benchmark(wrapped_function, extent, times)

        # hit = wrapped_function.__cache__.hit
        # miss = wrapped_function.__cache__.miss
        # print("Hit rate: {:.2f}%".format(hit/(hit+miss)*100))

        # print("Hit: {}\n"
        #       "Miss: {}".format(wrapped_function.__cache__.hit, wrapped_function.__cache__.miss))

        # print("Original: {}\nNew: {}".format(original, new))

        self.assertLess(new, original)


@unittest.skip("Not implemented")
class TestClockCacheDecorator(TestCacheDecorator):
    cache_algorithm = "Clock"


class TestSplayTreeCacheDecorator(TestCacheDecorator):
    cache_algorithm = "SplayTree"


if __name__ == "__main__":
    unittest.main()
