import random
import main
from main import *
import math

UCB_CONST = 0.5

class Node():
    def __init__(self, state, parent_node):
        self.state = state
        self.parent = parent_node
        self.children = {}
        self.visits = 0
        self.value = float{"nan"}
        self.wins = 0

    def addMove(self, move):
        """ 
        Adds a new node for the child resulting from given move if it doesn't already exist.
        Returns true if node was added, false otherwise.
        """
        if move not in self.children:
            state = self.state.nextState(move)
            self.children[move] = Node(state, self)
            return True
        return False
    
    def getValue(self):
        """
        Gets value estimate for current node.
        """
        return self.value

    def updateValue(self, outcome):
        """
        Updates value estimate for node's state.
        +1 for player 1 win. -1 for player 2 win. 0 for draw.
        """
        turn = self.state.getTurn()

        if outcome != turn:
            self.wins += 1
        self.visits += 1

        self.value = self.wins/self.visits

    def UCBValue(self):
        """
        Gives UCB value used by parent to select a child node.
        """
        return self.value + (UCB_CONST * math.sqrt(math.log((self.parent.visits))/self.visits))

def MCTS(root, rollouts):
    pass

def main():
    print("Working on it")
    
if __name__ == "__main__":
    main()