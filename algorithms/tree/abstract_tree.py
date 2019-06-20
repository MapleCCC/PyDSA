from ..queue import Queue


class Node:
    def __init__(self, key, value=None):
        self.key = key
        self.value = value
        self.children = []

    def __str__(self):
        # return "({}, {})".format(self.key, self.value)
        return "Node(key={}, value={})".format(self.key, self.value)

    def __repr__(self):
        return self.__str__()

    # for search tree implementation
    def __lt__(self, node):
        if not isinstance(node, Node):
            raise TypeError(
                "'<' not supported between instances of 'Node' and '{}'".format(type(node)))
        return self.key < node.key

    # for seaerch tree implementation
    def __gt__(self, node):
        if not isinstance(node, Node):
            raise TypeError(
                "'>' not supported between instances of 'Node' and '{}'".format(type(node)))
        return self.key > node.key

    # for equality test
    def __eq__(self, node):
        if not isinstance(node, Node):
            return False
        return self.key == node.key and self.value == node.value

    def swap(self, node):
        if not isinstance(node, Node):
            raise TypeError(
                "Cannot swap 'Node' type with '{}' type.".format(type(node)))
        self.key, node.key = node.key, self.key
        self.value, node.value = node.value, self.value


class Tree:
    def __init__(self):
        self.root = None
        self.size = 0

    def clear(self):
        self.root = None
        self.size = 0

    def isEmpty(self):
        return self.size == 0

    def __len__(self):
        return self.size

    def __str__(self):
        return self._recursive_str(self.root)

    def _recursive_str(self, node):
        if node is None:
            return 'None'
        if len(node.children) == 0:
            return "Node(key={}, value={})".format(node.key, node.value)
        else:
            return "Node(key={}, value={}, children=[{}])".format(node.key, node.value, ', '.join(self._recursive_str(child) for child in node.children))

    def __repr__(self):
        return str(self)

    def pre_order_traverse(self, func):
        """
            func takes one parameter: node
        """
        self._pre_order_traverse(self.root, func)

    def _pre_order_traverse(self, node, func):
        if node is None:
            return
        func(node)
        for child in node.children:
            self._pre_order_traverse(child, func)

    def post_order_traverse(self, func):
        """
            func takes one parameter: node
        """
        self._post_order_traverse(self.root, func)

    def _post_order_traverse(self, node, func):
        if node is None:
            return
        for child in node.children:
            self._post_order_traverse(child, func)
        func(node)

    def breadth_first_order_traverse(self, func):
        """
            func takes one parameter: node
        """
        q = Queue()
        q.enqueue(self.root)
        while not q.isEmpty():
            node = q.dequeue()
            if node is not None:
                func(node)
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


class M_aryNode(Node):
    def __init__(self, key, value=None, branch=2):
        super().__init__(key, value)
        self.children = [None] * branch


class M_aryTree(Tree):
    def __init__(self, m):
        super().__init__()
        if not isinstance(m, int) or m <= 0:
            raise ValueError("Valid branch number is a natural number.")
        self.branch = m


class BinaryNode(M_aryNode):
    def __init__(self, key, value=None):
        super().__init__(key, value, branch=2)

    @property
    def left(self):
        return self.children[0]

    @left.setter
    def left(self, node):
        if not isinstance(node, (Node, type(None))):
            raise ValueError
        self.children[0] = node

    @property
    def right(self):
        return self.children[1]

    @right.setter
    def right(self, node):
        if not isinstance(node, (Node, type(None))):
            raise ValueError
        self.children[1] = node


class BinaryTree(M_aryTree):
    def __init__(self):
        super().__init__(m=2)


if __name__ == '__main__':
    tree1 = Tree()
    tree1.root = Node(0, 0)
    tree1.root.children = [Node(0, 1), Node(0, 2), Node(0, 3)]
    tree1.root.children[0].children = [Node(0, 4), Node(0, 2), Node(0, 3)]

    tree2 = Tree()
    tree2.root = Node(0, 0)
    tree2.root.children = [Node(0, 4), Node(0, 2), Node(0, 3)]

    tree1.pre_order_traverse(lambda x: print(x.value))
    print(tree1)
    print(tree2)
