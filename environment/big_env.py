import numpy as np
from environment.env import SmallEnvironment, LENGTH

BIG_LENGTH = 9


class Environment(object):
    def __init__(self):
        self.board = np.empty((3, 3), object)
        for i in range(LENGTH):
            for j in range(LENGTH):
                self.board[i, j] = SmallEnvironment()
        self.x = -1
        self.o = 1
        self.winner = None
        self.ended = False
        self.num_states = 3**(BIG_LENGTH * BIG_LENGTH)
        self.next_block_x = 1
        self.next_block_y = 1

    def is_empty(self, big_i, big_j, i, j):
        return self.board[big_i, big_j].is_empty(i, j)

    def reward(self, sym):
        if not self.game_over():
            return 0

        return 1 if self.winner == sym else 0

    def get_state(self):
        k = 0
        h = 0
        for big_i in range(LENGTH):
            for big_j in range(LENGTH):
                for i in range(LENGTH):
                    for j in range(LENGTH):
                        if self.board[big_i, big_j].board[i, j] == 0:
                            v = 0
                        elif self.board[big_i, big_j].board[i, j] == self.x:
                            v = 1
                        elif self.board[big_i, big_j].board[i, j] == self.o:
                            v = 2
                        h += (3**k) * v
                        k += 1
        return h

    def game_over(self, force_recalculate=False):
        if not force_recalculate and self.ended:
            return self.ended
        for i in range(LENGTH):
            for j in range(LENGTH):
                if self.board[i, j].game_over(force_recalculate):
                    self.winner = self.board[i, j].winner
                    self.ended = True
                    return True

    def is_draw(self):
        return self.ended and self.winner is None
