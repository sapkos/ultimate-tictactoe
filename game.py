import numpy as np

from environment import Environment
from agent import Agent


def get_state_hash_and_winner(env: Environment, i=0, j=0):
    results = []

    for v in (0, env.x, env.o):
        env.board[env.next_block_y, env.next_block_y].board[i, j] = v
        if j == 2:
            if i == 2:
                state = env.get_state()
                ended = env.game_over(force_recalculate=True)
                winner = env.winner
                results.append((state, winner, ended))
            else:
                results += get_state_hash_and_winner(env, i+1, 0)
        else:
            results += get_state_hash_and_winner(env, i, j+1)

    return results


def initial_v_x(env: Environment, state_winner_triples):
    V = np.zeros(env.num_states)
    for state, winner, ended in state_winner_triples:
        if ended:
            if winner == env.x:
                v = 1
            else:
                v = 0
        else:
            v = 0.5
        V[state] = v
    return V


def initial_v_o(env: Environment, state_winner_triples):
    V = np.zeros(env.num_states)
    for state, winner, ended in state_winner_triples:
        if ended:
            if winner == env.o:
                v = 1
            else:
                v = 0
        else:
            v = 0.5
        V[state] = v
    return V


def play_game(p1: Agent, p2: Agent, env: Environment):
    current_player = None
    while not env.game_over():
        if current_player == p1:
            current_player = p2
        else:
            current_player = p1

        current_player.take_action(env)

        state = env.get_state()
        p1.update_state_history(state)
        p2.update_state_history(state)

    p1.update(env)
    p2.update(env)

if __name__ == '__main__':
    p1 = Agent()
    p2 = Agent()

    env = Environment()
    state_winner_triples = get_state_hash_and_winner(env)

    Vx = initial_v_x(env, state_winner_triples)
    Vo = initial_v_o(env, state_winner_triples)

    p1.sym = env.x
    p2.sym = env.o

    T = 10000
    for t in range(T):
        if t % 200 == 0:
            print(t)
        play_game(p1, p2, Environment())


