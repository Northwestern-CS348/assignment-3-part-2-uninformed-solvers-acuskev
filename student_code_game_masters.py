from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        p1 = []
        p2 = []
        p3 = []
        bindings1 = self.kb.kb_ask(parse_input("fact: (on ?disk peg1)"))
        if bindings1:
            for binding in bindings1:
                disknum = binding.bindings[0].constant.element[-1]
                p1.append(int(disknum))
            p1.sort()

        bindings2 = self.kb.kb_ask(parse_input("fact: (on ?disk peg2)"))
        if bindings2:
            for binding in bindings2:
                disknum = binding.bindings[0].constant.element[-1]
                p2.append(int(disknum))
            p2.sort()
        bindings3 = self.kb.kb_ask(parse_input("fact: (on ?disk peg3)"))
        if bindings3:
            for binding in bindings3:
                disknum = binding.bindings[0].constant.element[-1]
                p3.append(int(disknum))
            p3.sort()

        return (tuple(p1), tuple(p2), tuple(p3))


    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        terms = movable_statement.terms
        disk = terms[0].term.element
        pegx = terms[1].term.element
        pegy = terms[2].term.element
        r_oldytop = False
        r_emptypegy = False
        r_a_newxtop = False
        a_newytop = False
        a_emptyx = False
        #check for empty pegy
        # lx = self.getGameState()
        # print(lx)
        # if lx == ((2,), (3,), (1,)):
        #     for i in self.kb.facts:
        #         print(i.statement)
        #     x = self.kb.kb_ask(parse_input('fact: (movable disk2 peg2 peg1)'))
        #     if x:
        #         print('lll')
        if not self.kb.kb_ask(parse_input('fact: (empty ' + pegy + ')')):
            #not empty
            old_pegy_bindings = self.kb.kb_ask(parse_input('fact: (top ?disk ' + pegy + ')'))
            # if not old_pegy_bindings:
            #     print('destination peg ' + pegy + ' not empty, but ???')
            #     lx = self.getGameState()
            #     #print(lx)
            #     for i in self.kb.facts:
            #         pass
            #         #print(i)
            old_pegy_top = old_pegy_bindings[0].bindings_dict['?disk']
            # lx = self.getGameState()
            # if lx == ((2, 3), (1,), ()):
            #     print(disk)
            #     print(pegx)
            #     print(old_pegy_top)
            #     print(pegy)
            #     for i in self.kb.facts:
            #         print(i)
            r_oldytop = True
            a_newytop = True
            #self.kb.kb_assert(parse_input('fact: (above ' + disk + ' ' + old_pegy_top + ')'))
        else:
            #pegy was empty
            r_emptypegy = True
        #check for presence of disk below top disk
        above_bindings = self.kb.kb_ask(parse_input('fact: (above ' + disk + ' ?disk)'))
        if above_bindings:
            #top disk was above another
            new_pegx_top = above_bindings[0].bindings_dict['?disk']
            r_a_newxtop = True
        else:
            #top disk was the only disk on pegx, which should now be empty
            a_emptyx = True

        self.kb.kb_retract(parse_input('fact: (on ' + disk + ' ' + pegx + ')'))
        self.kb.kb_retract(parse_input('fact: (top ' + disk + ' ' + pegx + ')'))
        if r_oldytop:
            self.kb.kb_retract(parse_input('fact: (top ' + old_pegy_top + ' ' + pegy + ')'))
        if r_emptypegy:
            self.kb.kb_retract(parse_input('fact: (empty ' + pegy + ')'))
        if r_a_newxtop:
            self.kb.kb_retract(parse_input('fact: (above ' + disk + ' ' + new_pegx_top + ')'))
            self.kb.kb_assert(parse_input('fact: (top ' + new_pegx_top + ' ' + pegx + ')'))
        if a_newytop:
            self.kb.kb_assert(parse_input('fact: (above ' + disk + ' ' + old_pegy_top + ')'))
        if a_emptyx:
            self.kb.kb_assert(parse_input('fact: (empty ' + pegx + ')'))
        self.kb.kb_assert(parse_input('fact: (top ' + disk + ' ' + pegy + ')'))
        self.kb.kb_assert(parse_input('fact: (on ' + disk + ' ' + pegy + ')'))

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        row1 = [29, 29, 29]
        bindings1 = self.kb.kb_ask(parse_input("fact: (tile ?tile ?col pos1)"))
        if bindings1:
            for binding in bindings1:
                if binding.bindings[0].constant.element == 'empty':
                    row1[int(binding.bindings[1].constant.element[3]) - 1] = -1
                else:
                    row1[int(binding.bindings[1].constant.element[3]) - 1] = int(binding.bindings[0].constant.element[4])

        row2 = [29, 29, 29]
        bindings2 = self.kb.kb_ask(parse_input("fact: (tile ?tile ?col pos2)"))
        if bindings2:
            for binding in bindings2:
                if binding.bindings[0].constant.element == 'empty':
                    row2[int(binding.bindings[1].constant.element[3]) - 1] = -1
                else:
                    row2[int(binding.bindings[1].constant.element[3]) - 1] = int(binding.bindings[0].constant.element[4])

        row3 = [29, 29, 29]
        bindings3 = self.kb.kb_ask(parse_input("fact: (tile ?tile ?col pos3)"))
        if bindings3:
            for binding in bindings3:
                if binding.bindings[0].constant.element == 'empty':
                    row3[int(binding.bindings[1].constant.element[3]) - 1] = -1
                else:
                    row3[int(binding.bindings[1].constant.element[3]) - 1] = int(binding.bindings[0].constant.element[4])

        row1 = tuple(row1)
        row2 = tuple(row2)
        row3 = tuple(row3)
        return (row1, row2, row3)

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        tile = movable_statement.terms[0].term.element
        col1 = movable_statement.terms[1].term.element
        row1 = movable_statement.terms[2].term.element
        col2 = movable_statement.terms[3].term.element
        row2 = movable_statement.terms[4].term.element
        oldfact = parse_input('fact: (tile ' + tile + ' ' + col1 + ' ' + row1 + ')')
        oldfact2 = parse_input('fact: (tile empty ' + col2 + ' ' + row2 + ')')
        newfact = parse_input('fact: (tile ' + tile + ' ' + col2 + ' ' + row2 + ')')
        newfact2 = parse_input('fact: (tile empty ' + col1 + ' ' + row1 + ')')
        self.kb.kb_retract(oldfact)
        self.kb.kb_retract(oldfact2)
        self.kb.kb_assert(newfact)
        self.kb.kb_assert(newfact2)

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
