import numpy as np

HEIGHT = 3
WIDTH = 3

class State:
    def __init__(self, state=None, move=None):
        if state==None:
            self._boxes = [0]*(WIDTH * HEIGHT)
            self._lines = {}

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


if __name__=='__main__':
    db = State()
    print(db._lines)
