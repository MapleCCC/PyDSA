from algorithms.sort import *
import unittest
from collections import Counter


class TestSort(unittest.TestCase):
    # def __init__(self, sorting_algorithm):
    #     super().__init__()
    #     self.sorting_algorithm = sorting_algorithm

    # @classmethod
    # def setUpClass(cls):
    #     cls.sorting_algorithm = lambda x: x

    sorting_algorithm = quick_sort

    def test_empty_array(self):
        self.verify([])

    def test_single_element_array(self):
        self.verify([1])

    def test_trivial_sort(self):
        self.verify([1, 5, 2, 7])

    def test_duplicate_element(self):
        self.verify([8, 5, 11, 7, 5])

    def test_zero(self):
        self.verify([1, 6, 4, 0])

    def test_negative_number(self):
        self.verify([8, 5, 11, 7, -1])

    def test_invalid_argument(self):
        with self.assertRaises(ValueError):
            self.__class__.sorting_algorithm(1)

    def test_incomparable(self):
        with self.assertRaises(TypeError):
            self.__class__.sorting_algorithm([dict(), dict()])

    def verify(self, array):
        self._formally_verify_sorting_result(
            self.__class__.sorting_algorithm, array)

    def _formally_verify_sorting_result(self, sorting_algorithm, array):
        input = array
        output = sorting_algorithm(array)

        self.assertEqual(Counter(input), Counter(output))

        for i in range(len(output) - 1):
            self.assertLessEqual(output[i], output[i + 1])


class TestQuickSort(TestSort):
    sorting_algorithm = quick_sort


@unittest.skip("Not yet implemented")
class TestSelectSort(TestSort):
    sorting_algorithm = select_sort


@unittest.skip("Not yet implemented")
class TestHeapSort(TestSort):
    sorting_algorithm = heap_sort


# suite = unittest.TestSuite()
# suite.addTest(TestQuickSort())

# unittest.TextTestRunner().run(suite)

# unittest.main()

if __name__ == "__main__":
    unittest.main()
