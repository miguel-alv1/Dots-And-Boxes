from os import WIFCONTINUED
import numpy as np
import copy

# Number of Dots, not lines!
HEIGHT = 5
WIDTH = 5

moves = [((0, 0), (0, 1)), ((0, 1), (0, 2)), ((0, 2), (0, 3)), ((0, 3), (0, 4)), ((1, 0), (1, 1)),
         ((1, 1), (1, 2)), ((1, 2), (1, 3)), ((1, 3), (1, 4)), ((2, 0), (2, 1)), ((2, 1), (2, 2)), 
         ((2, 2), (2, 3)), ((2, 3), (2, 4)), ((3, 0), (3, 1)), ((3, 1), (3, 2)), ((3, 2), (3, 3)), 
         ((3, 3), (3, 4)), ((4, 0), (4, 1)), ((4, 1), (4, 2)), ((4, 2), (4, 3)), ((4, 3), (4, 4)), 
         ((0, 0), (1, 0)), ((1, 0), (2, 0)), ((2, 0), (3, 0)), ((3, 0), (4, 0)), ((0, 1), (1, 1)), 
         ((1, 1), (2, 1)), ((2, 1), (3, 1)), ((3, 1), (4, 1)), ((0, 2), (1, 2)), ((1, 2), (2, 2)), 
         ((2, 2), (3, 2)), ((3, 2), (4, 2)), ((0, 3), (1, 3)), ((1, 3), (2, 3)), ((2, 3), (3, 3)), 
         ((3, 3), (4, 3)), ((0, 4), (1, 4)), ((1, 4), (2, 4)), ((2, 4), (3, 4)), ((3, 4), (4, 4))]

class State:
    def __init__(self, state=None, move=None):
        self.prev_move_filled_box = False

        if state==None:
            self._boxes = [0]*((WIDTH - 1) * (HEIGHT - 1))
            self._box_owner = [' ']*((WIDTH - 1) * (HEIGHT - 1))
            self._lines = {}
            self.turn = 1
            self.player1_score = 0
            self.player2_score = 0

            # Map horizontal lines to adjacent box numbers
            for i in range(HEIGHT):
                for j in range(WIDTH - 1):
                    k = ((i, j), (i, j + 1))
                    # Connect to box below
                    if i < HEIGHT - 1:
                        if k in self._lines:
                            self._lines[k].append((i * (WIDTH - 1)) + j)
                        else:
                            self._lines[k] = [(i * (WIDTH - 1)) + j]
                    # Connect to box above
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
                    # Connect to box right adjacent box
                    if j < WIDTH - 1:
                        if k in self._lines:
                            self._lines[k].append(((i * (WIDTH - 1)) + j))
                        else:
                            self._lines[k] = [(i * (WIDTH - 1)) + j]
                    # Connect to box left adjacent box
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
            self._box_owner = copy.copy(state._box_owner)
            self.turn = -state.turn

            if move is not None:
                try:
                    boxes = self._lines[move]

                    for box in boxes:
                        self._boxes[box] += 1
                        if self._boxes[box] == 4:
                            self.fillBox(box, state)
                            self.prev_move_filled_box = True

                    #remove move from available moves in this state
                    del self._lines[move]
                except KeyError as e:
                    print("Invalid Move")

            if state.prev_move_filled_box:
                self.turn = state.turn

    def getMoves(self):
        return self._lines

    def nextState(self, move):
        return State(self, move)

    def fillBox(self, box, prevstate):
        if prevstate.turn == 1:
            self.player1_score += 1
            self._box_owner[box] = 'R'
        else:
            self.player2_score += 1
            self._box_owner[box] = 'B'

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

    def toVector(self):
        vector = [0.25]*(((WIDTH - 1)*WIDTH) + (((HEIGHT - 1)*HEIGHT)) + (HEIGHT - 1)*(WIDTH - 1))
        for i in range(len(moves)):
            e = moves[i]
            if e in self._lines:
                vector[i] = 0

        for j in range((HEIGHT - 1)*(WIDTH - 1)):
            if self._box_owner[j] == 'R':
                vector[i + j + 1] = 0.5
            elif self._box_owner[j] == 'B':
                vector[i + j + 1] = 0.75
            else:
                vector[i + j + 1] = 1

        return vector
            




def new_game() -> State:
    return State()


def print_board(state):
    sb1 = '.'
    sb2 = ''
    for i in range(HEIGHT - 1):
        j = 0
        while j < WIDTH - 1:
            if ((i, j), (i, j + 1)) in state._lines:
                sb1 += '     .'
            else:
                sb1 += '-----.'
            j += 1

        j = 0

        while j < WIDTH:
            if ((i, j), (i + 1, j)) in state._lines:
                sb2 += '      '
            else:
                if j < WIDTH - 1:
                    # Get box index number from formula used above for vertical lines
                    # Note Player 1 is 'R' and Player 2 is 'B'
                    sb2 += '|  {}  '.format(state._box_owner[(i * (WIDTH - 1)) + j])
                else:
                    sb2 += '|    '
            j += 1
        print(sb1)
        print(sb2)
        sb1 = '.'
        sb2 = ''

    for j in range(WIDTH - 1):
        if ((HEIGHT - 1, j), (HEIGHT - 1, j + 1)) in state._lines:
            sb1 += '     .'
        else:
            sb1 += '-----.'

    print(sb1)
    print(sb2)

if __name__ == '__main__':
    state = State()
    print(list(state._lines.keys()))