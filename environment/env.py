# https://deeplearningcourses.com/c/artificial-intelligence-reinforcement-learning-in-python
# https://www.udemy.com/artificial-intelligence-reinforcement-learning-in-python
# Simple reinforcement learning algorithm for learning tic-tac-toe
# Use the update rule: V(s) = V(s) + alpha*(V(s') - V(s))
# Use the epsilon-greedy policy:
#   action|s = argmax[over all actions possible from state s]{ V(s) }  if rand > epsilon
#   action|s = select random action from possible actions from state s if rand < epsilon

import numpy as np

LENGTH = 3


class SmallEnvironment(object):
    def __init__(self):
        self.board = np.zeros((LENGTH, LENGTH))
        self.x = -1
        self.o = 1
        self.winner = None
        self.ended = False
        self.num_states = 3 ** (LENGTH * LENGTH)

    def is_empty(self, i, j):
        return self.board[i, j] == 0

    def game_over(self, force_recalcuate=False):
        if not force_recalcuate and self.ended:
            return self.ended
        # rows
        for i in range(LENGTH):
            for player in (self.x, self.o):
                if self.board[i].sum() == player * LENGTH:
                    self.winner = player
                    self.ended = True
                    return True

        # columns
        for j in range(LENGTH):
            for player in (self.x, self.o):
                if self.board[:, j].sum() == player * LENGTH:
                    self.winner = player
                    self.ended = True
                    return True

        # diagonal
        for player in (self.x, self.o):
            if self.board.trace() == player * LENGTH:
                self.winner = player
                self.ended = True

            if np.fliplr(self.board).trace() == player * LENGTH:
                self.winner = player
                self.ended = True

        # if draw
        if np.all((self.board == 0) is False):
            self.winner = None
            self.ended = True
            return True

        self.winner = None
        return False

    def is_draw(self):
        return self.ended and self.winner is None
