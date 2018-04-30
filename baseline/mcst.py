import time
import numpy as np
import collections
import sys
import math
from random import choice
from board import hashable


class Mcst:

    def __init__(self, board, time_limit):
        self.time_limit = time_limit
        self.board = board
        self.states = []  # (MOVE, STATE)
        self.wins = {}    # (PLAYER, STATE)
        self.plays = {}   # (PLAYER, STATE)
        self.states.append((1,self.board.init_representation()))

    def search_move(self):
        begin_time = time.time()
        simulated_games = 0

        current_state = self.states[-1]
        possible_moves = self.board.legal_plays(current_state[1])

        next_states = self.expand_state(current_state[1])
        player1 = self.board.current_player(current_state[1])
        player2 = self.board.current_player(choice(next_states)[1])

        if possible_moves.shape[0] == 0:
            return -1

        while time.time() - begin_time < self.time_limit:
            random_state = choice(next_states)
            self.simulate_random_game(random_state[1], player1)
            simulated_games += 1

        print("Simulated games: " + str(simulated_games))

        r,c,o = self.get_best_move(current_state[1], player2, next_states)
        return r.item(),c.item(),o

    def expand_state(self, current_state):
        next_states = []
        moves = self.board.legal_plays(current_state)
        for move in moves:
            new_state, move_done = self.board.next_state(current_state, move)
            next_states.append((move_done, new_state))

            player = self.board.current_player(new_state)

            self.plays[(player, hashable(new_state))] = 0
            self.wins[(player, hashable(new_state))] = 0

        return next_states

    def get_best_move(self, current_state, player, next_states):

        win_rate, best_move = max((self.wins.get((player, hashable(state)), 0) / self.plays.get((player, hashable(state)), 1), move)
                       for move, state in next_states)

        print("Picked move " + str(best_move) + " with win rate of " + str(win_rate))
        r,c,o = self.board.translate_to_coord(best_move)
        return r,c,o

    def simulate_random_game(self, state, player1):

        state_copy = np.copy(state)
        player = self.board.current_player(state)

        while not self.board.is_finished(state_copy):
            possible_moves = self.board.legal_plays(state_copy)
            random_move = choice(possible_moves)

            state_copy, move = self.board.next_state(state_copy, random_move)

        winner = self.board.winner(state_copy)
        state_hash = hashable(state)

        self.plays[(player, state_hash)] += 1
        if player1 == winner:
                self.wins[(player, state_hash)] += 1

    def register_other_player_move(self, row, col, ori, player):
        (move, state) = self.states[-1]
        new_state, new_move = self.board.register_state(state, row, col, ori, player)
        self.states.append((new_move, new_state))



