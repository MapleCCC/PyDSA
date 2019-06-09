from collections import Iterable


def quick_sort(array: Iterable):
    """
    sort in-place.
    descendance ordering.
    unstable. Doesn't preserve ordering.
    Raise TypeError if elemenets in array are non-comparable.
    Raise ValueError if the subject is not iterable.
    """

    if not isinstance(array, Iterable):
        raise ValueError("Quicksort algorithm only accepts list as argument.")

    n = len(array)

    if n == 0 or n == 1:
        return array

    pivot = array[0]
    p = 1
    q = n - 1

    while True:
        while array[q] >= pivot and p < q:
            q -= 1
        while array[p] < pivot and p < q:
            p += 1
        if p == q:
            break
        else:
            array[p], array[q] = (array[q], array[p])

    if pivot <= array[p]:
        return [pivot] + quick_sort(array[1:])
    else:
        return quick_sort(array[1:p + 1]) + [pivot] + quick_sort(array[p + 1:])


def bucket_sort(array):
    pass


def select_sort(array):
    pass


def heap_sort(array):
    pass


def bubble_sort(array):
    return array


sorting_algorithms = [quick_sort, select_sort,
                      heap_sort, bubble_sort, bucket_sort]

__all__ = [algorithm.__name__ for algorithm in sorting_algorithms]
