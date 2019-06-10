__all__ = ['SplayTree']


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = None


class SplaySubTree:
    def __init__(self, node=None):
        self.node = node

    # INPUT: (key, value) pair
    # Insert the key-value entry into tree, and push it upward while preserving tree balance state.
    # If a node with same key already exists, will cover its content.
    def insert(self, key, value):
        if self.is_empty_tree():
            new_node = Node(key, value)
            self.node = new_node
        else:
            self.insert_helper(key, value)
            self.splay(key)

    # recursive function helper
    def insert_helper(self, key, value):
        if key < self.node.key:
            if self.node.left is not None:
                SplaySubTree(self.node.left).insert_helper(key, value)
            else:
                new_node = Node(key, value)
                new_node.parent = self.node
                self.node.left = new_node
        elif key > self.node.key:
            if self.node.right is not None:
                SplaySubTree(self.node.right).insert_helper(key, value)
            else:
                new_node = Node(key, value)
                new_node.parent = self.node
                self.node.right = new_node
        else:  # when key == self.node.key
            self.node.value = value

    def find_max_key(self):
        if self.is_empty_tree():
            return None
        if self.node.right is None:
            return self.node.key, self.node.value
        key = SplaySubTree(self.node.right).find_max_key_helper()
        self.splay(key)
        return self.node.key, self.node.value

    # recursive function helper
    def find_max_key_helper(self):
        if self.node.right is None:
            return self.node.key
        else:
            return SplaySubTree(self.node.right).find_max_key_helper()

    def find_min_key(self):
        if self.is_empty_tree():
            return None
        if self.node.left is None:
            return self.node.key, self.node.value
        key = SplaySubTree(self.node.left).find_min_key_helper()
        self.splay(key)
        return self.node.key, self.node.value

    def find_min_key_helper(self):
        if self.node.left is None:
            return self.node.left
        else:
            return SplaySubTree(self.node.left).find_min_key_helper()

    # No return value to indicate if the desired key is found.
    def delete(self, key):
        if self.find(key) is None:
            return

        if self.node.left is None and self.node.right is None:
            self.node = None
        elif self.node.left is not None:
            SplaySubTree(self.node.left).find_max_key()
            self.node.left.right = self.node.right
            self.node.left.parent = self.node.parent
            self.node = self.node.left
        else:
            SplaySubTree(self.node.right).find_min_key()
            self.node.right.left = self.node.left
            self.node.right.parent = self.node.parent
            self.node = self.node.right

    # INPUT: key
    # OUPUT: matched value or None
    def find(self, key):
        if self.is_empty_tree():
            return None
        self.splay(key)
        if key == self.node.key:
            return self.node.value
        else:
            return None

    def is_left_subtree_of_parent(self):
        if self.is_empty_tree():
            return False
        if self.has_no_parent():
            return False
        return self.node.key < self.node.parent.key

    def zig(self):
        if self.is_empty_tree():
            return
        if self.has_no_parent():
            return

        if self.is_left_subtree_of_parent():
            grand_parent = self.node.parent.parent
            self.node.parent.parent = self.node
            self.node.parent.left = self.node.right
            self.node.right = self.node.parent
            self.node.parent = grand_parent
        else:
            grand_parent = self.node.parent.parent
            self.node.parent.parent = self.node
            self.node.parent.right = self.node.left
            self.node.left = self.node.parent
            self.node.parent = grand_parent

    def zig_zig(self):
        if self.is_empty_tree():
            return
        if self.has_no_parent():
            return
        if self.has_no_grand_parent():
            return

        SplayTree(self.node.parent).zig()
        self.zig()

    # It's funny that despite the name, zig_zag actually perfroms zig twice.
    def zig_zag(self):
        if self.is_empty_tree():
            return
        if self.has_no_parent():
            return
        if self.has_no_grand_parent():
            return

        self.zig()
        self.zig()

    def is_empty_tree(self):
        return self.size == 0

    def has_no_parent(self):
        if self.is_empty_tree():
            return True
        else:
            return self.node.parent is None

    def has_no_grand_parent(self):
        if self.has_no_parent():
            return True
        else:
            return self.node.parent.parent is None

    def push_oneself_upward(self):
        if self.is_empty_tree():
            return
        while not self.has_no_parent():
            if self.has_no_grand_parent():
                self.zig()
            elif self.is_left_subtree_of_parent() == SplayTree(self.node.parent).is_left_subtree_of_parent():
                self.zig_zig()
            else:
                self.zig_zag()

    # INPUT: key
    #   Find the node whose key matches input, and push the node upward with tree rotations that preserve balance state.
    # OUTPUT: boolean indicating whether succeed in finding the key
    def splay(self, key):
        new_root = self.splay_helper(key)
        if new_root is None:
            return False
        else:
            self.node = new_root
            return True

    # OUTPUT: root of rearranged tree, i.e., the node with key inputted. None
    # if key is not found.
    def splay_helper(self, key):
        if self.is_empty_tree():
            return None

        if key < self.node.key:
            return SplaySubTree(self.node.left).splay_helper(key)
        elif key > self.node.key:
            return SplaySubTree(self.node.right).splay_helper(key)
        else:  # When key == self.node.key
            self.push_oneself_upward()
            return self.node

    # An ugly workaround
    def splay_nearest_key(self, key):
        self.find_max_key()
        itr = self.node
        while itr is not None:
            if key >= itr.key:
                left_distance = key - itr.key
                right_distance = itr.parent.key - key
                if left_distance > right_distance:
                    self.splay(itr.parent.key)
                else:
                    self.splay(itr.key)
                return
            else:
                itr = itr.left

    def __len__(self):
        return self.size

    def __str__(self):
        self.find_max_key()
        itr = self.node
        temp = []
        while itr is not None:
            temp.append((itr.key, itr.value))
            itr = itr.left
        return "A splay tree object: %s" % temp

    __repr__ = __str__

    # An ugly temporary implementation
    def __iter__(self):
        self.find_max_key()
        itr = self.node
        temp = []
        while itr is not None:
            temp.append((itr.key, itr.value))
            itr = itr.left
        return iter(temp)

    @property
    def size(self):
        if self.node is None:
            return 0
        else:
            return 1 + SplaySubTree(self.node.left).size + \
                SplaySubTree(self.node.right).size

    # Reduce size by half
    # Expensive operation, be cautious to use.
    # In order to do it efficiently, we need to maintain the middle-key.
    def cut_by_half(self):
        if self.size == 0:
            return
        if self.size == 1:
            return

        self.find_max_key()
        itr = self.node
        for _ in range(self.size // 2):
            itr = itr.left
        itr.parent.left = None

    def prune(self):
        self.cut_by_half()


# The difference between SplayTree and SplaySubTree is that SplaySubTree is parent-aware.
# While SplayTree has no parent information,
# that is, it assume itself is an independent, free, dettached, orphan tree.
class SplayTree(SplaySubTree):
    def __init__(self, root=None):
        SplaySubTree.__init__(self, root)
        if self.node is not None:
            self.node.parent = None
