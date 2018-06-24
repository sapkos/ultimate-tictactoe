import numpy as np
from environment.env import LENGTH
from environment.big_env import Environment


class Agent(object):
    def __init__(self, eps=0.1, alpha=0.5):
        self.eps = eps,
        self.alpha = alpha,
        self.verbose = False,
        self.state_history = []
        self.__V = None
        self.__sym = None

    @property
    def v(self):
        return self.__V

    @v.setter
    def v(self, v):
        self.__V = v

    @property
    def sym(self):
        return self.__sym

    @sym.setter
    def sym(self, sym):
        self.__sym = sym

    def reset_history(self):
        self.state_history = []

    def take_action(self, env: Environment):
        # eps greedy
        r = np.random.rand()
        best_state = None
        if r < self.eps:
            if self.verbose:
                print('yolo')
            possible_moves = []
            for i in range(LENGTH):
                for j in range(LENGTH):
                    if env.is_empty(env.next_block_x, env.next_block_y, i, j):
                        possible_moves.append((i, j))
            id_move = np.random.choice(len(possible_moves))
            next_move = possible_moves[id_move]
        else:
            # choose best action based on current value of states
            pos2value = {}
            next_move = None
            best_value = -1
            for i in range(LENGTH):
                for j in range(LENGTH):
                    if env.is_empty(env.next_block_x, env.next_block_y, i, j):
                        # what's the state if I make this move?
                        env.board[env.next_block_x, env.next_block_y].board[i, j] = self.sym
                        state = env.get_state()
                        # im just tryin
                        env.board[env.next_block_x, env.next_block_y].board[i, j] = 0
                        pos2value[(i, j)] = self.__V[state]
                        if self.__V[state] > best_value:
                            best_value = self.__V[state]
                            best_state = state
                            next_move = (i, j)
        if self.verbose:
            print("I'm greedy now")
            for i in range(LENGTH):
                print("------------------")
                for j in range(LENGTH):
                    if env.board[env.next_block_x, env.next_block_y].is_empty(i, j):
                        # print the value
                        print(" %.2f|" % pos2value[(i, j)], end="")
                    else:
                        print("  ", end="")
                        if env.board[env.next_block_x, env.next_block_y].board[i, j] == env.x:
                            print("x  |", end="")
                        elif env.board[env.next_block_x, env.next_block_y].board[i, j] == env.o:
                            print("o  |", end="")
                        else:
                            print("   |", end="")
                print("")
            print("------------------")

        env.board[env.next_block_x, env.next_block_y, next_move[0], next_move[1]] = self.sym

    def update_state_history(self, s):
        self.state_history.append(s)

    # after a good game we should learn something
    def update(self, env: Environment):
        reward = env.reward(self.sym)
        target = reward
        for prev in reversed(self.state_history):
            value = self.__V[prev] + self.alpha*(target - self.V[prev])
            self.V[prev] = value
            target = value
        self.reset_history()



