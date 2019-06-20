from ..queue import Queue


class Node:
    def __init__(self, value):
        self.value = value
        self.children = []

    def __str__(self):
        return "Node(value={})".format(self.value)

    def __repr__(self):
        return self.__str__()

    # for search tree implementation
    def __lt__(self, node):
        if not isinstance(node, Node):
            raise TypeError(
                "'<' not supported between instances of 'Node' and '{}'".format(type(node)))
        return self.value < node.value

    # for seaerch tree implementation
    def __gt__(self, node):
        if not isinstance(node, Node):
            raise TypeError(
                "'>' not supported between instances of 'Node' and '{}'".format(type(node)))
        return self.value > node.value

    # for equality test
    def __eq__(self, node):
        if not isinstance(node, Node):
            return False
        return self.value == node.value

    def swap(self, node):
        if not isinstance(node, Node):
            raise TypeError(
                "Cannot swap 'Node' type with '{}' type.".format(type(node)))
        self.value, node.value = node.value, self.value


# A unique sentinel
NullNode = Node(None)


class Tree:
    def __init__(self):
        self._root = None
        self._size = 0

    def clear(self):
        self._root = None
        self._size = 0
        return self

    @property
    def root(self):
        return self._root.value

    @property
    def size(self):
        return self._size

    def isEmpty(self):
        return self.size == 0

    def __len__(self):
        return self.size

    def __str__(self):
        return self._recursive_str(self._root)

    def _recursive_str(self, node):
        if len(node.children) == 0:
            return "Node(value={})".format(node.value)
        else:
            return "Node(value={}, children=[{}])".format(node.value, ', '.join(self._recursive_str(child) for child in node.children))

    def __repr__(self):
        return str(self)

    def __iter__(self):
        return self.traverse()

    # traversal returns an iterator, utilize power of lazy evaluation to save space and reduce overhead.
    def traverse(self, order=None):
        """
            'Generator Factory' pattern
            Calling this function will return a generator.
            Iterating over the generator will retrieve the tree node in given order.
            Note that the retrieval is real-time, which means altering the tree between two consecutive generator call may result in different results.
        """
        if order is None:
            order = self.__class__.default_traversal_order

        for node in self._traverse(order):
            yield node.value

    default_traversal_order = "breadth_first_order"

    def _traverse(self, order):
        if not isinstance(order, str):
            raise ValueError("`order` should be string.")
        try:
            return getattr(self, order+"_traverse")()
        except AttributeError:
            raise ValueError("Wrong ordering chosen.")

    def pre_order_traverse(self):
        return self._pre_order_traverse(self._root)

    def _pre_order_traverse(self, node):
        if node is NullNode:
            return
        yield node
        for child in node.children:
            yield from self._pre_order_traverse(child)

    def post_order_traverse(self):
        return self._post_order_traverse(self._root)

    def _post_order_traverse(self, node):
        if node is NullNode:
            return
        for child in node.children:
            yield from self._post_order_traverse(child)
        yield node

    def breadth_first_order_traverse(self):
        q = Queue()
        q.enqueue(self._root)
        while not q.isEmpty():
            node = q.dequeue()
            if node is not NullNode:
                yield node
                for child in node.children:
                    q.enqueue(child)

    # def visualize(self):
    #     q = Queue()

    #     def log(node):
    #         q.enqueue(node.key)
    #     self.traverse(log, order="pre_order")

    #     h = self.height

    #     node_num_of_full_tree = 2 ** h - 1
    #     res = node_num_of_full_tree - q.size
    #     for _ in range(res):
    #         q.enqueue(' ')
    #     print("\n")
    #     for n in range(h):
    #         margin = ' ' * (3 * h - 3 * n - 2)
    #         interval = ' ' * 5
    #         s = margin
    #         for _ in range(2 ** n):
    #             s += str(q.dequeue()) + interval
    #         s = s[:-5]
    #         s += margin
    #         print(s)
    #     print("\n")


M_aryNullNode = M_aryNode(None)


class M_aryNode(Node):
    def __init__(self, value, branch=2):
        super().__init__(value)
        self.children = [M_aryNullNode] * branch


class M_aryTree(Tree):
    def __init__(self, m):
        super().__init__()
        if not isinstance(m, int) or m <= 0:
            raise ValueError("Valid branch number is a natural number.")
        self.branch = m


# Sentinel
BinaryNullNode = BinaryNode(None)
BinaryNullNode.left = BinaryNullNode.right = BinaryNullNode


class BinaryNode(M_aryNode):
    def __init__(self, value):
        super().__init__(value, branch=2)

    @property
    def left(self):
        return self.children[0]

    @left.setter
    def left(self, node):
        if not isinstance(node, BinaryNode) or node is not BinaryNullNode:
            raise ValueError
        self.children[0] = node

    @property
    def right(self):
        return self.children[1]

    @right.setter
    def right(self, node):
        if not isinstance(node, BinaryNode) or node is not BinaryNullNode:
            raise ValueError
        self.children[1] = node


class BinaryTree(M_aryTree):
    def __init__(self):
        super().__init__(m=2)


if __name__ == '__main__':
    tree1 = Tree()
    tree1._root = Node(0)
    tree1._root.children = [Node(1), Node(2), Node(3)]
    tree1._root.children[0].children = [Node(4), Node(2), Node(3)]

    tree2 = Tree()
    tree2._root = Node(0)
    tree2._root.children = [Node(4), Node(2), Node(3)]

    print(list(tree1.pre_order_traverse()))
    print(tree1)
    print(tree2)
