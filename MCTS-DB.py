"""
MCTS starter code. This is the only file you'll need to modify, although
you can take a look at DBGame.py to get a sense of how the game is structured.

@author Bryce Wiedenbeck
@author Anna Rafferty (adapted from original)
@author Dave Musicant (adapted for Python 3 and other changes)
@author Miguel Alvarez and Nick Pandelakis (Adapted for Dots and Boxes with parallelization)
"""

# These imports are used by the starter code.
import random
import argparse
import DBGame

# You will want to use this import in your code
import math
import time
import concurrent.futures
import keras
import numpy

# Load Model
MODEL = keras.models.load_model("DB_Model")

# Set Win Threshold for model prediction.
THRESHOLD = 0.8

# Whether to display the UCB rankings at each turn.
DISPLAY_BOARDS = False 

# UCB_CONST value - you should experiment with different values
UCB_CONST = .5


class Node(object):
    """Node used in MCTS"""
    
    def __init__(self, state: DBGame.State, parent_node):
        """Constructor for a new node representing game state
        state. parent_node is the Node that is the parent of this
        one in the MCTS tree. """
        self.state = state
        self.parent = parent_node
        self.children = {} # maps moves (keys) to Nodes (values); if you use it differently, you must also change addMove
        self.visits = 0
        self.value = 0
        
    def addMove(self, move):
        """
        Adds a new node for the child resulting from move if one doesn't already exist.
        Returns true if a new node was added, false otherwise.
        """
        if move not in self.children:
            state = self.state.nextState(move)
            self.children[move] = Node(state, self)
            return True
        return False
    
    def getValue(self):
        """
        Gets the value estimate for the current node. Value estimates should correspond
        to the win percentage for the player at this node (accounting for draws as in 
        the project description).
        """
        return self.value

    def updateValue(self, outcome):
        
        player_wins = self.value * self.visits

        if self.parent is not None:
            # Root node does not need to be updated
            if outcome == 0:
                player_wins += 0.5
            elif outcome == 1:
                if self.parent.state.turn == 1:
                    player_wins += 1
            else:
                if self.parent.state.turn == -1:
                    player_wins += 1

        
        self.visits += 1

        self.value = (player_wins / self.visits)

    def UCBValue(self):
        """Value from the UCB formula used by parent to select a child. """

        return self.value + UCB_CONST * math.sqrt(math.log(self.parent.visits)/self.visits)


def MCTS(root: Node, rollouts: int) -> int:
    """Select a move by Monte Carlo tree search.
    Plays rollouts random games from the root node to a terminal state.
    In each rollout, play proceeds according to UCB while all children have
    been expanded. The first node with unexpanded children has a random child
    expanded. After expansion, play proceeds by selecting uniform random moves.
    Upon reaching a terminal state, values are propagated back along the
    expanded portion of the path. After all rollouts are completed, the move
    generating the highest value child of root is returned.
    Inputs:
        node: the node for which we want to find the optimal move
        rollouts: the number of root-leaf traversals to run
    Return:
        The legal move from node.state with the highest value estimate
    """
    
    for i in range(rollouts):    
        leaf = select(root)
        if not leaf.state.isTerminal():
            child = expand(leaf)
            outcome = simulate(child, root.state.turn)
        else:
            #Set child to be the state just before the terminal state is reached
            child = leaf.parent
            outcome = child.state.value()
        back_propogate(outcome, child, root)

    return max(root.children, key = lambda move: root.children[move].value)


def select(root: Node) -> Node:
    #traverse down tree, look for a move that generates a node that IS NOT CURRENTLY IN THE TREE!
    children = root.children.keys()
    moves = root.state.getMoves()

    if len(moves) != 0:
        if len(children) != len(moves):
            # We found a node to expand
            return root
        else:
            #Take the best option and keep searching
            best_option = max(root.children.values(), key = lambda child: child.UCBValue())
            return select(best_option)
    else:
        #reached a terminal node, do not attempt to use max() function
        return root


def expand(leaf: Node) -> Node:
    moves = leaf.state.getMoves()

    for move in moves:
        if leaf.addMove(move):
            #successful expansion
            return leaf.children[move]


def simulate(child: Node, turn) -> int:
    state = child.state

    if turn == 1:
        while not state.isTerminal():
            prob = MODEL.predict(numpy.array([state.toVector()]))[0][0]
            if prob >= THRESHOLD:
                return 1
            else:
                state = random_next_state(state)
        return state.value()
    else:
        while not state.isTerminal():
            state = random_next_state(state)

        return state.value()

# only bp back to the root we started at.
def back_propogate(outcome, child: Node, root: Node) -> None:

    while child != root:
        child.updateValue(outcome)
        child = child.parent

    root.updateValue(outcome)

def parse_args():
    """
    Parse command line arguments.
    """
    p = argparse.ArgumentParser()
    p.add_argument("--rollouts", type=int, default=0, help="Number of root-to-leaf "+\
                    "play-throughs that MCTS should run). Default=0 (random moves)")
    p.add_argument("--numGames", type=int, default=0, help="Number of games "+\
                    "to play). Default=1")
    p.add_argument("--second", action="store_true", help="Set this flag to "+\
                    "make your agent move second.")
    p.add_argument("--displayBoard", action="store_true", help="Set this flag to "+\
                    "make display the board at each MCTS turn with MCTS's rankings of moves.")
    p.add_argument("--rolloutsSecondMCTSAgent", type=int, default=0, help="If non-0, other player "+\
                    "will also be an MCTS agent and will use the number of rollouts set with this "+\
                    "argument. Default=0 (other player is random)")   
    p.add_argument("--ucbConst", type=float, default=.5, help="Value for the UCB exploration "+\
                    "constant. Default=.5")
    p.add_argument("--parallel", action="store_true", help="Set this flag to "+\
                    "run MCTS games in parallel.")
    args = p.parse_args()
    if args.displayBoard:
        global DISPLAY_BOARDS
        DISPLAY_BOARDS = True
    global UCB_CONST
    UCB_CONST = args.ucbConst
    return args


def random_move(node):
    """
    Choose a valid move uniformly at random.
    """
    move = random.choice(list(node.state.getMoves()))
    node.addMove(move)
    return move

def random_next_state(state: DBGame.State) -> DBGame.State:
    """
    Choose a valid move uniformly at random without adding it to the tree
    """
    move = random.choice(list(state.getMoves().keys()))
    next_state = state.nextState(move)
    return next_state

def run_multiple_games(num_games, args):
    """
    Runs num_games games, with no printing except for a report on which game 
    number is currently being played, and reports final number
    of games won by player 1 and draws. args specifies whether player 1 or
    player 2 is MCTS and how many rollouts to use. For multiple games, you
    probably do not want to include the --displayBoard option in args, as
    this will do lots of printing and make running relatively slow.
    """

    start  = time.perf_counter()

    player1GamesWon = 0
    draws = 0

    #writer = csv.writer(open('data.csv', 'w'))

    if args.parallel:
        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = [executor.submit(play_game, args) for _ in range(num_games)]

            for f in concurrent.futures.as_completed(results):
                result, state_list = f.result()
                winner = result.state.value()
                # for row in state_list:
                #     writer.writerow(row + [winner])
                
                print('done')


                if winner == 1:
                    player1GamesWon += 1
                elif winner == 0:
                    draws += 1

            print("Player 1 games won: " + str(player1GamesWon) + "/" + str(num_games))
            print("Draws: " + str(draws) + "/" + str(num_games))
            finish = time.perf_counter()
            print(round(finish-start, 3))
    else:
        for i in range(num_games):
            print("Game " + str(i))
            result, state_list = play_game(args)
            winner = result.state.value()
            # for row in state_list:
            #     writer.writerow(row + [winner])

            if winner == 1:
                player1GamesWon += 1
            elif winner == 0:
                draws += 1
        print("Player 1 games won: " + str(player1GamesWon) + "/" + str(num_games))
        print("Draws: " + str(draws) + "/" + str(num_games))
        finish = time.perf_counter()
        print(round(finish-start, 3))

def play_game(args):
    """
    Play one game against another player.
    args specifies whether player 1 or player 2 is MCTS (
    or both if rolloutsSecondMCTSAgent is non-zero)
    and how many rollouts to use.
    Returns the final terminal node for the game.
    """

    state_list = []

    # Make start state and root of MCTS tree
    start_state = DBGame.new_game()
    root1 = Node(start_state, None)
    if args.rolloutsSecondMCTSAgent != 0:
        root2 = Node(start_state, None)

    # Run MCTS
    node = root1
    if args.rolloutsSecondMCTSAgent != 0:
        node2 = root2
    while not node.state.isTerminal():
        if (not args.second and node.state.turn == 1) or \
                (args.second and node.state.turn == -1):
            move = MCTS(node, args.rollouts)
            if DISPLAY_BOARDS:
                DBGame.print_board(node.state)
        else:
            if args.rolloutsSecondMCTSAgent == 0:
                move = random_move(node)
            else:
                move = MCTS(node2, args.rolloutsSecondMCTSAgent)
                if DISPLAY_BOARDS:
                    DBGame.print_board(node2.state)

        node.addMove(move)
        node = node.children[move]
        state_list.append(node.state.toVector())
        if args.rolloutsSecondMCTSAgent != 0:
            node2.addMove(move)
            node2 = node2.children[move]

    if DISPLAY_BOARDS:
        DBGame.print_board(node.state)
    
    return node, state_list

            
    

def main():
    """
    Play a game of Dots and Boxes using MCTS to choose the moves for one of the players.
    args on command line set properties; see parse_args() for details.
    """
    # Get commandline arguments
    args = parse_args()

    if args.numGames > 1:
        run_multiple_games(args.numGames, args)
    else:
        # Play the game
        node = play_game(args)
    
        # Print result
        winner = node.state.value()
        DBGame.print_board(node.state)
        print("Player 1 Boxes: ", node.state.player1_score)
        print("Player 2 Boxes: ", node.state.player2_score)
        if winner == 1:
            print("Player 1 wins")
        elif winner == -1:
            print("Player 2 wins")
        else:
            print("It's a draw")
            
            
if __name__ == "__main__":
    main()
