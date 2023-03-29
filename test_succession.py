import unittest
from royals import *


class TestAbsolute(unittest.TestCase):
    '''Test lines of succession in absolute primogeniture FamilyTree.'''

    def setUp(self):
        self.tree = FamilyTree(True)
        self.sarah = Person('Sarah', 'Gibeau', 'F')
        self.mr = Person('Mr', 'Gibeau', 'M')
        self.gibeaus = CoupleNode(self.sarah, self.mr, self.tree)
        self.zeus = self.gibeaus.have_son('Zeus')
        self.aph = self.gibeaus.have_daughter('Aphrodite')
        self.di = self.gibeaus.have_son('Dionysus')
        self.zeuses = self.zeus.marry(Person('Hera', 'Juno', 'F'))
        self.herc = self.zeuses.have_son('Hercules')
        self.aphes = self.aph.marry(Person('Apollo', 'A', 'M'))
        self.art = self.aphes.have_daughter('Artemis')
        self.ath = self.aphes.have_daughter('Athena')
        self.tree.root = self.gibeaus

    def tearDown(self):
        pass

    def testCrown(self):
        '''Test the crown method.'''

        self.tree.crown(self.zeus.royal)
        self.assertEqual(self.zeuses.ancestor_of_ruler, True)
        self.assertEqual(self.gibeaus.ancestor_of_ruler, True)
        self.assertEqual(self.herc.ancestor_of_ruler, False)
        self.assertEqual(self.aphes.ancestor_of_ruler, False)
        self.assertEqual(self.art.ancestor_of_ruler, False)
        self.assertEqual(self.ath.ancestor_of_ruler, False)
        self.assertEqual(self.di.ancestor_of_ruler, False)

    def testNodeSuccession(self):
        '''Test line_of_succession as called from RoyalNode'''

        self.assertEqual(self.gibeaus.line_of_succession(), \
        [self.sarah, self.zeuses.royal, self.herc.royal, self.aphes.royal, \
        self.art.royal, self.ath.royal, self.di.royal])

    def testRootRuler(self):
        '''Test with the original couple as ruler.'''

        self.tree.crown(self.gibeaus.royal)
        self.assertEqual(self.tree.line_of_succession(), [self.gibeaus.royal, \
        self.zeuses.royal, self.herc.royal, self.aphes.royal, \
        self.art.royal, self.ath.royal, self.di.royal])

    def testLeafRuler(self):
        '''Test with leaf as ruler.'''

        self.tree.crown(self.art.royal)
        self.assertEqual(self.tree.line_of_succession(), [self.art.royal, \
        self.aph.royal, self.ath.royal, self.gibeaus.royal, \
        self.zeus.royal, self.herc.royal, self.di.royal])

    def testInternalRuler(self):
        '''Test with internal node as ruler.'''

        self.tree.crown(self.zeuses.royal)
        self.assertEqual(self.tree.line_of_succession(), [self.zeuses.royal, \
        self.herc.royal, self.gibeaus.royal, self.aphes.royal, \
        self.art.royal, self.ath.royal, self.di.royal])

    def testDeadRoyal(self):
        '''Test with one royal dead and removed from line.'''

        self.tree.crown(self.gibeaus.royal)
        self.tree.kill(self.zeuses.royal)
        self.assertEqual(self.tree.line_of_succession(), [self.sarah, \
        self.herc.royal, self.aphes.royal, self.art.royal, \
        self.ath.royal, self.di.royal])


class TestGenderMale(unittest.TestCase):
    '''Test FamiltyTree with male gender preference.'''

    def setUp(self):
        self.tree = FamilyTree(False)
        self.sarah = Person('Sarah', 'Gibeau', 'F')
        self.mr = Person('Mr', 'Gibeau', 'M')
        self.gibeaus = CoupleNode(self.mr, self.sarah, self.tree)
        self.zeus = self.gibeaus.have_son('Zeus')
        self.aph = self.gibeaus.have_daughter('Aphrodite')
        self.di = self.gibeaus.have_son('Dionysus')
        self.zeuses = self.zeus.marry(Person('Hera', 'Juno', 'F'))
        self.herc = self.zeuses.have_son('Hercules')
        self.aphes = self.aph.marry(Person('Apollo', 'A', 'M'))
        self.art = self.aphes.have_daughter('Artemis')
        self.ath = self.aphes.have_daughter('Athena')
        self.tree.root = self.gibeaus

    def tearDown(self):
        pass

    def testRootRuler(self):
        '''Test with root as ruler and male preference.'''

        self.tree.crown(self.gibeaus.royal)
        self.assertEqual(self.tree.line_of_succession(),
        [self.gibeaus.royal, self.zeuses.royal, self.herc.royal, \
        self.di.royal, self.aphes.royal, self.art.royal, self.ath.royal])

    def testInternalRuler(self):
        '''Test with internal node as ruler and male preference.'''

        self.tree.crown(self.zeuses.royal)
        self.assertEqual(self.tree.line_of_succession(), \
        [self.zeuses.royal, self.herc.royal, self.gibeaus.royal, \
        self.di.royal, self.aphes.royal, self.art.royal, self.ath.royal])

    def testLeafRuler(self):
        '''Test with leaf as ruler and male preference.'''

        self.tree.crown(self.zeuses.royal)
        self.assertEqual(self.tree.line_of_succession(), \
        [self.zeuses.royal, self.herc.royal, self.gibeaus.royal, \
        self.di.royal, self.aphes.royal, self.art.royal, self.ath.royal])


class TestGenderFemale(unittest.TestCase):
    '''Test FamilyTree with female gender preference.'''

    def setUp(self):
        self.tree = FamilyTree(False)
        self.sarah = Person('Sarah', 'Gibeau', 'F')
        self.mr = Person('Mr', 'gibeau', 'M')
        self.gibeaus = CoupleNode(self.sarah, self.mr, self.tree)
        self.zeus = self.gibeaus.have_son('Zeus')
        self.aph = self.gibeaus.have_daughter('Aphrodite')
        self.di = self.gibeaus.have_son('Dionysus')
        self.zeuses = self.zeus.marry(Person('Hera', 'Juno', 'F'))
        self.herc = self.zeuses.have_son('Hercules')
        self.aphes = self.aph.marry(Person('Apollo', 'A', 'M'))
        self.art = self.aphes.have_daughter('Artemis')
        self.ath = self.aphes.have_daughter('Athena')
        self.tree.root = self.gibeaus

    def tearDown(self):
        pass

    def testRootRuler(self):
        '''Test with root as ruler and female preference.'''

        self.tree.crown(self.gibeaus.royal)
        self.assertEqual(self.tree.line_of_succession(), \
        [self.gibeaus.royal, self.aphes.royal, self.art.royal, \
        self.ath.royal, self.zeuses.royal, self.herc.royal, \
        self.di.royal])

    def testInternalRuler(self):
        '''Test with internal node as ruler and female preference.'''

        self.tree.crown(self.zeuses.royal)
        self.assertEqual(self.tree.line_of_succession(), [self.zeuses.royal, \
        self.herc.royal, self.gibeaus.royal, self.aphes.royal, \
        self.art.royal, self.ath.royal, self.di.royal])

    def testLeafRuler(self):
        '''Test with leaf as ruler and female preference.'''

        self.tree.crown(self.di.royal)
        self.assertEqual(self.tree.line_of_succession(), [self.di.royal, \
        self.gibeaus.royal, self.aphes.royal, self.art.royal, \
        self.ath.royal, self.zeus.royal, self.herc.royal])


if __name__ == '__main__':
    # go!
    suite1 = unittest.TestLoader().loadTestsFromTestCase(TestAbsolute)
    suite2 = unittest.TestLoader().loadTestsFromTestCase(TestGenderMale)
    suite3 = unittest.TestLoader().loadTestsFromTestCase(TestGenderFemale)
    alltests = unittest.TestSuite([suite1, suite2, suite3])
    runner = unittest.TextTestRunner()
    runner.run(alltests)
