import unittest
from tree import *


class TestEmptyTree(unittest.TestCase):

    def setUp(self):
        self.tree = Tree()

    def tearDown(self):
        pass

    def testIsEmpty(self):
        '''Test that tree has no root.'''

        self.assertTrue(not self.tree.root)

    def testTraverse(self):
        '''Test that traverse method does nothing and raises
        no errors.'''

        self.tree.traverse(adder)
        self.assertEqual(self.tree.root, None)


class TestSingleNode(unittest.TestCase):

    def setUp(self):
        self.tree = Tree()
        self.four = IntNode(4, self.tree)
        self.tree.root = self.four

    def tearDown(self):
        pass

    def testRoot(self):
        '''Test that root and children are correctly assigned.'''

        self.assertTrue(self.tree.root is self.four)
        self.assertTrue(not self.tree.root.children)

    def testDepth(self):
        '''Test depth method on single root node.'''

        self.assertEqual(self.tree.root.depth(), 1)

    def testNodeTraverse(self):
        '''Test that node traverse method is correctly applied.'''

        self.tree.root.traverse(adder)
        self.assertEqual(self.tree.root.intvalue, 5)

    def testTreeTraverse(self):
        '''Test that tree traverse method is correctly applied.'''

        self.tree.traverse(adder)
        self.assertEqual(self.tree.root.intvalue, 5)


class TestLargeTree(unittest.TestCase):

    def setUp(self):
        self.tree = Tree()
        self.four = IntNode(4, self.tree)
        self.tree.root = self.four
        self.one = self.four.add_child(1)
        self.two = self.four.add_child(2)
        self.nine = self.one.add_child(9)
        self.three = self.one.add_child(3)
        self.six = self.three.add_child(6)

    def tearDown(self):
        pass

    def testDepth(self):
        '''Test depth method.'''

        self.assertEqual(self.four.depth(), 1)
        self.assertEqual(self.one.depth(), 2)
        self.assertEqual(self.two.depth(), 2)
        self.assertEqual(self.nine.depth(), 3)
        self.assertEqual(self.three.depth(), 3)
        self.assertEqual(self.six.depth(), 4)

    def testNodeTraverse(self):
        '''Test node traverse method.'''

        self.three.traverse(adder)
        self.assertEqual(self.three.intvalue, 4)
        self.assertEqual(self.six.intvalue, 7)
        self.assertEqual(self.one.intvalue, 1)

    def testTreeTraverse(self):
        '''Test tree traverse method.'''

        self.tree.traverse(adder)
        self.assertEqual(self.four.intvalue, 5)
        self.assertEqual(self.one.intvalue, 2)
        self.assertEqual(self.two.intvalue, 3)
        self.assertEqual(self.nine.intvalue, 10)
        self.assertEqual(self.three.intvalue, 4)
        self.assertEqual(self.six.intvalue, 7)


def adder(intnode):
    '''(IntNode) -> None

    Increase node's value by one.
    '''

    intnode.intvalue += 1


if __name__ == '__main__':
    # go!
    suite1 = unittest.TestLoader().loadTestsFromTestCase(TestEmptyTree)
    suite2 = unittest.TestLoader().loadTestsFromTestCase(TestSingleNode)
    suite3 = unittest.TestLoader().loadTestsFromTestCase(TestLargeTree)
    alltests = unittest.TestSuite([suite1, suite2, suite3])
    runner = unittest.TextTestRunner()
    runner.run(alltests)
