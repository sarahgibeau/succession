class Node:
    '''An arbitrary-tree node class with no data.'''

    def __init__(self, tree, parent=None):
        '''(Node, Tree, Node or NoneType) -> NoneType
        Initialize a new Node of tree tree with parent parent.'''

        self.parent = parent
        self.tree = tree
        self.children = []

    def traverse(self, f):
        '''(Node, function) -> NoneType
        Call f with self as parameter, then on each of
        self's children.'''

        f(self)
        for i in self.children:
            i.traverse(f)

    def depth(self):
        '''(Node) -> int
        Return the depth of self in the tree. The root of a
        tree has a depth of 1.'''

        if not self.parent:
            return 1
        return self.parent.depth() + 1


class IntNode(Node):
    '''A class inheriting from Node that can contain integers.'''

    def __init__(self, value, tree, parent=None):
        '''(IntNode, int, Tree, IntNode or NoneType) -> NoneType
        Initialize a new IntNode of tree tree with intvalue value
        and parent parent.'''

        Node.__init__(self, tree, parent)
        self.intvalue = value

    def __str__(self):
        '''(IntNode) -> str
        Return the string representation of this object.'''

        return str(self.intvalue)

    def add_child(self, v):
        '''(IntNode, int) -> IntNode
        Create a new IntNode with value v and add
        it to the end of self's children.
        Return the newly created IntNode.'''

        retnode = IntNode(v, self.tree, self)
        self.children.append(retnode)
        return retnode


class Tree:
    '''A class representing an arbitrary branching factor tree.'''

    def __init__(self, root=None):
        '''(Tree, Node or NoneType) -> NoneType
        Initialize a new tree with root root (optional).'''

        self.root = root

    def traverse(self, f):
        '''(Tree, function) -> NoneType
        Apply f to every node in the tree, starting with root.'''

        if self.root:
            self.root.traverse(f)

    def print_tree(self):
        '''(Tree) -> NoneType
        Print a tabbed representation of the tree to the screen.'''

        self.traverse(print_offset)


def print_offset(n):
    '''(Node) -> NoneType
    Print Node n with an offset of depth * 4 spaces'''

    print('    ' * n.depth() + str(n))


if __name__ == '__main__':
    #the tiniest of tests
    tree = Tree()
    five = IntNode(5, tree)
    tree.root = five
    nine = five.add_child(9)
    two = five.add_child(2)
    eight = nine.add_child(8)
    three = nine.add_child(3)
    tree.print_tree()
