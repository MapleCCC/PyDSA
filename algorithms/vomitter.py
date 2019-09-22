from enum import Enum
from math import fabs, floor
from random import expovariate, normalvariate


class RVDistribution(Enum):
    NORMAL = 0
    EXP = 1


class Vomitter:
    """
    Randomly pick a value from storage.
    The more recently a value is added, the more likely it's picked.
    """

    def __init__(self, maxsize=None):
        if maxsize is None:
            self._maxsize = 128
        elif not isinstance(maxsize, int) or maxsize < 1:
            raise ValueError(
                "Invalid value for parameter `maxsize`: {}".format(maxsize))
        else:
            self._maxsize = maxsize
        self._storage = []

    __slots__ = ['_storage', '_maxsize']

    def clear(self):
        self._storage.clear()

    def add(self, element):
        self._storage.append(element)

        # delete oldest element to save space
        if len(self._storage) > self._maxsize:
            self._storage.pop(0)

    def emit(self, distribution=RVDistribution.NORMAL):
        if self._storage == []:
            raise IndexError("Emit from empty vomitter")
        if len(self._storage) == 1:
            return self._storage[0]

        N = len(self._storage)

        if distribution == RVDistribution.NORMAL:
            # """
            # Elements are emitted following normal distribution.
            # The most recently added element corresponds to peak of normal distribution curve.
            # The least recently added element corresponds to the 3-sigma position of normal distribution curve.
            # Other elements are located in between, in an equidistance manner.
            # """
            # For normal distribution, three sigma corresponds to tail probability of 0.99730
            mu = 0
            sigma = (N - 1) / 3
            r = fabs(normalvariate(mu, sigma))
        elif distribution == RVDistribution.EXP:
            # For exponential distribution, 5-sigma corresponds to tail probability of 0.99752
            lambda_ = 6 / (N - 1)
            r = expovariate(lambda_)

        # Use N as threshold instead of N=1
        if r <= N:
            index = N - 1 - floor(r)
            return self._storage[index]
        else:
            # if the random number generated go beyond threshold,
            # then just output the most recently added element.
            return self._storage[-1]


if __name__ == '__main__':
    rr = Vomitter()
    for i in range(100):
        rr.add(i)

    count = 0
    while True:
        ret = rr.emit(RVDistribution.EXP)
        count += 1
        if ret == 99:
            print("Iterated {} rounds until found 99".format(count))
            break
