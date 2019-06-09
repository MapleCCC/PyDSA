__all__ = ['TransliterateCache']

from .splay_tree import SplayTree


def hash(key_list):
    # return "-".join([str(key) for key in key_list])
    return tuple(key_list)


class TransliterateCache:
    def __init__(self, max_cache_size=100):
        self.storage = SplayTree()
        self.max_cache_size = max_cache_size

    # Return candidate_word_list or None
    def query(self, key_list):
        hash_code = hash(key_list)
        return self.storage.find(hash_code)

    def store(self, key_list, candidate_word_list):
        hash_code = hash(key_list)
        self.storage.insert(hash_code, candidate_word_list)

        if self.storage.size >= self.max_cache_size:
            self.storage.prune()
