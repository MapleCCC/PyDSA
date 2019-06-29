from .abstract_tree import Node, Tree


class M_aryNode(Node):
    def __init__(self, data, branch=2):
        super().__init__(data)

        if not isinstance(branch, int) or branch <= 0:
            raise ValueError("Invalid branch number")
        self.children = [None] * branch


class M_aryTree(Tree):
    def __init__(self, m):
        super().__init__()

        if not isinstance(m, int) or m <= 0:
            raise ValueError("Valid branch number is a positive integer.")
        self.branch = m


class BinaryNode(M_aryNode):
    def __init__(self, data):
        super().__init__(data, branch=2)

    @property
    def left(self):
        return self.children[0]

    @left.setter
    def left(self, node):
        if not isinstance(node, (BinaryNode, type(None))):
            raise TypeError("{} is not BinaryNode type".format(type(node)))
        self.children[0] = node

    @property
    def right(self):
        return self.children[1]

    @right.setter
    def right(self, node):
        if not isinstance(node, (BinaryNode, type(None))):
            raise TypeError("{} is not BinaryNode type".format(type(node)))
        self.children[1] = node


class BinaryTree(M_aryTree):
    def __init__(self):
        super().__init__(m=2)
