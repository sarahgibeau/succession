from tree import *


class Person:

    def __init__(self, first, last, gender, alive=True):
        '''(Person, str, str, str, bool) -> NoneType
        Create a new Person object.
        '''

        self.first = first
        self.last = last
        self.gender = gender
        self.alive = alive

    def __str__(self):
        '''(Person) -> str
        Return a str representation of person.
        '''

        return self.first + ' ' + self.last

    def __repr__(self):
        '''(Person) -> str
        Return a str representation of person.
        '''

        return str(self)


class RoyalNode(Node):

    def __init__(self, royal, tree):
        '''(RoyalNode, Person, Tree) -> NoneType
        Create a new RoyalNode object.
        '''

        Node.__init__(self, tree)
        self.royal = royal
        self.ancestor_of_ruler = False

    def __str__(self):
        '''(RoyalNode) -> str
        Return a str representation of node.
        '''

        return str(self.royal) + ' (' + self.royal.gender + ')'

    def __repr__(self):
        '''(RoyalNode) -> str
        Return a str representation of node.
        '''

        return str(self)

    def marry(self, consort):
        '''(RoyalNode, Person) -> CoupleNode
        Create and return CoupleNode of royal and consort.
        '''

        if not self.royal.alive:
            raise DeadRoyalError
        new = CoupleNode(self.royal, consort, self.tree)
        if self.parent:
            #Set parent of new CoupleNode to be the same as RoyalNode
            new.parent = self.parent
            #Loop through parents' children and update correct node
            for i in range(len(self.parent.children)):
                if self.parent.children[i] is self:
                    self.parent.children.pop(i)
                    self.parent.children.insert(i, new)
        return new

    def search(self, royal, children=[]):
        '''(RoyalNode, Person, list) -> Person or NoneType
        Find royal in list and return corresponding node.
        '''

        l = self.search_helper()
        for i in l:
            if i.royal is royal:
                return i

    def search_helper(self):
        '''(RoyalNode) -> list
        Add Node and all descendant Nodes to list and return list.
        '''

        #Start list with original node
        l = [self]
        if self.children:
            #Call search_helper again on each child node, passing
            #each descendant node back up and extending the list
            for i in self.children:
                l.extend(i.search_helper())
        return l

    def line_of_succession(self):
        '''(RoyalNode) -> list
        Generate line of succession in list form from node.
        '''

        l = []
        #Check that royal is alive before adding it to list
        if self.royal.alive:
            l = [self.royal]
        if (self.children):
            #For absolute primogeniture, children are added
            #in order of age
            if (self.tree.absolute == True):
                for i in self.children:
                    if not i.ancestor_of_ruler:
                        l.extend(i.line_of_succession())
            #In the case of gender preference primogeniture
            else:
                #Gender of royal in original couple is determined
                gender = self.tree.root.royal.gender
                #n will be a new list to store royals of
                #non-preferred gender
                n = []
                for i in self.children:
                    if not i.ancestor_of_ruler:
                        #If royal is preferred gender, add to list
                        if i.royal.gender == gender:
                            l.extend(i.line_of_succession())
                        #Otherwise, append to n
                        else:
                            n.append(i)
                #Add royals in n to end of list
                for i in n:
                    l.extend(i.line_of_succession())
        #If node represents ruler or ancestor of ruler and has a parent,
        #recursively generate lines of succession for ancestor nodes
        if self.ancestor_of_ruler and self.parent:
            l.extend(self.parent.line_of_succession())

        return l

    def change_ancestor(self, value):
        '''(RoyalNode, bool) -> NoneType
        Change ancestor_of_ruler attribute to value (True or False)
        '''

        self.ancestor_of_ruler = value

    def reset_descendants(self):
        '''(RoyalNode) -> NoneType
        Resets current node and all its descendant's ancestor_of_ruler
        attributes  to False.
        '''

        self.change_ancestor(False)
        for i in self.children:
            i.reset_descendants()

    def set_ancestors(self):
        '''(RoyalNode) -> NoneType
        Change ancestor_of_ruler attribute of current node and its
        ancestor nodes to True.
        '''

        self.change_ancestor(True)
        if self.parent:
            self.parent.set_ancestors()


class NoSuchRoyalError(Exception):
    '''Raises an exception when no such royal exists.'''
    pass


class DeadRoyalError(Exception):
    '''Raises an exception when royal is dead.'''
    pass


class CoupleNode(RoyalNode):

    def __init__(self, royal, consort, tree):
        '''(CoupleNode, Person, Person, Tree) -> NoneType
        Create a new CoupleNode object.
        '''

        RoyalNode.__init__(self, royal, tree)
        self.consort = consort

    def __str__(self):
        '''(CoupleNode) -> str
        Return a str representation of node.
        '''

        return str(self.royal) + ' (' + self.royal.gender + \
               ') and ' + str(self.consort)

    def __repr__(self):
        '''(CoupleNode) -> str
        Return a str representation of node.
        '''

        return str(self)

    def have_son(self, name):
        '''(CoupleNode, str) - RoyalNode
        Create and return new male RoyalNode object with CoupleNode
        as parent.
        '''

        if not self.royal.alive:
            raise DeadRoyalError
        node = RoyalNode(Person(name, self.royal.last, 'M'), self.tree)
        node.parent = self
        self.children.append(node)
        return node

    def have_daughter(self, name):
        '''(CoupleNode, str) - RoyalNode
        Create and return new female RoyalNode object with CoupleNode
        as parent.
        '''

        if not self.royal.alive:
            raise DeadRoyalError
        node = RoyalNode(Person(name, self.royal.last, 'F'), self.tree)
        node.parent = self
        self.children.append(node)
        return node


class FamilyTree(Tree):

    def __init__(self, absolute):
        '''(Tree, bool) -> NoneType
        Create a new FamilyTree object.
        '''

        Tree.__init__(self)
        self.absolute = absolute
        self.ruler = None

    def start(self, couple):
        '''(Tree, CoupleNode) -> NoneType
        Set tree's root and ruler attributes to CoupleNode.
        '''

        self.root = couple
        self.ruler = couple

    def search(self, person):
        '''(Tree, Person) -> Node or NoneType
        Search for Person object in Tree and return its
        corresponding Node. If person is not found, return None.
        '''

        if self.root:
            return self.root.search(person)

    def crown(self, person):
        '''(Tree, Person) -> NoneType
        Set Tree's ruler attribute to Node representing Person and
        set all Nodes' ancestor_of_ruler attribute accordingly.
        '''

        ruler = self.search(person)
        if not ruler:
            raise NoSuchRoyalError
        if not ruler.royal.alive:
            raise DeadRoyalError
        else:
            #Reset all ancestor_of_ruler attributes in tree to False
            self.root.reset_descendants()
            self.ruler = ruler
            #Set ancestor_of_ruler attributes for new ruler's
            #ancestors to True
            self.ruler.set_ancestors()

    def kill(self, royal):
        '''(Person) -> NoneType
        Change royal's alive attribute to False.
        '''

        deadperson = self.search(royal)
        if not deadperson:
            raise NoSuchRoyalError
        deadperson.royal.alive = False

    def line_of_succession(self):
        '''(Tree) -> list
        Generate line of succession for tree based on current ruler.
        '''

        return self.ruler.line_of_succession()
