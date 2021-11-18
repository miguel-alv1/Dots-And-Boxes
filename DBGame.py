import numpy as np
import copy

# Number of Dots, not lines!
HEIGHT = 6
WIDTH = 6

class State:
    def __init__(self, state=None, move=None):
        self.prev_move_filled_box = False

        if state==None:

            self._boxes = [0]*((WIDTH - 1) * (HEIGHT - 1))
            self._lines = {}
            self.turn = 1
            self.player1_score = 0
            self.player2_score = 0

            # Map horizontal lines to adjacent box numbers
            for i in range(HEIGHT):
                for j in range(WIDTH - 1):
                    k = ((i, j), (i, j + 1))
                    if i < HEIGHT - 1:
                        if k in self._lines:
                            self._lines[k].append((i * (WIDTH - 1)) + j)
                        else:
                            self._lines[k] = [(i * (WIDTH - 1)) + j]
                    if i > 0:
                        k = ((i, j), (i, j + 1))
                        if k in self._lines:
                            self._lines[k].append(((i - 1) * (WIDTH - 1)) + j)
                        else:
                            self._lines[k] = [((i - 1) * (WIDTH - 1)) + j]

            # Map vertical lines to adjacent box numbers
            for j in range(WIDTH):
                for i in range(HEIGHT - 1):
                    k = ((i, j), (i + 1, j))
                    if j < WIDTH - 1:
                        if k in self._lines:
                            self._lines[k].append(((i * (WIDTH - 1)) + j))
                        else:
                            self._lines[k] = [(i * (WIDTH - 1)) + j]
                    if j > 0:
                        if k in self._lines:
                            self._lines[k].append(((i * (WIDTH - 1)) + j) - 1)
                        else:
                            self._lines[k] = [(i * (WIDTH - 1)) + j - 1]
        else:
            self._boxes = copy.copy(state._boxes)
            self._lines = copy.copy(state._lines)
            self.player1_score = state.player1_score
            self.player2_score = state.player2_score
            self.turn = -state.turn

            if move is not None:
                try:
                    boxes = self._lines[move]

                    for box in boxes:
                        self._boxes[box] += 1
                        if self._boxes[box] == 4:
                            self.fillBox(state)
                            self.prev_move_filled_box = True

                    #remove move pool of available moves from this state
                    del self._lines[move]
                except KeyError as e:
                    print("Invalid Move")

            if state.prev_move_filled_box:
                self.turn = state.turn
    
    def getMoves(self):
        return self._lines

    def nextState(self, move):
        return State(self, move)

    def fillBox(self, prevstate):
        if prevstate.turn == 1:
            self.player1_score += 1
        else:
            self.player2_score += 1

        # TODO: Keep track of which players own which boxes

    def isTerminal(self):
        if self._lines:
            return False
        else:
            return True

    def value(self):
        if not self._lines:
            if self.player1_score > self.player2_score:
                return 1
            elif self.player1_score < self.player2_score:
                return -1
            else:
                return 0
        else:
            return 0


def new_game() -> State:
    return State()

# '''.-----.
#    |  R  |
#    .-----.'''


if __name__=='__main__':
    db = State()
    print(db._lines)
