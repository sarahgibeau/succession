import unittest
from royals import *


class TestPerson(unittest.TestCase):

    def setUp(self):
        self.person = Person('Sarah', 'Gibeau', 'F')

    def tearDown(self):
        pass

    def testAttributes(self):
        '''Test that person attributes have been correctly assigned.'''

        self.assertTrue(self.person.first == 'Sarah')
        self.assertTrue(self.person.last == 'Gibeau')
        self.assertTrue(self.person.gender == 'F')
        self.assertTrue(self.person.alive)

    def testStr(self):
        '''Test the str method.'''

        self.assertEqual(str(self.person), 'Sarah Gibeau')

    def testRepr(self):
        '''Test the repr method.'''

        self.assertEqual(repr(self.person), 'Sarah Gibeau')


class TestRoyalNode(unittest.TestCase):

    def setUp(self):
        self.tree = FamilyTree(True)
        self.sarah = RoyalNode(Person('Sarah', 'Gibeau', 'F'), self.tree)
        self.mr = Person('Mr', 'Gibeau', 'M')

    def tearDown(self):
        pass

    def testAttributes(self):
        '''Test that attributes have been correctly assigned.'''

        self.assertEqual(self.sarah.royal.first, 'Sarah')
        self.assertEqual(self.sarah.royal.last, 'Gibeau')
        self.assertEqual(self.sarah.royal.gender, 'F')
        self.assertTrue(self.sarah.royal.alive)
        self.assertEqual(self.sarah.tree, self.tree)
        self.assertTrue(not self.sarah.children)
        self.assertEqual(self.sarah.parent, None)

    def testStr(self):
        '''Test the str method.'''

        self.assertEqual(str(self.sarah), 'Sarah Gibeau (F)')

    def testRepr(self):
        '''Test the repr method.'''

        self.assertEqual(repr(self.sarah), 'Sarah Gibeau (F)')

    def testMarry(self):
        '''Test the marry method.'''

        self.couple = self.sarah.marry(self.mr)
        self.assertEqual(self.couple.royal, self.sarah.royal)
        self.assertEqual(self.couple.consort, self.mr)
        self.assertEqual(self.couple.tree, self.tree)
        self.assertEqual(self.couple.parent, None)
        self.assertTrue(not self.couple.children)


class TestCoupleNode(unittest.TestCase):
    '''Test the CoupleNode class.'''

    def setUp(self):
        self.tree = FamilyTree(True)
        self.sarah = Person('Sarah', 'Gibeau', 'F')
        self.mr = Person('Mr', 'Gibeau', 'M')
        self.couple = CoupleNode(self.sarah, self.mr, self.tree)

    def tearDown(self):
        pass

    def testAttributes(self):
        '''Test that attributes have been correctly assigned.'''

        self.assertEqual(self.couple.royal, self.sarah)
        self.assertEqual(self.couple.consort, self.mr)
        self.assertEqual(self.couple.tree, self.tree)
        self.assertEqual(self.couple.parent, None)
        self.assertTrue(not self.couple.children)

    def testStr(self):
        '''Test the str method.'''

        self.assertEqual(str(self.couple), 'Sarah Gibeau (F) and Mr Gibeau')

    def testRepr(self):
        '''Test the repr method.'''

        self.assertEqual(str(self.couple), 'Sarah Gibeau (F) and Mr Gibeau')

    def testHaveSon(self):
        '''Test the have_son method.'''

        self.zeus = self.couple.have_son('Zeus')
        self.assertEqual(self.zeus.royal.first, 'Zeus')
        self.assertEqual(self.zeus.royal.last, 'Gibeau')
        self.assertEqual(self.zeus.royal.gender, 'M')
        self.assertEqual(self.zeus.parent, self.couple)
        self.assertEqual(self.zeus.tree, self.tree)
        self.assertTrue(self.zeus.royal.alive)
        self.assertTrue(not self.zeus.children)
        self.assertEqual(self.couple.children, [self.zeus])

    def testHaveDaughter(self):
        '''Test the have_daughter method.'''

        self.aph = self.couple.have_daughter('Aphrodite')
        self.assertEqual(self.aph.royal.first, 'Aphrodite')
        self.assertEqual(self.aph.royal.last, 'Gibeau')
        self.assertEqual(self.aph.royal.gender, 'F')
        self.assertEqual(self.aph.parent, self.couple)
        self.assertEqual(self.aph.tree, self.tree)
        self.assertTrue(self.aph.royal.alive)
        self.assertTrue(not self.aph.children)
        self.assertEqual(self.couple.children, [self.aph])

    def testChildrenOrder(self):
        '''Test that children are listed in proper order.'''

        self.zeus = self.couple.have_son('Zeus')
        self.aph = self.couple.have_daughter('Aphrodite')
        self.assertEqual(self.couple.children, [self.zeus, \
                                                self.aph])

    def testDeadRoyal(self):
        '''Test methods in the case of a dead royal.'''

        self.sarah.alive = False
        self.assertRaises(DeadRoyalError, self.couple.have_son, 'Zeus')
        self.assertRaises(DeadRoyalError, self.couple.have_daughter, \
                          'Aphrodite')


class TestFamilyTree(unittest.TestCase):
    '''Test the FamilyTree class.'''

    def setUp(self):
        self.tree = FamilyTree(True)
        self.sarah = Person('Sarah', 'Gibeau', 'F')
        self.mr = Person('Mr', 'Gibeau', 'M')
        self.couple = CoupleNode(self.sarah, self.mr, self.tree)
        self.tree.root = self.couple
        self.zeus = self.couple.have_son('Zeus')
        self.aph = self.couple.have_daughter('Aphrodite')
        self.newcouple = self.zeus.marry(Person('Hera', 'Juno', 'F'))
        self.herc = self.newcouple.have_son('Hercules')

    def tearDown(self):
        pass

    def testAttributes(self):
        '''Test that attributes are correctly assigned.'''

        self.assertEqual(self.tree.ruler, None)
        # self.assertEqual(self.tree.root, None)
        self.assertEqual(self.tree.absolute, True)

    def testStart(self):
        '''Test the start method.'''

        self.tree.start(self.couple)
        self.assertEqual(self.tree.root, self.couple)
        self.assertEqual(self.tree.ruler, self.couple)

    def testNodeSearch(self):
        '''Test the node search method.'''

        #Call method from CoupleNode
        self.assertEqual(self.couple.search(self.sarah), self.couple)
        self.assertEqual(self.couple.search(self.aph.royal), self.aph)
        self.assertEqual(self.couple.search(self.zeus.royal), self.newcouple)
        self.assertEqual(self.couple.search(self.newcouple.consort), None)
        #self.assertEqual(self.couple.search(Person('Venus', 'Flytrap', \
                                                   #'F'), None))
        #Call method from RoyalNode
        self.assertEqual(self.aph.search(self.aph.royal), self.aph)
        #Checking that only child nodes are searched
        self.assertEqual(self.aph.search(self.sarah), None)
        self.assertEqual(self.aph.search(self.zeus.royal), None)

    def testTreeSearch(self):
        '''Test the tree search method.'''

        self.tree.root = self.couple
        self.assertEqual(self.tree.search(self.sarah), self.couple)
        self.assertEqual(self.tree.search(self.aph.royal), self.aph)
        self.assertEqual(self.tree.search(self.zeus.royal), self.newcouple)
        self.assertEqual(self.tree.search(self.newcouple.consort), None)
        #self.assertEqual(self.tree.search(Person('Venus', 'Flytrap', \
                                                   #'F'), None))

    def testCrown(self):
        '''Test the crown method.'''

        self.tree.crown(self.sarah)
        #self.assertEqual(self.tree.root, self.couple)
        self.assertEqual(self.tree.ruler, self.couple)
        #self.assertRaises(NoSuchRoyalError, self.tree.crown, \
                          #Person('Venus', 'Flytrap', 'F'))
        self.zeus.royal.alive = False
        self.assertRaises(DeadRoyalError, self.tree.crown, self.zeus.royal)

    def testKill(self):
        '''Test the kill method.'''

        self.tree.root = self.couple
        #Test kill with royal in CoupleNode
        self.tree.kill(self.newcouple.royal)
        self.assertFalse(self.newcouple.royal.alive)
        #Check that consort's status is unchanged
        self.assertTrue(self.newcouple.consort.alive)
        #Test with single royal
        self.tree.kill(self.aph.royal)
        self.assertFalse(self.aph.royal.alive)
        #Test with royal who is already dead
        self.tree.kill(self.zeus.royal)
        self.assertFalse(self.zeus.royal.alive)
        #Check that proper exceptions are raised
        self.assertRaises(NoSuchRoyalError, self.tree.kill, \
                          Person('Venus', 'Flytrap', 'F'))


if __name__ == '__main__':
    # go!
    suite1 = unittest.TestLoader().loadTestsFromTestCase(TestPerson)
    suite2 = unittest.TestLoader().loadTestsFromTestCase(TestRoyalNode)
    suite3 = unittest.TestLoader().loadTestsFromTestCase(TestCoupleNode)
    suite4 = unittest.TestLoader().loadTestsFromTestCase(TestFamilyTree)
    alltests = unittest.TestSuite([suite1, suite2, suite3, suite4])
    runner = unittest.TextTestRunner()
    runner.run(alltests)
