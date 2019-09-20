__all__ = ["RecencyTracker"]

import gc

# Sentinel Object Pattern
DELETED = object()

# Other than shrink which is expensive, we can also consider reuse the slice _storage[:offset]
# try examining the Round Robin data structure and its complexity
# Also possible: randomized version, return not necessary strictly least recently used entry.


class RecencyTracker:
    """
    Complexity:
    -----------
    | get(pop)_lru | amortized O() |
    | update_mru | amortized O(1) |
    | remove | O(1) |

    Space complexity:
    -----------------
    Depends on `_gc_check` detail
    """

    def __init__(self):
        # _storage holds all the elements in recency order. Least recently used on the left.
        # some elements in _storage are garbage.
        self._storage = []
        # _indexer tracks the element's position in _storage
        self._indexer = {}
        # _offset marks a position in _storage, to the left of which are all garbage. Maintain for speed-up other operations.
        self._offset = 0

    __slots__ = ['_storage', '_indexer', '_offset']

    def clear(self):
        self._storage.clear()
        self._indexer.clear()
        self._offset = 0

    @property
    def size(self):
        return len(self._indexer)

    def pop_lru(self):
        for index, entry in enumerate(self._storage, self._offset):
            # traverse from the position marked by _offset to the right, until the first non-garbage element is found.
            if entry is not DELETED:
                # Found the least recenlty used entry.
                # Update the _offset to mark the newest position where to the left of it are all garbage.
                self._offset = index + 1
                # Instead of deleting an element from the middle of a list, which is expensive, we lazily mark it as DELETED
                self._storage[index] = DELETED
                del self._indexer[entry]
                return entry
        raise IndexError("pop lru from empty recency tracker")

    def get_lru(self):
        for index, entry in enumerate(self._storage, self._offset):
            # traverse from the position marked by _offset to the right, until the first non-garbage element is found.
            if entry is not DELETED:
                # Found the least recenlty used entry.
                # Update the _offset to mark the newest position where to the left of it are all garbage.
                self._offset = index
                return entry
        raise IndexError("get lru from empty recency tracker")

    def update_mru(self, entry):
        try:
            self.remove(entry)
        except ValueError:
            pass
        self._storage.append(entry)
        self._indexer[entry] = len(self._storage) - 1

        if self._gc_check():
            self._garbage_collect()

    def remove(self, entry):
        try:
            index = self._indexer[entry]
            # Instead of deleting an element from the middle of a list, which is expensive, we lazily mark it as DELETED
            self._storage[index] = DELETED
            del self._indexer[entry]
        except KeyError:
            raise ValueError("entry not in tracker")

    # TODO find commonly used reasonable good-performant critieria from industrial practice or academia theoretical reasoning
    def _gc_check(self):
        """
        Criteria of choosing check condition is
        1. reduce space waste
        2. avoid excessive and frequenct garbage collection causing large overhead
        """
        too_much_hole = len(self._storage) - \
            self._offset > 2 * len(self._indexer)
        offset_too_long = len(self._storage) > 2 * self._offset
        return too_much_hole or offset_too_long

    def _garbage_collect(self):
        too_much_hole = len(self._storage) - \
            self._offset > 2 * len(self._indexer)
        offset_too_long = len(self._storage) > 2 * self._offset

        if too_much_hole:
            # Squashing
            self._storage = [entry for entry in self._storage if entry is not DELETED]
            self._indexer = dict(enumerate(self._storage))
            self._offset = 0
        elif offset_too_long:
            # Shrinking
            self._storage = self._storage[self._offset:]
            for entry in self._indexer:
                self._indexer[entry] -= self._offset
            self._offset = 0
