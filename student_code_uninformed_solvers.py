
from solver import *
from collections import deque

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def populateChildList(self, movables, child_list):
        for move in movables:
                #append children for each move and then revert, not marking for visiting
                self.gm.makeMove(move)
                #deeper game state
                new_state = GameState(self.gm.getGameState(), self.currentState.depth + 1, move)
                #generate parent-child relationships
                new_state.parent = self.currentState
                new_state.parent.children.append(new_state)
                self.gm.reverseMove(move)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here


        # def __init__(self, gameMaster, victoryCondition):
        # self.gm = gameMaster
        # self.visited = dict()
        # self.currentState = GameState(self.gm.getGameState(), 0, None)
        #initial depth of zero, no moves
        # self.visited[self.currentState] = True
        # self.victoryCondition = victoryCondition
        """
        GameState Attributes:
        children (list of GameState): GameState nodes expandable from the the current GameState node
        nextChildToVisit (int): index of the next GameState node in 'children' list of expand
        parent (GameState): reference to the GameState object from which the current one is generated
        requiredMovable (Statement): the MOVABLE Statement which enables the transition from the
                                    parent GameState to this GameState
        state (object): a hashable object that denotes a specific game state, such as a Tuple of Tuples
        depth (int): the depth of the current GameState -- the number of moves that had been made to reach the
        current game state
        """ 
        if self.currentState.state == self.victoryCondition:
            return True
        child_list = self.currentState.children
        if not child_list:
            movables = self.gm.getMovables()
            if not movables: #if game state somehow lacks moves, something's wrong with the facts and we must debug
                lx = self.getGameState()
                print(lx)
                for i in self.kb.facts:
                    print(i)
            self.populateChildList(movables, child_list)

        #now we go through the children of currentState
        i = self.currentState.nextChildToVisit
        j = len(child_list)

        while i < j:
            if child_list[i] in self.visited:
                i += 1
            else:
                # found an unvisited child at i so mark as visited and check for victory condition
                child = child_list[i]
                self.visited[child] = True
                self.gm.makeMove(child.requiredMovable)
                self.currentState = child
                return child.state == self.victoryCondition
        #after looking through entire child list and finding no victory conditions, 
        #reset state to parent
        self.gm.reverseMove(self.currentState.requiredMovable)
        self.currentState = self.currentState.parent

class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.queue = deque()

    def populateChildList(self, movables, child_list):
        for move in movables:
                self.gm.makeMove(move)
                new_state = GameState(self.gm.getGameState(), self.currentState.depth + 1, move)
                if new_state not in self.visited:
                    #mark for future visitation
                    self.visited[new_state] = False
                    #generate parent-child relationships
                    new_state.parent = self.currentState
                    child_list.append(new_state)
                self.gm.reverseMove(move)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        if self.currentState.state == self.victoryCondition:
            return True
        next_moves = []
        self.visited[self.currentState] = True
        child_list = self.currentState.children
        movables = self.gm.getMovables()
        if not movables: #if game state somehow lacks moves, something's wrong with the facts and we must debug
            lx = self.getGameState()
            print(lx)
            for i in self.kb.facts:
                print(i)
        if not child_list:
            #if child list is empty, we populate it
            self.populateChildList(movables, child_list)
        #add all unvisited children to queue for BFS
        for child in child_list:
            if self.visited[child] == False:
                #add to head of queue
                self.queue.appendleft(child)
        #return tail of queue
        next_state = self.queue.pop()
        if next_state.depth == self.currentState.depth:
            prior_state = next_state
        else: 
            #next_state can only be deeper
            next_moves.append(next_state.requiredMovable)
            prior_state = next_state.parent
        while self.currentState != prior_state:
            #move up in ancestry until we converge on prior_state, adding to next_moves as we go
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
            next_moves.append(prior_state.requiredMovable)
            prior_state = prior_state.parent
        while next_moves:
            self.gm.makeMove(next_moves.pop())
        #address next_state last after updating moves
        self.currentState = next_state
        return self.currentState.state == self.victoryCondition